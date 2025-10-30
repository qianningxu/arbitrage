"""
Bybit → Jupiter 套利条件计算

实现无亏损条件和Bybit滑点上限推导公式
"""

def is_profitable(B, J, s_bybit, U, w):
    """
    无亏损条件检查
    
    公式: J ≥ B(1 + sᴮ) × 1.01 × (U + 0.001) / [(U - w) × 0.999]
    
    参数:
        B: Bybit上代币价格 (USDT/枚)
        J: Jupiter上代币价格 (USDT/枚)
        s_bybit: Bybit端滑点容忍度 (小数形式)
        U: Bybit端初始USDT数量
        w: Bybit提币手续费 (USDT绝对值)
    
    返回:
        True表示满足套利条件，False表示不满足
    """
    gas = 0.001
    fee_bybit = 0.01
    s_jupiter = 0.001
    
    numerator = B * (1 + s_bybit) * (1 + fee_bybit) * (U + gas)
    denominator = (U - w) * (1 - s_jupiter)
    min_jupiter_price = numerator / denominator
    
    return J >= min_jupiter_price


def get_max_slippage(J, B, U, w):
    """
    Bybit滑点上限推导
    
    公式: sᴮ_max = [J × 0.999 × (U - w)] / [B × 1.01 × (U + 0.001)] - 1
    
    参数:
        J: Jupiter上代币价格 (USDT/枚)
        B: Bybit上代币价格 (USDT/枚)
        U: Bybit端初始USDT数量
        w: Bybit提币手续费 (USDT绝对值)
    
    返回:
        Bybit最大可承受滑点
    """
    gas = 0.001
    fee_bybit = 0.01
    s_jupiter = 0.001
    
    numerator = J * (1 - s_jupiter) * (U - w)
    denominator = B * (1 + fee_bybit) * (U + gas)
    
    return numerator / denominator - 1

