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
            curr_low_amount = self.data.Low[-1]
            curr_high_amount = self.data.High[-1]
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
            
            if self.breakout_long and not self.position:
                
                #retest candle passes
                if curr_low_amount < self.high815 < curr_close_amount:
                    entry_price = curr_close_amount
                    stop_loss = self.low815
                    risk = entry_price - stop_loss
                    take_profit = entry_price + (risk * 2)
                    self.buy(sl=stop_loss, tp=take_profit)
                
                if curr_close_amount < self.high815:
                    self.breakout_long = False     
            
            '''
            retest short example:
            
            if a price breaks the low of 8-815 we look for shorts. to retest the breakout the next candles to come after the breakout have to have a 
            high greater than the 8-815 low but a close position below the 8-815 low, then we can enter a short position.
            
            during the retest stage if the candle closes above the low of 8-815 then the retest failed and we have to look
            for another breakout signal
            '''
            
            if self.breakout_short and not self.position:
                
                # The Retest
                if curr_high_amount > self.low815 > curr_close_amount:
                    entry_price = curr_close_amount
                    stop_loss = self.high815
                    risk = stop_loss - entry_price
                    take_profit = entry_price - (risk * 2)
                    
                    self.sell(sl=stop_loss, tp=take_profit)
                
                # Retest fails
                if curr_close_amount > self.low815:
                    self.breakout_short = False     
            
                     
            
                

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
