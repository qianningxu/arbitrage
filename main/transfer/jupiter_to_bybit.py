import os
import json
import requests
import time
import hmac
import hashlib
from dotenv import load_dotenv
from solders.keypair import Keypair

# Load environment variables from .env file
load_dotenv()
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from spl.token.instructions import transfer_checked, TransferCheckedParams, get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID


def _load_tokens():
    """Load tokens from unique_mint_by_symbol.json"""
    path = os.path.join(os.path.dirname(__file__), "../../files/unique_mint_by_symbol.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_bybit_deposit_address(coin_symbol):
    """Get Bybit deposit address via API"""
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    
    url = "https://api.bybit.com/v5/asset/deposit/query-address"
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    coin = coin_symbol.upper()
    
    param_str = f"coin={coin}&chainType=SOL"
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }
    
    response = requests.get(url, params={"coin": coin, "chainType": "SOL"}, headers=headers)
    data = response.json()
    
    if data.get("retCode") != 0:
        raise ValueError(f"Bybit API error: {data.get('retMsg')}")
    
    for chain in data.get("result", {}).get("chains", []):
        if chain.get("chainType") == "SOL" and chain.get("addressDeposit"):
            address = chain["addressDeposit"]
            print(f"📍 Bybit deposit address for {coin}: {address}")
            return address
    
    raise ValueError(f"No SOL deposit address found for {coin}")


def get_sol_balance(keypair, client):
    """Get SOL balance of wallet"""
    balance_response = client.get_balance(keypair.pubkey())
    return balance_response.value / 1e9


def send_native_sol(destination_address, amount):
    """Send native SOL"""
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    client = Client("https://api.mainnet-beta.solana.com")
    
    # Check balance
    balance = get_sol_balance(keypair, client)
    print(f"💰 Current balance: {balance:.6f} SOL")
    
    # Add buffer for transaction fees (typically ~0.000005 SOL)
    required = amount + 0.00001
    if balance < required:
        raise ValueError(f"Insufficient balance! Have {balance:.6f} SOL, need at least {required:.6f} SOL (including fees)")
    
    dest_pubkey = Pubkey.from_string(destination_address)
    lamports = int(amount * 1e9)
    
    transfer_ix = transfer(TransferParams(
        from_pubkey=keypair.pubkey(),
        to_pubkey=dest_pubkey,
        lamports=lamports
    ))
    
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message.new_with_blockhash([transfer_ix], keypair.pubkey(), recent_blockhash)
    transaction = Transaction.new_unsigned(message)
    transaction.sign([keypair], recent_blockhash)
    
    result = client.send_transaction(transaction, opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    
    tx_sig = str(result.value)
    print(f"✅ Transfer sent: https://solscan.io/tx/{tx_sig}")
    return tx_sig


def send_spl_token(token_mint, destination_address, amount, decimals):
    """Send SPL token"""
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    client = Client("https://api.mainnet-beta.solana.com")
    
    mint_pubkey = Pubkey.from_string(token_mint)
    dest_pubkey = Pubkey.from_string(destination_address)
    source_ata = get_associated_token_address(keypair.pubkey(), mint_pubkey)
    dest_ata = get_associated_token_address(dest_pubkey, mint_pubkey)
    amount_lamports = int(amount * (10 ** decimals))
    
    transfer_ix = transfer_checked(TransferCheckedParams(
        program_id=TOKEN_PROGRAM_ID,
        source=source_ata,
        mint=mint_pubkey,
        dest=dest_ata,
        owner=keypair.pubkey(),
        amount=amount_lamports,
        decimals=decimals
    ))
    
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message.new_with_blockhash([transfer_ix], keypair.pubkey(), recent_blockhash)
    transaction = Transaction.new_unsigned(message)
    transaction.sign([keypair], recent_blockhash)
    
    result = client.send_transaction(transaction, opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    
    tx_sig = str(result.value)
    print(f"✅ Transfer sent: https://solscan.io/tx/{tx_sig}")
    return tx_sig


def transfer_to_bybit(coin_symbol, amount):
    """Transfer coins from Solana wallet to Bybit"""
    tokens = _load_tokens()
    coin_symbol = coin_symbol.upper()
    
    coin_data = tokens.get(coin_symbol, [None])[0]
    if not coin_data:
        raise ValueError(f"Token not found: {coin_symbol}")
    
    print(f"🔍 Fetching Bybit deposit address for {coin_symbol}...")
    bybit_address = get_bybit_deposit_address(coin_symbol)
    
    print(f"💸 Sending {amount} {coin_symbol} to Bybit...")
    
    if coin_symbol == "SOL":
        tx_sig = send_native_sol(bybit_address, amount)
    else:
        tx_sig = send_spl_token(coin_data["mint"], bybit_address, amount, coin_data["decimals"])
    
    return tx_sig


if __name__ == "__main__":
    # Reduced to 0.1 SOL to account for current balance
    transfer_to_bybit("SOL", 0.1)

