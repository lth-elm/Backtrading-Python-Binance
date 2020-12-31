import backtest, csv, os


commission_val = 0.04 # 0.04% taker fees binance usdt futures
portofolio = 10000.0
stake_val = 1
quantity = 0.10 # percentage to buy based on the current portofolio amount

start = '2017-01-01'
end = '2020-12-31'
# datapath = 'data/BTCUSDT-2017-2020-12h.csv'
strategies = ['SMA']
plot = False


for strategy in strategies:

    for data in os.listdir("./data"):

        datapath = 'data/' + data

        print('\n ------------ ', datapath)
        input()

        csvfile = open('result/{}-result-{}'.format(strategy, datapath[5:]), 'w', newline='')
        result_writer = csv.writer(csvfile, delimiter=',')

        result_writer.writerow(['data processed', 'parameter', 'portofolio final value', '%'])


        for period in range(10, 31):

            end_val = backtest.runbacktest(period, datapath, start, end, strategy, commission_val, portofolio, stake_val, quantity, plot)
            gain = ((end_val - portofolio) / portofolio) * 100


            print('%s, %s (Period %2d) - Ending Value : %.2f' % (datapath[5:], strategy, period, end_val))

            result_writer.writerow([datapath[5:-4], period, end_val, gain])

            plot=False


        csvfile.close()