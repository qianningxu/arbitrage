"""Test get_jupiter_price functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.jupiter.monitor.pricing import get_exchange_rate, get_quote
from main.shared.data import get_token_info


def test_get_exchange_rate(from_symbol, to_symbol, amount):
    """Get exchange rate with debugging"""
    print(f"\n=== Testing {from_symbol}->{to_symbol} ===")
    
    input_info = get_token_info(from_symbol)
    output_info = get_token_info(to_symbol)
    print(f"Input token info: {input_info}")
    print(f"Output token info: {output_info}")
    
    if input_info and output_info:
        amount_lamports = int(amount * (10 ** input_info["decimals"]))
        print(f"Amount in lamports: {amount_lamports}")
        
        quote = get_quote(input_info["mint"], output_info["mint"], amount_lamports)
        print(f"Quote response: {quote}")
    
    rate = get_exchange_rate(from_symbol, to_symbol, amount)
    print(f"Exchange rate: {rate}")
    return rate


if __name__ == "__main__":
    test_get_exchange_rate("GRASS", "USDT", 1)
    
