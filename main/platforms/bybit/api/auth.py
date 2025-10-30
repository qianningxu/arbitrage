"""
Bybit API authentication
"""
import time
import hmac
import hashlib
from main.core.config import get_bybit_credentials


def sign_request(param_str: str) -> dict:
    """Create signature headers for Bybit API request
    
    Args:
        param_str: Parameter string to sign
        
    Returns:
        dict: Headers with signature
    """
    api_key, api_secret = get_bybit_credentials()
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    return {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "Content-Type": "application/json"
    }


def create_headers(params: dict = None) -> dict:
    """Create authenticated headers for Bybit API
    
    Args:
        params: Optional parameters to sign
        
    Returns:
        dict: Request headers
    """
    if params:
        import json
        param_str = json.dumps(params) if isinstance(params, dict) else str(params)
        return sign_request(param_str)
    return sign_request("")

