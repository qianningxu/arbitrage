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
from main.trade.bybit_swap import crypto_to_u, u_to_crypto


def test_crypto_to_u():
    """Test Scenario 1: Convert all crypto from FUND to USDT in UNIFIED
    
    After receiving SOL from Jupiter:
    1. Checks SOL balance in FUND
    2. Transfers all SOL from FUND → UNIFIED
    3. Swaps all available SOL in UNIFIED → USDT
    """
    result = crypto_to_u('SOL')
    print(f"✅ crypto_to_u completed - Order ID: {result['orderId']}")


def test_u_to_crypto():
    """Test Scenario 2: Convert all USDT to target crypto
    
    After crypto_to_u (all funds are now USDT):
    1. Checks USDT balance in UNIFIED
    2. Swaps all available USDT → SOL
    """
    result = u_to_crypto('SOL')
    print(f"✅ u_to_crypto completed - Order ID: {result['orderId']}")


if __name__ == "__main__":
    # Uncomment to test
    # test_crypto_to_u()
    # test_u_to_crypto()
    pass

