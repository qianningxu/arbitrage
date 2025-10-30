# 目录结构说明

## 核心功能模块 (main/)

```
main/
├── Bybit/                              # Bybit 交易所相关操作
│   ├── helper/                         # 辅助工具模块
│   │   └── auth.py                     # API 认证与请求签名（生成签名、创建请求头）
│   ├── monitor/                        # 市场监控模块
│   │   └── pricing.py                  # 获取订单簿、价格、计算买卖均价和价差
│   └── account/                        # 账户操作模块
│       ├── balance.py                  # 查询 FUND/UNIFIED 账户余额
│       ├── swap.py                     # 现货交易（市价买卖、币种互换）
│       └── transfers.py                # 内部划转、充值地址查询、提币操作
│
├── Jupiter/                            # Jupiter 聚合器 / Solana 链上操作
│   ├── helper/                         # 辅助工具模块
│   │   └── client.py                   # Solana RPC 客户端、钱包密钥管理
│   ├── monitor/                        # 市场监控模块
│   │   └── pricing.py                  # 获取 Jupiter 报价、计算交易汇率
│   └── account/                        # 账户操作模块
│       ├── balance.py                  # 查询 SOL 和 SPL 代币余额
│       ├── swap.py                     # 通过 Jupiter 执行链上代币兑换
│       └── transfers.py                # 发送 SOL 和 SPL 代币、提币到 Bybit
│
├── shared/                             # 跨平台共享工具
│   ├── config.py                       # 环境变量读取、密钥对加载（Solana、Bybit）
│   └── data.py                         # 加载代币元数据、交易对信息、提币手续费数据
│
└── workflows/                          # 跨平台业务流程
    ├── arbitrage/                      # 套利策略相关
    │   ├── detector.py                 # 检测套利机会（计算路径 A/B 利润）
    │   ├── executor.py                 # 执行套利策略（检测资金位置、自动执行）
    │   └── consolidate.py              # 资金归集（归集到 Bybit/Solana，统一换成 USDT）
    └── transfers/                      # 跨平台转账
        └── bridge.py                   # Bybit ↔ Jupiter 之间的资金转移
```

## 测试模块 (test/)

测试目录完全镜像 main/ 的结构，每个功能模块都有对应的测试文件。

```
test/
├── Bybit/                              # Bybit 模块测试
│   ├── helper/                         # 辅助工具测试
│   │   ├── test_auth.py                # 测试 API 签名和认证功能
│   │   ├── test_info.py                # 测试获取交易对信息
│   │   ├── test_min_order.py           # 测试最小订单量计算
│   │   └── test_transfer.py            # 测试内部划转功能
│   ├── monitor/                        # 市场监控测试
│   │   └── test_pricing.py             # 测试订单簿、买卖价格、价差计算
│   └── account/                        # 账户操作测试
│       ├── test_balance.py             # 测试余额查询功能
│       ├── test_swap.py                # 测试现货交易功能
│       └── test_withdraw.py            # 测试提币功能
│
├── Jupiter/                            # Jupiter 模块测试
│   ├── helper/                         # 辅助工具测试
│   │   ├── test_get_id_from_pairs.py   # 测试交易对到代币地址的转换
│   │   ├── test_quote.py               # 测试 Jupiter 报价 API（完整响应）
│   │   └── test_quote_fees.py          # 测试报价手续费分析（详细费用拆解）
│   ├── monitor/                        # 市场监控测试
│   │   └── test_pricing.py             # 测试汇率查询和价格对比功能
│   └── account/                        # 账户操作测试
│       ├── test_balance.py             # 测试链上余额查询
│       ├── test_swap.py                # 测试链上代币兑换
│       └── test_withdraw.py            # 测试从 Solana 提币到 Bybit
│
└── workflow/                           # 业务流程测试
    ├── test_arbitrage_strategy.py      # 测试套利策略检测和执行
    ├── test_bybit_to_jupiter.py        # 测试 Bybit → Jupiter 转账流程
    └── test_jupiter_to_bybit.py        # 测试 Jupiter → Bybit 转账流程
```

## 文件组织原则

- **helper/** - 基础工具和辅助功能（认证、客户端、工具函数）
- **monitor/** - 市场数据监控和价格查询（不涉及交易）
- **account/** - 账户相关操作（余额、交易、转账）
- **shared/** - 跨平台共享的配置和数据
- **workflows/** - 组合多个模块实现的复杂业务流程
