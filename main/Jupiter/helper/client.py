"""Solana client and keypair management"""
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from main.shared.config import get_solana_keypair, SOLANA_RPC_URL

_client_instance = None

def get_client():
    """Get Solana RPC client (cached singleton)"""
    global _client_instance
    if _client_instance is None:
        _client_instance = Client(SOLANA_RPC_URL)
    return _client_instance

def get_keypair():
    """Get Solana keypair from environment"""
    return get_solana_keypair()

def get_address():
    """Get Solana wallet address"""
    keypair = get_keypair()
    return str(keypair.pubkey())

