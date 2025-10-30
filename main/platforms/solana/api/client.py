"""
Solana client and keypair management
"""
from solana.rpc.api import Client
from solders.keypair import Keypair
from main.core.config import get_solana_keypair, SOLANA_RPC_URL


_client_instance = None


def get_client() -> Client:
    """Get Solana RPC client (cached singleton)
    
    Returns:
        Client: Solana RPC client
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = Client(SOLANA_RPC_URL)
    return _client_instance


def get_keypair() -> Keypair:
    """Get Solana keypair from environment
    
    Returns:
        Keypair: Solana keypair
    """
    return get_solana_keypair()

