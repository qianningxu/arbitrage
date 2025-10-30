"""
Simple demo test for bybit swap scenarios

Scenario 1 (crypto_to_u): Jupiter → Bybit
- Crypto just arrived from Jupiter in FUND account
- Transfer all crypto from FUND → UNIFIED
- Swap all available crypto in UNIFIED → USDT

Scenario 2 (u_to_crypto): Bybit Trading
- All funds are USDT in UNIFIED (after Scenario 1)
- Swap all available USDT → target crypto
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.account.swap import crypto_to_u, u_to_crypto, place_limit_order


def test_crypto_to_u(symbol):
    """Test Scenario 1: Convert all crypto from FUND to USDT in UNIFIED
    
    After receiving crypto from Jupiter:
    1. Checks crypto balance in FUND
    2. Transfers all crypto from FUND → UNIFIED
    3. Swaps all available crypto in UNIFIED → USDT (market order)
    """
    result = crypto_to_u(symbol)
    print(f"✅ crypto_to_u completed - Order ID: {result['orderId']}")


def test_u_to_crypto(symbol, price):
    """Test Scenario 2: Convert all USDT to target crypto at specified price
    
    After crypto_to_u (all funds are now USDT):
    1. Checks USDT balance in UNIFIED
    2. Places limit order (IOC) to buy target crypto at specified price
    """
    result = u_to_crypto(symbol, price)
    if result.get("status") == "success":
        print(f"✅ u_to_crypto completed - Order ID: {result['orderId']}")
    else:
        print(f"❌ u_to_crypto failed - {result.get('retMsg')}")


def test_limit_order(symbol, side, qty, price, time_in_force="GTC"):
    """Test placing a limit order
    
    Args:
        symbol: Trading pair (e.g., SOLUSDT)
        side: Buy or Sell
        qty: Quantity to trade
        price: Limit price
        time_in_force: GTC, IOC, FOK, or PostOnly
    """
    result = place_limit_order(symbol, side, qty, price, time_in_force)
    if result.get("status") == "success":
        print(f"✅ Limit order placed - Order ID: {result['orderId']}")
    else:
        print(f"❌ Limit order failed/cancelled - {result.get('retMsg')}")


if __name__ == "__main__":
    # === Main workflow tests ===
    # test_crypto_to_u('SOL')  # Convert all SOL from FUND to USDT
    
    # Test scenario: IOC order that should be cancelled (need sufficient USDT balance first)
    # If you have enough USDT (e.g., >$10), uncomment below to see IOC cancellation:
    test_u_to_crypto('SOL', 10.0)  # Buy at $10 (far below market ~$150-200), IOC will cancel
