"""Configuration and environment variable management"""
import os
from dotenv import load_dotenv
from solders.keypair import Keypair

load_dotenv()

def get_env_var(key, required=True):
    """Get environment variable with optional requirement check"""
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value

def get_solana_keypair():
    """Get Solana keypair from environment"""
    private_key = get_env_var("SOLANA_PRIVATE_KEY")
    return Keypair.from_base58_string(private_key)

def get_bybit_credentials():
    """Get Bybit API credentials from environment"""
    api_key = get_env_var("BYBIT_API_KEY")
    api_secret = get_env_var("BYBIT_API_SECRET")
    return api_key, api_secret

SOLANA_RPC_URL = get_env_var("SOLANA_RPC_URL", required=False) or "https://api.mainnet-beta.solana.com"
SOLANA_BASE_FEE_LAMPORTS = 5000
BYBIT_API_BASE = "https://api.bybit.com"

