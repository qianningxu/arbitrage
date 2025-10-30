"""
DEPRECATED: This file has been split into multiple modules for better organization.

New module structure:
- solana_wallet.py: Wallet operations (_load_tokens, get_solana_wallet_address, get_sol_balance)
- solana_send.py: Send operations (send_native_sol, send_spl_token)
- bybit_deposit.py: Bybit deposit address (get_bybit_deposit_address)
- transfer_to_bybit.py: Main transfer function (transfer_to_bybit)
- transfer_multiple_to_bybit.py: Batch transfer function (transfer_multiple_to_bybit)

This file now re-exports the functions from the new modules for backward compatibility.
"""

# Import all functions from new modules
from .solana_wallet import _load_tokens, get_sol_balance
from .solana_send import send_native_sol, send_spl_token
from .bybit_deposit import get_bybit_deposit_address
from .transfer_to_bybit import transfer_to_bybit

# Re-export all functions
__all__ = [
    '_load_tokens',
    'get_bybit_deposit_address',
    'get_sol_balance',
    'send_native_sol',
    'send_spl_token',
    'transfer_to_bybit'
]


if __name__ == "__main__":
    # Example usage
    transfer_to_bybit("SOL", 0.1)
