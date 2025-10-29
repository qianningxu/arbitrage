import requests
import base64
import os
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from trade.jupiter_helpers import get_jupiter_quote, _load_tokens, check_balance


def swap(quote):
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    
    swap_tx = requests.post("https://lite-api.jup.ag/swap/v1/swap", json={
        "quoteResponse": quote,
        "userPublicKey": str(keypair.pubkey()),
        "wrapAndUnwrapSol": True
    }, timeout=15).json()
    
    raw_tx = base64.b64decode(swap_tx["swapTransaction"])
    transaction = VersionedTransaction.from_bytes(raw_tx)
    signed_tx = VersionedTransaction(transaction.message, [keypair])
    
    client = Client("https://api.mainnet-beta.solana.com")
    result = client.send_raw_transaction(bytes(signed_tx), opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    
    tx_sig = str(result.value)
    print(f"✅ https://solscan.io/tx/{tx_sig}")
    return tx_sig


def trade(input_symbol, output_symbol, amount):
    """Trade tokens by symbol"""
    tokens = _load_tokens()
    
    input_data = tokens.get(input_symbol.upper(), [None])[0]
    if not input_data:
        raise ValueError(f"Token not found: {input_symbol}")
    
    output_data = tokens.get(output_symbol.upper(), [None])[0]
    if not output_data:
        raise ValueError(f"Token not found: {output_symbol}")
    
    input_mint = input_data["mint"]
    output_mint = output_data["mint"]
    amount_lamports = int(amount * (10 ** input_data["decimals"]))
    
    quote = get_jupiter_quote(input_mint, output_mint, amount_lamports)
    if not quote:
        raise ValueError("Failed to get quote")
    
    print(f"Trading {input_symbol} -> {output_symbol}: {amount}")
    return swap(quote)


if __name__ == "__main__":
    # Check USDT balance
    usdt_balance = check_balance("SOL")
    print(f"SOL Balance: {usdt_balance}")
    
    # trade("SOL", "USDT", 0.001)
