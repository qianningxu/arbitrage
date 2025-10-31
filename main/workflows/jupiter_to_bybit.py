"""
Jupiter → Bybit 套利条件计算

实现无亏损条件和Jupiter滑点上限推导公式
"""

def is_profitable(J, B, U, s_bybit):
    """
    无亏损条件检查
    
    公式: B ≥ J(1 + sᴶ) · U / [0.999(1 - sᴮ)(U - 0.002)]
    
    参数:
        J: Jupiter上代币价格 (USDT/枚)
        B: Bybit上代币价格 (USDT/枚)
        U: Jupiter端初始USDT数量
        s_bybit: Bybit端预期滑点，通过orderbook估算 (小数形式)
    
    返回:
        True表示满足套利条件，False表示不满足
    """
    s_jupiter = 0.001  # Jupiter 固定滑点容忍度 0.1% (无法通过orderbook估算)
    gas = 0.002
    fee_bybit = 0.001
    
    numerator = J * (1 + s_jupiter) * U
    denominator = (1 - fee_bybit) * (1 - s_bybit) * (U - gas)
    min_bybit_price = numerator / denominator
    
    return B >= min_bybit_price


def get_max_slippage(B, J, U, s_bybit):
    """
    Jupiter滑点上限推导（盈亏平衡点）
    
    公式: sᴶ_max = [0.999(1 - sᴮ)B(U - 0.002)] / (UJ) - 1
    
    说明: 计算在给定条件下，Jupiter最大可承受的滑点（盈亏平衡点）
    
    参数:
        B: Bybit上代币价格 (USDT/枚)
        J: Jupiter上代币价格 (USDT/枚)
        U: Jupiter端初始USDT数量
        s_bybit: Bybit端预期滑点 (小数形式)
    
    返回:
        Jupiter最大可承受滑点（盈亏平衡点）
    """
    gas = 0.002
    fee_bybit = 0.001
    
    numerator = (1 - fee_bybit) * (1 - s_bybit) * B * (U - gas)
    denominator = U * J
    
    return numerator / denominator - 1

