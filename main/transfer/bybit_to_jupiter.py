"""
DEPRECATED: This file has been split into multiple modules for better organization.

New module structure:
- solana_wallet.py: Wallet operations (get_solana_wallet_address)
- bybit_internal.py: Internal transfers (transfer_unified_to_fund)
- bybit_withdraw.py: Withdrawal operations (withdraw_from_bybit)
- transfer_to_jupiter.py: Main transfer function (transfer_all_to_jupiter)
- transfer_multiple_to_jupiter.py: Batch transfer function (transfer_multiple_to_jupiter)

This file now re-exports the functions from the new modules for backward compatibility.
"""

# Import all functions from new modules
from .solana_wallet import get_solana_wallet_address
from .bybit_internal import transfer_unified_to_fund
from .bybit_withdraw import withdraw_from_bybit
from .transfer_to_jupiter import transfer_all_to_jupiter

# Re-export all functions
__all__ = [
    'get_solana_wallet_address',
    'transfer_unified_to_fund',
    'withdraw_from_bybit',
    'transfer_all_to_jupiter'
]


if __name__ == "__main__":
    import json
    # Example: Run the complete transfer flow
    result = transfer_all_to_jupiter()
    print("\nFinal result:", json.dumps(result, indent=2))
