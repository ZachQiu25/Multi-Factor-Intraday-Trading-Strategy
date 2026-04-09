import pandas as pd
import numpy as np
from collections import deque

"""
MULTI-FACTOR INTRADAY STRATEGY (Optimized Weights)
====================================================
Combines cross-sectional short-term reversal and intraday momentum.
Weights optimized via grid search on validation set:
    Reversal = 0.7, Momentum = 0.3
"""


class Strategy:
    def __init__(self):
        # --- Hyperparameters ---
        self.lookback_short = 6       # 30 min (6 x 5-min bars) for reversal
        self.lookback_medium = 24     # 2 hours (24 x 5-min bars) for momentum
        self.top_k = 30              # Number of stocks to hold

        # Optimized factor weights (from grid search)
        self.w_reversal = 0.70
        self.w_momentum = 0.30

        # --- State Variables ---
        max_lookback = max(self.lookback_short, self.lookback_medium) + 1
        self.price_history = deque(maxlen=max_lookback)
        self.step_count = 0

    def step(self, current_market_data: pd.DataFrame) -> pd.Series:
        prices = current_market_data["close"]
        tickers = prices.index

        self.price_history.append(prices.values.copy())
        self.step_count += 1

        min_history = max(self.lookback_short, self.lookback_medium) + 1
        if self.step_count < min_history:
            return pd.Series(0.0, index=tickers)

        price_arr = np.array(self.price_history)
        current_prices = price_arr[-1]

        # Factor 1: Short-term reversal (30 min)
        past_short = price_arr[-1 - self.lookback_short]
        ret_short = (current_prices - past_short) / (past_short + 1e-10)
        reversal_signal = -ret_short  # buy losers

        # Factor 2: Intraday momentum (2 hours)
        past_medium = price_arr[-1 - self.lookback_medium]
        momentum_signal = (current_prices - past_medium) / (past_medium + 1e-10)

        # Rank-based composite (no volume factor needed)
        rank_rev = self._rank(reversal_signal)
        rank_mom = self._rank(momentum_signal)
        composite = self.w_reversal * rank_rev + self.w_momentum * rank_mom

        # Top-K equal weight
        top_indices = np.argsort(composite)[-self.top_k:]
        weights_arr = np.zeros(len(tickers))
        weights_arr[top_indices] = 1.0 / self.top_k
        return pd.Series(weights_arr, index=tickers)

    @staticmethod
    def _rank(arr):
        clean = np.where(np.isfinite(arr), arr, -np.inf)
        temp = clean.argsort().argsort()
        return temp / (len(temp) - 1 + 1e-10)
