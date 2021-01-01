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
        sep = datapath[5:-4].split(sep='-')

        print('\n ------------ ', datapath)
        print()

        dataname = 'result/{}-{}-{}-{}-{}.csv'.format(strategy, sep[0], start.replace('-',''), end.replace('-',''), sep[3])
        csvfile = open(dataname, 'w', newline='')
        result_writer = csv.writer(csvfile, delimiter=',')

        result_writer.writerow(['Pair', 'Timeframe', 'Start', 'End', 'Strategy', 'Period', 'Final value', '%', 'Total win', 'Total loss', 'SQN'])


        for period in range(10, 31):

            end_val, totalwin, totalloss, pnl_net, sqn = backtest.runbacktest(datapath, start, end, period, strategy, commission_val, portofolio, stake_val, quantity, plot)
            profit = (pnl_net / portofolio) * 100


            print('data processed: %s, %s (Period %d) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' % (datapath[5:], strategy, period, end_val, totalwin, totalloss, sqn))

            result_writer.writerow([sep[0], sep[3] , start, end, strategy, period, round(end_val,3), round(profit,3), totalwin, totalloss, sqn])


        csvfile.close()