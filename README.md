# Roadmap

First, our goal is to backtest several trading strategy on different cryptocurrencies and timeframes and rank them according their profit return.

We won't bother developping a complex strategy, we will stick to basics ones using SMA and RSI relying on the Ta-Lib library and backtrader.

The cryptocurrencies datas needed are collected through the Binance API.

Later, the algorithm will be adapted for trading futures and the strategies will be improved. The bot will then be connected to Binance and take automatic positions according the best strategy returned by the backtest.

Ideally, the backtest will run automatically each X period and reset the best strategy.

