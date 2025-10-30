"""
测试 Jupiter → Bybit 套利条件计算
"""
import sys
sys.path.append('/Users/side/Desktop/arbitrage')

from main.workflows.jupiter_to_bybit import is_profitable, get_max_slippage

def test_is_profitable():
    # 测试用例1: 明显盈利的情况
    J = 1.0  # Jupiter 价格 1 USDT
    B = 1.05  # Bybit 价格 1.05 USDT (高5%)
    s_jupiter = 0.005  # Jupiter 滑点 0.5%
    U = 100  # 投入 100 USDT
    s_bybit = 0.001  # Bybit 滑点 0.1%
    
    result = is_profitable(J, B, s_jupiter, U, s_bybit)
    print(f"测试1 - 盈利情况:")
    print(f"  J={J}, B={B}, s_jupiter={s_jupiter}, U={U}, s_bybit={s_bybit}")
    print(f"  结果: {result} (期望 True)")
    print()
    
    # 测试用例2: 明显亏损的情况
    J = 1.0
    B = 0.95  # Bybit 价格更低，肯定亏损
    result2 = is_profitable(J, B, s_jupiter, U, s_bybit)
    print(f"测试2 - 亏损情况:")
    print(f"  J={J}, B={B}, s_jupiter={s_jupiter}, U={U}, s_bybit={s_bybit}")
    print(f"  结果: {result2} (期望 False)")
    print()
    
    # 测试用例3: 临界情况
    J = 1.0
    B = 1.008  # 接近临界点
    result3 = is_profitable(J, B, s_jupiter, U, s_bybit)
    print(f"测试3 - 临界情况:")
    print(f"  J={J}, B={B}, s_jupiter={s_jupiter}, U={U}, s_bybit={s_bybit}")
    print(f"  结果: {result3}")
    print()

def test_get_max_slippage():
    # 测试滑点上限计算
    B = 1.05
    J = 1.0
    U = 100
    s_bybit = 0.001
    
    max_slip = get_max_slippage(B, J, U, s_bybit)
    print(f"测试 Jupiter 最大滑点:")
    print(f"  B={B}, J={J}, U={U}, s_bybit={s_bybit}")
    print(f"  最大可承受滑点: {max_slip:.4f} ({max_slip*100:.2f}%)")
    print()
    
    # 验证：使用这个最大滑点应该刚好盈亏平衡
    result = is_profitable(J, B, max_slip, U, s_bybit)
    print(f"  使用最大滑点验证: {result} (应该接近 True)")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Jupiter → Bybit 套利条件计算测试")
    print("=" * 50)
    print()
    
    test_is_profitable()
    test_get_max_slippage()

