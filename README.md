# Multi-Factor Intraday Trading Strategy for US Equities

## Project Overview

Developed a multi-factor intraday quantitative trading strategy within an event-driven backtesting framework as part of the MAFS5140 Quantitative Finance course. The strategy operates on 5-minute bar data covering 439 US-listed equities, incorporating both closing prices and trading volumes to generate long-only portfolio allocations.

## Methodology

### Factor Design

The strategy integrates two academically validated alpha factors through a rank-based composite scoring system:

**Factor 1 — Cross-Sectional Short-Term Reversal (Weight: 0.70)**
Captures mean-reversion behavior over a 30-minute lookback window (6 bars). Stocks exhibiting the largest short-term price declines are ranked highest, reflecting the empirical finding that transient liquidity-driven price dislocations tend to revert. This effect is well-documented in the microstructure literature, where temporary price concessions by liquidity providers create predictable reversals (Jegadeesh, 1990; Da, Liu & Schaumburg, 2014).

**Factor 2 — Intraday Momentum (Weight: 0.30)**
Captures trend continuation over a 2-hour lookback window (24 bars). Stocks with the strongest positive intraday trends are ranked highest. Gao, Han, Li & Zhou (2018) demonstrate that early-session returns significantly predict late-session returns, with the effect being stronger on high-volatility and high-volume days.

### Signal Construction and Portfolio Allocation

At each 5-minute interval, the strategy computes percentile ranks for both factors across all 439 stocks, eliminating scale differences and ensuring robustness to outliers. The weighted composite score (0.7 × reversal rank + 0.3 × momentum rank) determines stock selection. The top 30 stocks by composite score receive equal-weight allocation (3.33% each), with the portfolio fully invested (weights sum to 1.0), strictly adhering to long-only and no-leverage constraints.

### Parameter Optimization

Factor weights were determined through a systematic grid search over 66 combinations (step size = 0.1, subject to weights summing to 1.0). The optimal configuration (Reversal = 0.7, Momentum = 0.3, Volume = 0.0) was selected based on the Sharpe Ratio evaluated on the validation dataset.

## Results

| Metric | Validation Set | Training Set |
| --- | --- | --- |
| Cumulative Return | 8.15% | 57,071.94% |
| Annualized Return | 180.66% | 101.29% |
| Annualized Volatility | 18.5% | 20.12% |
| Sharpe Ratio | 33.69 | 5.03 |
| Max Drawdown | -1.71% | -27.59% |

Note: Results are gross of transaction costs. The high annualized figures reflect the compounding effect across approximately 19,600 five-minute bars per year (252 days × 78 bars/day). In practice, frequent rebalancing would incur significant execution costs.

## Technical Implementation

Built entirely in Python using Pandas and NumPy, with memory-efficient data structures (collections.deque) for real-time rolling-window computation. The modular design separates strategy logic from the backtesting engine, data feed, and performance evaluation components.

## References

- Jegadeesh, N. (1990). "Evidence of Predictable Behavior of Security Returns." *Journal of Finance*, 45(3), 881–898.
- Da, Z., Liu, Q., & Schaumburg, E. (2014). "A Closer Look at the Short-Term Return Reversal." *Management Science*, 60(3), 658–674.
- Gao, L., Han, Y., Li, S. Z., & Zhou, G. (2018). "Market Intraday Momentum." *Journal of Financial Economics*, 129(2), 394–414.
- Campbell, J. Y., Grossman, S. J., & Wang, J. (1993). "Trading Volume and Serial Correlation in Stock Returns." *Quarterly Journal of Economics*, 108(4), 905–939.
