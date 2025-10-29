"""Test bybit_auth functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.bybit_auth import sign_request


def test_sign_request():
    """Generate signed headers for API request"""
    headers = sign_request("accountType=SPOT")
    print(f"Generated headers with signature: {headers['X-BAPI-SIGN'][:10]}...")


if __name__ == "__main__":
    test_sign_request()

