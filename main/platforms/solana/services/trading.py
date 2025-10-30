"""
Solana/Jupiter trading services
"""
from main.core.data_loader import get_token_info
from ..api.jupiter_api import get_quote, execute_swap, get_recent_priority_fees


def swap(input_symbol: str, output_symbol: str, amount: float, slippage_bps: int = 50, auto_priority_fee: bool = True) -> str:
    """Swap tokens via Jupiter
    
    Args:
        input_symbol: Input token symbol
        output_symbol: Output token symbol
        amount: Amount in input token units
        slippage_bps: Slippage tolerance in basis points (default: 50 = 0.5%)
        auto_priority_fee: Automatically set priority fee based on recent fees
        
    Returns:
        str: Transaction signature
        
    Raises:
        ValueError: If tokens not found or quote fails
    """
    input_info = get_token_info(input_symbol)
    output_info = get_token_info(output_symbol)
    
    if not input_info:
        raise ValueError(f"Input token not found: {input_symbol}")
    if not output_info:
        raise ValueError(f"Output token not found: {output_symbol}")
    
    input_mint = input_info["mint"]
    output_mint = output_info["mint"]
    amount_lamports = int(amount * (10 ** input_info["decimals"]))
    
    # Get quote
    quote = get_quote(input_mint, output_mint, amount_lamports, slippage_bps)
    if not quote:
        raise ValueError("Failed to get quote from Jupiter")
    
    print(f"🔄 Swapping {input_symbol} → {output_symbol}: {amount}")
    
    # Determine priority fee
    priority_fee = None
    if auto_priority_fee:
        fees = get_recent_priority_fees()
        priority_fee = fees["p75"]  # Use 75th percentile
        if priority_fee > 0:
            print(f"⚡ Priority fee: {priority_fee} lamports")
    
    # Execute swap
    return execute_swap(quote, priority_fee)


def trade(input_symbol: str, output_symbol: str, amount: float) -> str:
    """High-level trade function (alias for swap with default settings)
    
    Args:
        input_symbol: Input token symbol
        output_symbol: Output token symbol
        amount: Amount in input token units
        
    Returns:
        str: Transaction signature
    """
    return swap(input_symbol, output_symbol, amount)

