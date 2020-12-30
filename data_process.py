import pandas as pd

df = pd.read_csv('result/SMA-result-BTCUSDT-2017-2020-4h.csv') # ',' default delimiter

print(df.sort_values('pnl %', ascending=False))

