"""
Solana/Jupiter pricing services
"""
from main.core.data_loader import get_token_info
from main.core.converters import bybit_symbol_to_mints
from ..api.jupiter_api import get_quote


def get_exchange_rate(input_symbol: str, output_symbol: str, amount: float) -> float:
    """Get exchange rate between two tokens via Jupiter
    
    Args:
        input_symbol: Input token symbol
        output_symbol: Output token symbol
        amount: Amount in input token units
        
    Returns:
        float or None: Exchange rate (output/input)
    """
    input_info = get_token_info(input_symbol)
    output_info = get_token_info(output_symbol)
    
    if not input_info or not output_info:
        return None
    
    input_mint = input_info["mint"]
    output_mint = output_info["mint"]
    input_decimals = input_info["decimals"]
    output_decimals = output_info["decimals"]
    
    # Get quote
    amount_lamports = int(amount * (10 ** input_decimals))
    quote = get_quote(input_mint, output_mint, amount_lamports)
    
    if not quote:
        return None
    
    in_amt = quote.get("inAmount")
    out_amt = quote.get("outAmount")
    
    if not in_amt or not out_amt:
        return None
    
    # Calculate rate (outAmount already includes LP/DEX fees)
    return (float(out_amt) / (10 ** output_decimals)) / (float(in_amt) / (10 ** input_decimals))


def get_price_from_bybit_symbol(symbol: str) -> float:
    """Get Jupiter price using Bybit trading pair symbol
    
    Args:
        symbol: Bybit trading pair symbol (e.g., 'SOLUSDT')
        
    Returns:
        float or None: Exchange rate
    """
    mints = bybit_symbol_to_mints(symbol)
    if not mints:
        return None
    
    base_mint, quote_mint = mints
    tokens = load_tokens()
    
    # Find symbols for mints
    input_symbol = None
    output_symbol = None
    
    for sym, data in tokens.items():
        if data and len(data) > 0:
            mint = data[0].get("mint")
            if mint == base_mint:
                input_symbol = sym
            if mint == quote_mint:
                output_symbol = sym
            if input_symbol and output_symbol:
                break
    
    if not input_symbol or not output_symbol:
        return None
    
    return get_exchange_rate(input_symbol, output_symbol, 1)

