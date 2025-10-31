
def is_b2j_profitable(B, J, U, w, s_bybit):
    """
    Bybit → Jupiter 无亏损条件检查并计算预期利润
    
    公式: J ≥ B(1 + sᴮ) × 1.01 × (U + 0.001) / [(U - w) × 0.999]
    
    参数:
        B: Bybit上代币价格 (USDT/枚)
        J: Jupiter上代币价格 (USDT/枚)
        U: Bybit端初始USDT数量
        w: Bybit提币手续费 (USDT绝对值)
        s_bybit: Bybit端预期滑点，通过orderbook估算 (小数形式)
    
    返回:
        (profitable, expected_profit):
        - profitable: True表示满足套利条件，False表示不满足
        - expected_profit: 预期利润 (USDT)
    """
    s_jupiter = 0.002  # Jupiter 固定滑点 0.2% (B→J有延迟，设置更保守)
    gas = 0.001
    fee_bybit = 0.01
    
    # 计算预期利润
    tokens = (U - w) / (B * (1 + s_bybit) * (1 + fee_bybit))
    final_usdt = tokens * J * (1 - s_jupiter) - gas
    expected_profit = final_usdt - U
    
    # 判断是否盈利
    profitable = expected_profit >= 0
    
    return profitable, expected_profit


def get_b2j_max_slippage(J, B, U, w):
    """
    Bybit → Jupiter 滑点上限推导（盈亏平衡点）
    
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


def is_j2b_profitable(J, B, U, s_bybit):
    """
    Jupiter → Bybit 无亏损条件检查并计算预期利润
    
    公式: B ≥ J(1 + sᴶ) · U / [0.999(1 - sᴮ)(U - 0.002)]
    
    参数:
        J: Jupiter上代币价格 (USDT/枚)
        B: Bybit上代币价格 (USDT/枚)
        U: Jupiter端初始USDT数量
        s_bybit: Bybit端预期滑点，通过orderbook估算 (小数形式)
    
    返回:
        (profitable, expected_profit): 
        - profitable: True表示满足套利条件，False表示不满足
        - expected_profit: 预期利润 (USDT)
    """
    s_jupiter = 0.001  # Jupiter 固定滑点容忍度 0.1% (无法通过orderbook估算)
    gas = 0.002
    fee_bybit = 0.001
    
    # 计算预期利润
    tokens = (U - gas) / (J * (1 + s_jupiter))
    final_usdt = tokens * B * (1 - s_bybit) * (1 - fee_bybit)
    expected_profit = final_usdt - U
    
    # 判断是否盈利
    profitable = expected_profit >= 0
    
    return profitable, expected_profit


def get_j2b_max_slippage(B, J, U, s_bybit):
    """
    Jupiter → Bybit 滑点上限推导（盈亏平衡点）
    
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

