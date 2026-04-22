from backtesting import Backtest, Strategy
import yfinance as yf

class NY_Open_MinuteStrategy(Strategy):
    def init(self):
        # Initialize indicators or variables here
        pass

    def next(self):
        # Implement your trading logic here
        pass

if __name__ == "__main__":
    # Download historical data for the desired stock (e.g., AAPL)
    data = yf.download("AAPL", period="1d", interval="1m")
    print(data)
    # Run the backtest
    # bt = Backtest(data, NY_Open_MinuteStrategy, cash=10000, commission=0.002)
    # stats = bt.run()
    # print(stats)
    # bt.plot()
