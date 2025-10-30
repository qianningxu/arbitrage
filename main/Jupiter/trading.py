"""Jupiter trading and swaps"""
import base64
import requests
from solders.transaction import VersionedTransaction
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from main.shared.data import get_token_info
from .client import get_client, get_keypair
from .pricing import get_quote, get_recent_priority_fees
from .balance import check_balance

def execute_swap(quote, priority_fee_lamports=None):
    """Execute swap with a quote"""
    keypair = get_keypair()
    client = get_client()
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
    raw_tx = base64.b64decode(swap_tx["swapTransaction"])
    transaction = VersionedTransaction.from_bytes(raw_tx)
    signed_tx = VersionedTransaction(transaction.message, [keypair])
    result = client.send_raw_transaction(bytes(signed_tx), opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    tx_sig = str(result.value)
    print(f"✅ Jupiter swap: https://solscan.io/tx/{tx_sig}")
    return tx_sig

def swap(input_symbol, output_symbol, amount, slippage_bps=50, auto_priority_fee=True):
    """Swap tokens via Jupiter"""
    input_info = get_token_info(input_symbol)
    output_info = get_token_info(output_symbol)
    if not input_info:
        raise ValueError(f"Input token not found: {input_symbol}")
    if not output_info:
        raise ValueError(f"Output token not found: {output_symbol}")
    input_mint = input_info["mint"]
    output_mint = output_info["mint"]
    amount_lamports = int(amount * (10 ** input_info["decimals"]))
    quote = get_quote(input_mint, output_mint, amount_lamports, slippage_bps)
    if not quote:
        raise ValueError("Failed to get quote from Jupiter")
    print(f"🔄 Swapping {input_symbol} → {output_symbol}: {amount}")
    priority_fee = None
    if auto_priority_fee:
        fees = get_recent_priority_fees()
        priority_fee = fees["p75"]
        if priority_fee > 0:
            print(f"⚡ Priority fee: {priority_fee} lamports")
    return execute_swap(quote, priority_fee)

def trade(input_symbol, output_symbol, amount):
    """High-level trade function (alias for swap)"""
    return swap(input_symbol, output_symbol, amount)

def crypto_to_u(crypto, slippage_bps=50, auto_priority_fee=True):
    """Swap all crypto balance to USDT"""
    balance = check_balance(crypto)
    if balance <= 0:
        raise ValueError(f"No {crypto} balance to swap")
    print(f"💰 {crypto} balance: {balance}")
    return swap(crypto, "USDT", balance, slippage_bps, auto_priority_fee)

def u_to_crypto(crypto, slippage_bps=50, auto_priority_fee=True):
    """Swap all USDT to target crypto"""
    balance = check_balance("USDT")
    if balance <= 0:
        raise ValueError("No USDT balance to swap")
    print(f"💰 USDT balance: {balance}")
    return swap("USDT", crypto, balance, slippage_bps, auto_priority_fee)

