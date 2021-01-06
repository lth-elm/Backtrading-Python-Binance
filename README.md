1. [Introduction and Roadmap](#introduction)
2. [Code review](#review)
3. [Analysis](#analysis)

# Introduction and Roadmap <a name="introduction"></a>

First, our goal is to backtest several trading strategy on different cryptocurrencies and timeframes and rank them according their profit return. We won't bother developping a complex strategy, we will stick to basics ones using SMA and RSI relying on the Ta-Lib library and backtrader and we will vary the period used between 10 and 30. [backtesting code](backtest.py) | [requirements needed](requirements.txt)

The cryptocurrencies datas needed are collected through the Binance API. [code to get the wanted kandlesticks](get_data.py) | [file containing this datas](data/)

These datas will be processed by the [get_result.py](get_result.py) code that will run through all the datas in the data file and save the result in [result/](result/).

Finally the top 10 strategies will be saved to a [JSON file](top10sqn.json) so that we may reuse them.

&nbsp;

*Later, the algorithm will be adapted for trading futures and the strategies will be improved. The bot will then be connected to Binance and take automatic positions according the best strategy returned by the backtest.*

*Ideally, the backtest will run automatically each X period and reset the best strategy.*

# Code review <a name="review"></a>

Write the code review here

# Analysis <a name="analysis"></a>

Find the analysis in [README.ipynb](README.ipynb) notebook.