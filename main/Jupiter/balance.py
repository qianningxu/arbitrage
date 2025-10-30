"""Jupiter/Solana balance operations"""
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address
from main.shared.data import get_token_info
from .client import get_client, get_keypair

def get_sol_balance() -> float:
    """Get SOL balance"""
    client = get_client()
    keypair = get_keypair()
    balance_response = client.get_balance(keypair.pubkey())
    return balance_response.value / 1e9

def get_token_balance(symbol: str) -> float:
    """Get token balance for a specific symbol"""
    if symbol.upper() == "SOL":
        return get_sol_balance()
    token_info = get_token_info(symbol)
    if not token_info:
        raise ValueError(f"Token not found: {symbol}")
    client = get_client()
    keypair = get_keypair()
    mint = Pubkey.from_string(token_info["mint"])
    token_account = get_associated_token_address(keypair.pubkey(), mint)
    try:
        response = client.get_token_account_balance(token_account)
        balance = float(response.value.amount) / (10 ** token_info["decimals"])
        return balance
    except Exception as e:
        print(f"Error getting balance for {symbol}: {e}")
        return 0.0

def check_balance(symbol: str) -> float:
    """Check balance for a token symbol (alias)"""
    return get_token_balance(symbol)

def has_ata(mint_address: str) -> bool:
    """Check if wallet has Associated Token Account for a mint"""
    client = get_client()
    keypair = get_keypair()
    mint = Pubkey.from_string(mint_address)
    ata = get_associated_token_address(keypair.pubkey(), mint)
    try:
        account_info = client.get_account_info(ata)
        return account_info.value is not None
    except:
        return False

