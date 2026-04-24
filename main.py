from backtesting import Backtest, Strategy
import yfinance as yf
import time

class Strat_815(Strategy):
    def init(self):
        # Initialize indicators or variables here

        self.high815 = None
        self.low815 = None
        self.breakout_long = False
        self.breakout_short = False

        pass

    def next(self):
        # Implement your trading logic here


        curr_time = self.data.index[-1].time()

        '''
        get the high and low from 8-815
        '''
        if curr_time == time(8,0):
            self.high815 = self.data.High[-1]  
            self.low815 = self.data.Low[-1]    
        elif time(8,0) < curr_time <= time(8,15):
            self.high815 = max(self.high815, self.data.High[-1])
            self.low815 = min(self.low815, self.data.Low[-1])

        if curr_time >= time(9,30):
            curr_close_amount = self.data.Close[-1]
        
            # find a breakout
            if not self.breakout_long or not self.breakout_short:
                if curr_close_amount > self.high815:
                    self.breakout_long = True
                elif curr_close_amount < self.low815:
                    self.breakout_short = True
            
            '''
            retest the breakout
            
            long breakout example:

            if a price breaks above the high of 8-815
            we want to check the next candles to see if the wick goes below the high of 8-815
            and the close is above the high of 8-815, then we can enter a long position

            if a candle closes below the high of 8-815 then the breakout was weak and we have to 
            look for another breakout, we can reset the breakout_long variable to False and wait 
            for another breakout signal
            '''

        pass

if __name__ == "__main__":
    # Download historical data for the desired stock (e.g., AAPL)
    ticker = "AAPL"
    data = yf.download(ticker, start="2026-04-22", end="2026-04-23", interval="5m", prepost=True)
    data.index = data.index.tz_convert("US/Eastern")
    strategy_candle = data.between_time("08:00", "08:15")

    # Run the backtest
    # bt = Backtest(data, Strat_815, cash=10000, commission=0.002)
    # stats = bt.run()
    # print(stats)
    # bt.plot()
