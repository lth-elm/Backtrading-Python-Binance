import backtest, csv, os


commission_val = 0.04 # 0.04% taker fees binance usdt futures
portofolio = 10000.0
stake_val = 1
quantity = 0.10 # percentage to buy based on the current portofolio amount

# start = '2018-03-01'
# end = '2020-11-15'
start = '2017-01-01'
end = '2020-12-31'
strategies = ['SMA', 'RSI']
plot = False


for strategy in strategies:

    for data in os.listdir("./data"):

        datapath = 'data/' + data

        print('\n ------------ ', datapath)
        print()

        dataname = 'result/{}-{}-{}{}{}-{}{}{}-{}'.format(strategy, datapath[5:12], start[:4], start[5:7], start[8:], end[:4], end[5:7], end[8:], datapath[23:])
        csvfile = open(dataname, 'w', newline='')
        result_writer = csv.writer(csvfile, delimiter=',')

        result_writer.writerow(['pairs', 'timeframe', 'start', 'end', 'strategy', 'period', 'portofolio final value', '%'])


        for period in range(10, 31):

            end_val = backtest.runbacktest(datapath, start, end, period, strategy, commission_val, portofolio, stake_val, quantity, plot)
            gain = ((end_val - portofolio) / portofolio) * 100


            print('data processed : %s, %s (Period %2d) - Ending Value : %.2f' % (datapath[5:], strategy, period, end_val))

            result_writer.writerow([datapath[5:12], datapath[23:-4] , start, end, strategy, period, end_val, gain])

            plot=False


        csvfile.close()