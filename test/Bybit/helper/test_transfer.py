"""Test bybit_transfer functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.Bybit.account.transfers import transfer_to_unified as transfer_all_to_unified


def test_transfer_all_to_unified():
    """Transfer all funds from FUND to UNIFIED (commented out - only run when ready)"""
    # Uncomment to execute real transfer:
    # results = transfer_all_to_unified()
    # print(f"Transfer results: {results}")
    
    print("Test transfer_all_to_unified function - uncomment to run real transfer")
    print("This will move ALL coins from FUND to UNIFIED account")


if __name__ == "__main__":
    test_transfer_all_to_unified()

