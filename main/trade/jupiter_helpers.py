import requests
import json
import os
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from spl.token.instructions import get_associated_token_address


def get_jupiter_quote(input_mint, output_mint, amount):
    response = requests.get("https://lite-api.jup.ag/swap/v1/quote", params={
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount
    })
    data = response.json()
    return None if "error" in data else data


def _load_tokens():
    path = os.path.join(os.path.dirname(__file__), "../../files/unique_mint_by_symbol.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_balance(symbol):
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    client = Client("https://api.mainnet-beta.solana.com")
    
    # Handle SOL balance separately
    if symbol.upper() == "SOL":
        balance_lamports = client.get_balance(keypair.pubkey()).value
        return balance_lamports / 1e9
    
    # For SPL tokens, get token account balance
    tokens = _load_tokens()
    token_data = tokens.get(symbol.upper(), [None])[0]
    if not token_data:
        raise ValueError(f"Token not found: {symbol}")
    
    mint = Pubkey.from_string(token_data["mint"])
    token_account = get_associated_token_address(keypair.pubkey(), mint)
    
    try:
        response = client.get_token_account_balance(token_account)
        balance = float(response.value.amount) / (10 ** token_data["decimals"])
        return balance
    except Exception as e:
        print(f"Error getting balance for {symbol}: {e}")
        return 0.0

