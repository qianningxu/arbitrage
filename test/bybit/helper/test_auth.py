"""Test bybit_auth functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.helper.auth import sign_request


def test_sign_request(param_string):
    """Test sign_request function"""
    headers = sign_request(param_string)
    print("Generated headers:")
    print(f"  API Key: {headers.get('X-BAPI-API-KEY')[:10]}...")
    print(f"  Signature: {headers.get('X-BAPI-SIGN')[:10]}...")
    print(f"  Timestamp: {headers.get('X-BAPI-TIMESTAMP')}")


if __name__ == "__main__":
    test_sign_request("test_param_string")

