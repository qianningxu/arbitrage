"""
Configuration and environment variable management
"""
import os
from dotenv import load_dotenv
from solders.keypair import Keypair

load_dotenv()


def get_env_var(key, required=True):
    """Get environment variable with optional requirement check
    
    Args:
        key: Environment variable key
        required: Whether the variable is required
        
    Returns:
        str: Environment variable value
        
    Raises:
        ValueError: If required variable is missing
    """
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def get_solana_keypair():
    """Get Solana keypair from environment
    
    Returns:
        Keypair: Solana keypair object
        
    Raises:
        ValueError: If SOLANA_PRIVATE_KEY is not set
    """
    private_key = get_env_var("SOLANA_PRIVATE_KEY")
    return Keypair.from_base58_string(private_key)


def get_bybit_credentials():
    """Get Bybit API credentials from environment
    
    Returns:
        tuple: (api_key, api_secret)
        
    Raises:
        ValueError: If credentials are not set
    """
    api_key = get_env_var("BYBIT_API_KEY")
    api_secret = get_env_var("BYBIT_API_SECRET")
    return api_key, api_secret


# Solana configuration
SOLANA_RPC_URL = get_env_var("SOLANA_RPC_URL", required=False) or "https://api.mainnet-beta.solana.com"
SOLANA_BASE_FEE_LAMPORTS = 5000  # Fixed base fee per signature

# Bybit configuration
BYBIT_API_BASE = "https://api.bybit.com"

