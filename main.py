import backtest, csv


commission_val = 0.04 # 0.04% taker fees binance usdt futures
portofolio = 100000.0
stake_val = 2

start = '2017-01-01'
end = '2020-12-31'
datapath = 'data/BTCUSDT-2017-2020-4h.csv'


performances = []

for period in range(10, 31):

    end_val = backtest.runbacktest(period, datapath, start, end, commission_val, portofolio, stake_val, False)
    gain = ((end_val - portofolio) / portofolio) * 100
    print('(MA Period %2d) Ending Value %.2f' % (period, end_val))

    performances.append([datapath[5:-4], period, end_val, gain])



csvfile = open('result/SMA-result-{}'.format(datapath[5:]), 'w', newline='')
result_writer = csv.writer(csvfile, delimiter=',')

for result in performances:
    result_writer.writerow(result)

csvfile.close()