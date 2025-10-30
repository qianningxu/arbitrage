"""Analyze Jupiter quote fees in detail"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.Jupiter.monitor.pricing import get_quote


def analyze_quote_fees(input_mint, output_mint, amount, label=""):
    """Analyze fees from Jupiter quote"""
    print(f"\n{'='*70}")
    print(f"Analyzing: {label}")
    print(f"{'='*70}")
    
    quote = get_quote(input_mint, output_mint, amount)
    if not quote:
        print("❌ Failed to get quote")
        return
    
    in_amount = int(quote['inAmount'])
    out_amount = int(quote['outAmount'])
    
    print(f"Input Amount:  {in_amount:,} lamports")
    print(f"Output Amount: {out_amount:,} lamports")
    print(f"Price Impact:  {quote.get('priceImpactPct', 0)}%")
    
    # Calculate implicit rate
    rate = out_amount / in_amount
    print(f"Exchange Rate: {rate:.10f}")
    
    # Platform fee
    platform_fee = quote.get('platformFee')
    if platform_fee:
        print(f"\n💰 Platform Fee:")
        print(f"   Amount: {platform_fee.get('amount')} lamports")
        print(f"   BPS: {platform_fee.get('feeBps')} ({platform_fee.get('feeBps')/100:.2f}%)")
    
    # Route analysis
    route_plan = quote.get('routePlan', [])
    print(f"\n🛤️  Route Plan: {len(route_plan)} step(s)")
    
    total_explicit_fees = 0
    for i, route in enumerate(route_plan):
        swap_info = route.get('swapInfo', {})
        fee_amount = int(swap_info.get('feeAmount', 0))
        total_explicit_fees += fee_amount
        
        print(f"\n   Step {i+1}: {swap_info.get('label', 'Unknown')}")
        print(f"   └─ In:  {int(swap_info.get('inAmount', 0)):,} lamports")
        print(f"   └─ Out: {int(swap_info.get('outAmount', 0)):,} lamports")
        print(f"   └─ Fee: {fee_amount:,} lamports ({swap_info.get('feeMint', 'Unknown')[:8]}...)")
        
        # Calculate step loss
        step_in = int(swap_info.get('inAmount', 0))
        step_out = int(swap_info.get('outAmount', 0))
        if i == 0:
            # First step uses SOL
            step_loss = step_in - step_out - fee_amount
            loss_pct = (step_loss / step_in * 100) if step_in > 0 else 0
            print(f"   └─ Implicit cost: {step_loss:,} lamports ({loss_pct:.4f}%)")
    
    print(f"\n📊 Summary:")
    print(f"   Explicit Fees: {total_explicit_fees:,} lamports")
    
    # Calculate total cost (assuming we're converting from SOL)
    # The difference between in and out represents total cost
    total_cost_lamports = in_amount - (out_amount * in_amount / out_amount)
    print(f"   Total Cost (implicit): based on exchange rate difference")
    
    # Estimate fee percentage
    if in_amount > 0:
        # For SOL to stablecoin, assume rough price of $180 per SOL
        # and $1 per stablecoin (with 6 decimals for USDC/USDT)
        assumed_sol_price = 180
        expected_out_exact = (in_amount / 1e9) * assumed_sol_price * 1e6
        actual_out = out_amount
        loss = expected_out_exact - actual_out
        loss_pct = (loss / expected_out_exact * 100) if expected_out_exact > 0 else 0
        print(f"   Estimated total loss vs spot: {loss:.2f} ({loss_pct:.4f}%)")


if __name__ == "__main__":
    sol_mint = "So11111111111111111111111111111111111111112"
    usdt_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    
    # Test different amounts
    analyze_quote_fees(sol_mint, usdc_mint, 100000000, "0.1 SOL -> USDC")
    analyze_quote_fees(sol_mint, usdc_mint, 1000000000, "1.0 SOL -> USDC")
    analyze_quote_fees(sol_mint, usdc_mint, 10000000000, "10 SOL -> USDC")
    analyze_quote_fees(sol_mint, usdt_mint, 1000000000, "1.0 SOL -> USDT")

