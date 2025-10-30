"""Test jupiter_helpers functions"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.jupiter.monitor.pricing import get_quote


def test_get_jupiter_quote(from_mint, to_mint, amount):
    """Get Jupiter quote for swap and display full response"""
    print(f"\n{'='*60}")
    print(f"Testing Jupiter Quote API")
    print(f"{'='*60}")
    print(f"Input: {from_mint}")
    print(f"Output: {to_mint}")
    print(f"Amount: {amount} lamports")
    print(f"{'='*60}\n")
    
    quote = get_quote(from_mint, to_mint, amount)
    if quote:
        print("✅ Quote received successfully!\n")
        print(json.dumps(quote, indent=2))
        
        # Extract key information
        print(f"\n{'='*60}")
        print("Key Information:")
        print(f"{'='*60}")
        print(f"In Amount: {quote.get('inAmount')}")
        print(f"Out Amount: {quote.get('outAmount')}")
        print(f"Price Impact: {quote.get('priceImpactPct', 'N/A')}%")
        
        # Platform fee
        if 'platformFee' in quote and quote['platformFee']:
            print(f"\nPlatform Fee:")
            print(f"  Amount: {quote['platformFee'].get('amount', 'N/A')}")
            print(f"  Fee BPS: {quote['platformFee'].get('feeBps', 'N/A')}")
        else:
            print(f"\nPlatform Fee: None")
        
        # Route plan with LP fees
        if 'routePlan' in quote:
            print(f"\nRoute Plan ({len(quote['routePlan'])} steps):")
            for i, route in enumerate(quote['routePlan']):
                swap_info = route.get('swapInfo', {})
                print(f"\n  Step {i+1}:")
                print(f"    DEX: {swap_info.get('label', 'N/A')}")
                print(f"    In Amount: {swap_info.get('inAmount', 'N/A')}")
                print(f"    Out Amount: {swap_info.get('outAmount', 'N/A')}")
                print(f"    Fee Amount: {swap_info.get('feeAmount', 'N/A')}")
                print(f"    Fee Mint: {swap_info.get('feeMint', 'N/A')}")
                print(f"    Fee PCT: {swap_info.get('feePct', 'N/A')}")
    else:
        print("❌ Failed to get quote")


if __name__ == "__main__":
    sol_mint = "So11111111111111111111111111111111111111112"
    usdt_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    
    print("\n" + "="*60)
    print("Test 1: SOL -> USDT (0.1 SOL)")
    print("="*60)
    test_get_jupiter_quote(sol_mint, usdt_mint, 100000000)  # 0.1 SOL
    
    print("\n\n" + "="*60)
    print("Test 2: SOL -> USDC (1 SOL)")
    print("="*60)
    test_get_jupiter_quote(sol_mint, usdc_mint, 1000000000)  # 1 SOL

