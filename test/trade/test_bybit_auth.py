"""Test bybit_auth functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.platforms.bybit.api.auth import sign_request


def test_sign_request():
    """Test sign_request function"""
    headers = sign_request("test_param_string")
    print("Generated headers:")
    print(f"  API Key: {headers.get('X-BAPI-API-KEY')[:10]}...")
    print(f"  Signature: {headers.get('X-BAPI-SIGN')[:10]}...")
    print(f"  Timestamp: {headers.get('X-BAPI-TIMESTAMP')}")


if __name__ == "__main__":
    test_sign_request()

