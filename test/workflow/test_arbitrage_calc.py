"""
测试双向套利条件计算 (Bybit ↔ Jupiter)
"""
import sys
sys.path.append('/Users/side/Desktop/arbitrage')

from main.workflows.arbitrage_calc import (
    is_b2j_profitable, get_b2j_max_slippage,
    is_j2b_profitable, get_j2b_max_slippage
)

def test_b2j_profitable():
    """测试 Bybit → Jupiter 盈利性判断"""
    print("=" * 60)
    print("Bybit → Jupiter 套利条件测试")
    print("=" * 60)
    print()
    
    # 测试用例1: 明显盈利的情况
    B = 1.0
    J = 1.05
    s_bybit = 0.005
    U = 100
    w = 0.5
    
    profitable, profit = is_b2j_profitable(B, J, U, w, s_bybit)
    print(f"测试1 - 盈利情况:")
    print(f"  B={B}, J={J}, U={U}, w={w}, s_bybit={s_bybit}")
    print(f"  结果: {profitable} (期望 True), 预期利润: ${profit:.4f} USDT")
    print()
    
    # 测试用例2: 明显亏损的情况
    B = 1.0
    J = 0.95
    profitable2, profit2 = is_b2j_profitable(B, J, U, w, s_bybit)
    print(f"测试2 - 亏损情况:")
    print(f"  B={B}, J={J}, U={U}, w={w}, s_bybit={s_bybit}")
    print(f"  结果: {profitable2} (期望 False), 预期利润: ${profit2:.4f} USDT")
    print()
    
    # 测试用例3: 临界情况
    B = 1.0
    J = 1.02
    profitable3, profit3 = is_b2j_profitable(B, J, U, w, s_bybit)
    print(f"测试3 - 临界情况:")
    print(f"  B={B}, J={J}, U={U}, w={w}, s_bybit={s_bybit}")
    print(f"  结果: {profitable3}, 预期利润: ${profit3:.4f} USDT")
    print()

def test_b2j_max_slippage():
    """测试 Bybit → Jupiter 最大滑点计算"""
    J = 1.05
    B = 1.0
    U = 100
    w = 0.5
    
    max_slip = get_b2j_max_slippage(J, B, U, w)
    print(f"测试 Bybit 最大滑点:")
    print(f"  J={J}, B={B}, U={U}, w={w}")
    print(f"  最大可承受滑点: {max_slip:.4f} ({max_slip*100:.2f}%)")
    print()
    
    # 验证：使用这个最大滑点应该刚好盈亏平衡
    profitable, profit = is_b2j_profitable(B, J, U, w, max_slip)
    print(f"  使用最大滑点验证: {profitable} (应该接近 True), 预期利润: ${profit:.4f} USDT")
    print()

def test_j2b_profitable():
    """测试 Jupiter → Bybit 盈利性判断"""
    print("=" * 60)
    print("Jupiter → Bybit 套利条件测试")
    print("=" * 60)
    print()
    
    # 测试用例1: 明显盈利的情况
    J = 1.0
    B = 1.05
    U = 100
    s_bybit = 0.001
    
    profitable, profit = is_j2b_profitable(J, B, U, s_bybit)
    print(f"测试1 - 盈利情况:")
    print(f"  J={J}, B={B}, U={U}, s_bybit={s_bybit}")
    print(f"  结果: {profitable} (期望 True), 预期利润: ${profit:.4f} USDT")
    print()
    
    # 测试用例2: 明显亏损的情况
    J = 1.0
    B = 0.95
    profitable2, profit2 = is_j2b_profitable(J, B, U, s_bybit)
    print(f"测试2 - 亏损情况:")
    print(f"  J={J}, B={B}, U={U}, s_bybit={s_bybit}")
    print(f"  结果: {profitable2} (期望 False), 预期利润: ${profit2:.4f} USDT")
    print()
    
    # 测试用例3: 临界情况
    J = 1.0
    B = 1.008
    profitable3, profit3 = is_j2b_profitable(J, B, U, s_bybit)
    print(f"测试3 - 临界情况:")
    print(f"  J={J}, B={B}, U={U}, s_bybit={s_bybit}")
    print(f"  结果: {profitable3}, 预期利润: ${profit3:.4f} USDT")
    print()

def test_j2b_max_slippage():
    """测试 Jupiter → Bybit 最大滑点计算"""
    B = 1.05
    J = 1.0
    U = 100
    s_bybit = 0.001
    
    max_slip = get_j2b_max_slippage(B, J, U, s_bybit)
    print(f"测试 Jupiter 最大滑点:")
    print(f"  B={B}, J={J}, U={U}, s_bybit={s_bybit}")
    print(f"  最大可承受滑点: {max_slip:.4f} ({max_slip*100:.2f}%)")
    print(f"  说明: 这是在盈亏平衡点时Jupiter能承受的最大滑点")
    print()

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("双向套利条件计算测试")
    print("=" * 60)
    print()
    
    test_b2j_profitable()
    test_b2j_max_slippage()
    print()
    test_j2b_profitable()
    test_j2b_max_slippage()

