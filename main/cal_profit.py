
def calculate_fees(trade_amount_usd):
    bybit_fee = trade_amount_usd * 0.001  # 0.1%
    jupiter_fee = trade_amount_usd * 0.0025  # 0.25%
    gas_fee = 0.002  # ~$0.002 in SOL
    slippage = trade_amount_usd * 0.005  # 0.5%
    
    total = bybit_fee + jupiter_fee + gas_fee + slippage
    return total


def calculate_profit(buy_price, sell_price, trade_amount_usd):
    units = trade_amount_usd / buy_price
    gross_profit = (sell_price - buy_price) * units
    total_fees = calculate_fees(trade_amount_usd)
    net_profit = gross_profit - total_fees
    
    return net_profit