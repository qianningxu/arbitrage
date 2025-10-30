## Brief

- 监听一个币对 (`{X}/USDT`) 的 list，同时获取 **Bybit** 和 **Jupiter** 的汇率

| Bybit > Jupiter | Jupiter > Bybit |
|-----------------|-----------------|
| 在Jupiter买 | 在Bybit买 ❌ |
| 转账到Bybit | 转账到Jupiter |
| Bybit换成 **USDT** | Jupiter换成 **USDT** |

> 本次交易中，资金量约为 \$80（初始100，测试10，留10作为gas fee）。  
> 为了避免频繁提现造成的 withdrawal fee（Bybit有一个[固定的最低withdrawal fee](https://www.bybit.com/)，比如对于SOL是0.008），以上两种模式会交替进行。  
>
> 也就是说，每次都是 all in，然后所有资金量都会储存在一个交易所。此时，即使另一方出现价差，也并无法进行交易。


## 缺陷

1. **Bybit** 上的代币并没有直接提供 mint，只有名字。名字可能对应多个 mint（比如 `trump`）。我并没有找到简单的创建 1:1 代单的方式。考虑到这类占比大概只有 5%，就直接剔除了。



## 潜在改进

- 在 **Bybit** 和 **Jupiter** 上各自保留一部分资金，直接双边操作，无需跨平台转账。  
- 目前 CEX 基本上只是监控代币/USDT 的价格，可以研究下 CEX-CEX 的部分兑换方案。
