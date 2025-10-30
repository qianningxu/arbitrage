"""
Jupiter → Bybit 套利条件计算

实现无亏损条件和Jupiter滑点上限推导公式
"""

def is_profitable(J, B, s_jupiter, U, s_bybit):
    """
    无亏损条件检查
    
    公式: B ≥ J(1 + sᴶ) · U / [0.999(1 - sᴮ)(U - 0.002)]
    
    参数:
        J: Jupiter上代币价格 (USDT/枚)
        B: Bybit上代币价格 (USDT/枚)
        s_jupiter: Jupiter端滑点容忍度 (小数形式)
        U: Jupiter端初始USDT数量
        s_bybit: Bybit端预期滑点 (小数形式)
    
    返回:
        True表示满足套利条件，False表示不满足
    """
    gas = 0.002
    fee_bybit = 0.001
    
    numerator = J * (1 + s_jupiter) * U
    denominator = (1 - fee_bybit) * (1 - s_bybit) * (U - gas)
    min_bybit_price = numerator / denominator
    
    return B >= min_bybit_price


def get_max_slippage(B, J, U, s_bybit):
    """
    Jupiter滑点上限推导
    
    公式: sᴶ_max = [0.999(1 - sᴮ)B(U - 0.002)] / (UJ) - 1
    
    参数:
        B: Bybit上代币价格 (USDT/枚)
        J: Jupiter上代币价格 (USDT/枚)
        U: Jupiter端初始USDT数量
        s_bybit: Bybit端预期滑点 (小数形式)
    
    返回:
        Jupiter最大可承受滑点
    """
    gas = 0.002
    fee_bybit = 0.001
    
    numerator = (1 - fee_bybit) * (1 - s_bybit) * B * (U - gas)
    denominator = U * J
    
    return numerator / denominator - 1

