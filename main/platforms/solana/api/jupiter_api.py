"""
Jupiter DEX API integration
"""
import base64
import requests
from solders.transaction import VersionedTransaction
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from .client import get_client, get_keypair


def get_quote(input_mint: str, output_mint: str, amount: int, slippage_bps: int = 50) -> dict:
    """Get swap quote from Jupiter
    
    Args:
        input_mint: Input token mint address
        output_mint: Output token mint address
        amount: Amount in token's smallest unit (lamports/decimals)
        slippage_bps: Slippage tolerance in basis points (default: 50 = 0.5%)
        
    Returns:
        dict or None: Quote data (outAmount already includes LP/DEX fees)
    """
    response = requests.get("https://api.jup.ag/swap/v1/quote", params={
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": slippage_bps
    })
    data = response.json()
    return None if "error" in data else data


def execute_swap(quote: dict, priority_fee_lamports: int = None) -> str:
    """Execute swap with a quote
    
    Args:
        quote: Quote from get_quote()
        priority_fee_lamports: Optional priority fee for faster confirmation
        
    Returns:
        str: Transaction signature
    """
    keypair = get_keypair()
    client = get_client()
    
    # Build swap transaction
    swap_params = {
        "quoteResponse": quote,
        "userPublicKey": str(keypair.pubkey()),
        "wrapAndUnwrapSol": True
    }
    
    if priority_fee_lamports is not None:
        swap_params["prioritizationFeeLamports"] = priority_fee_lamports
    
    swap_tx = requests.post(
        "https://api.jup.ag/swap/v1/swap",
        json=swap_params,
        timeout=15
    ).json()
    
    # Sign and send
    raw_tx = base64.b64decode(swap_tx["swapTransaction"])
    transaction = VersionedTransaction.from_bytes(raw_tx)
    signed_tx = VersionedTransaction(transaction.message, [keypair])
    
    result = client.send_raw_transaction(bytes(signed_tx), opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    
    tx_sig = str(result.value)
    print(f"✅ Jupiter swap: https://solscan.io/tx/{tx_sig}")
    return tx_sig


def get_recent_priority_fees() -> dict:
    """Get recent prioritization fees for adaptive fee setting
    
    Returns:
        dict: Priority fee statistics
    """
    client = get_client()
    try:
        fees_response = client.get_recent_prioritization_fees()
        if fees_response.value:
            fees = [f.prioritization_fee for f in fees_response.value]
            fees.sort()
            return {
                "min": min(fees) if fees else 0,
                "p50": fees[len(fees)//2] if fees else 0,
                "p75": fees[len(fees)*3//4] if fees else 0,
                "max": max(fees) if fees else 0
            }
    except:
        pass
    
    return {"min": 0, "p50": 0, "p75": 0, "max": 0}

