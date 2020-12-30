from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import backtrader as bt # Import the backtrader platfor


# Create a Stratey
class SMAStrategy(bt.Strategy):

    params = (
        ('maperiod', None),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                

# ______________________ End Strategy Class



def timeFrame(datapath):
    """
    Select the write compression and timeframe
    """
    if datapath[-8:-4] == '1mth':
        compression = 1
        timeframe = bt.TimeFrame.Months
    elif datapath[-7:-4] == '12h':
        compression = 720
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-7:-4] == '15m':
        compression = 15
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-7:-4] == '30m':
        compression = 30
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '1d':
        compression = 1
        timeframe = bt.TimeFrame.Days
    elif datapath[-6:-4] == '1h':
        compression = 60
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '3m':
        compression = 3
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '2h':
        compression = 120
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '3d':
        compression = 3
        timeframe = bt.TimeFrame.Days
    elif datapath[-6:-4] == '1w':
        compression = 1
        timeframe = bt.TimeFrame.Weeks
    elif datapath[-6:-4] == '4h':
        compression = 240
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '5m':
        compression = 5
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '6h':
        compression = 360
        timeframe = bt.TimeFrame.Minutes
    elif datapath[-6:-4] == '8h':
        compression = 480
        timeframe = bt.TimeFrame.Minutes
    else:
        print('dataframe not recognized')
        exit()
    
    return compression, timeframe



def runbacktest(period, datapath, start, end, commission_val=None, portofolio=10000.0, stake_val=1, plt=False):

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake_val) # Multiply the stake by X

    cerebro.broker.setcash(portofolio) # default : 10000.0

    if commission_val:
        cerebro.broker.setcommission(commission=commission_val/100) # divide by 100 to remove the %

    # Add a strategy
    cerebro.addstrategy(SMAStrategy, maperiod=period)

    compression, timeframe = timeFrame(datapath)

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        dtformat = 2, 
        compression = compression, 
        timeframe = timeframe,
        fromdate = datetime.datetime.strptime(start, '%Y-%m-%d'),
        todate = datetime.datetime.strptime(end, '%Y-%m-%d'),
        reverse = False)


    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.run()

    if plt:
        cerebro.plot()

    return cerebro.broker.getvalue()