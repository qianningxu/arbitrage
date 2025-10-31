"""
Bybit → Jupiter 套利条件计算

实现无亏损条件和Bybit滑点上限推导公式
"""

def is_profitable(B, J, U, w, s_bybit):
    """
    无亏损条件检查
    
    公式: J ≥ B(1 + sᴮ) × 1.01 × (U + 0.001) / [(U - w) × 0.999]
    
    参数:
        B: Bybit上代币价格 (USDT/枚)
        J: Jupiter上代币价格 (USDT/枚)
        U: Bybit端初始USDT数量
        w: Bybit提币手续费 (USDT绝对值)
        s_bybit: Bybit端预期滑点，通过orderbook估算 (小数形式)
    
    返回:
        True表示满足套利条件，False表示不满足
    """
    s_jupiter = 0.002  # Jupiter 固定滑点 0.2% (B→J有延迟，设置更保守)
    gas = 0.001
    fee_bybit = 0.01
    
    numerator = B * (1 + s_bybit) * (1 + fee_bybit) * (U + gas)
    denominator = (U - w) * (1 - s_jupiter)
    min_jupiter_price = numerator / denominator
    
    return J >= min_jupiter_price


def get_max_slippage(J, B, U, w):
    """
    Bybit滑点上限推导（盈亏平衡点）
    
    公式: sᴮ_max = [J × 0.998 × (U - w)] / [B × 1.01 × (U + 0.001)] - 1
    
    说明: 计算在给定条件下，Bybit最大可承受的滑点（盈亏平衡点）
    
    参数:
        J: Jupiter上代币价格 (USDT/枚)
        B: Bybit上代币价格 (USDT/枚)
        U: Bybit端初始USDT数量
        w: Bybit提币手续费 (USDT绝对值)
    
    返回:
        Bybit最大可承受滑点（盈亏平衡点）
    """
    gas = 0.001
    fee_bybit = 0.01
    s_jupiter = 0.002  # Jupiter 固定滑点 0.2% (B→J有延迟，设置更保守)
    
    numerator = J * (1 - s_jupiter) * (U - w)
    denominator = B * (1 + fee_bybit) * (U + gas)
    
    return numerator / denominator - 1

