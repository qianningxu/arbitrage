import os
import json
from dotenv import load_dotenv
from solders.keypair import Keypair
from solana.rpc.api import Client

load_dotenv()


def _load_tokens():
    """Load tokens from unique_mint_by_symbol.json"""
    path = os.path.join(os.path.dirname(__file__), "../../files/unique_mint_by_symbol.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_solana_wallet_address():
    """Get Solana wallet address from private key in .env"""
    private_key = os.getenv("SOLANA_PRIVATE_KEY")
    if not private_key:
        raise ValueError("SOLANA_PRIVATE_KEY must be set in .env file")
    
    keypair = Keypair.from_base58_string(private_key)
    address = str(keypair.pubkey())
    return address


def get_sol_balance(keypair, client):
    """Get SOL balance of wallet"""
    balance_response = client.get_balance(keypair.pubkey())
    return balance_response.value / 1e9

