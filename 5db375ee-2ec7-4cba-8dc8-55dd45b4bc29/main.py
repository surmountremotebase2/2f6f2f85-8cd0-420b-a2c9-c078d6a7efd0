from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["BTC", "ETH"] # Example with Bitcoin and Ethereum

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            rsi_data = RSI(ticker, data["ohlcv"], length=14)

            if len(macd_data['MACD']) == 0 or len(rsi_data) == 0:
                log(f"Insufficient data for {ticker}")
                continue

            # Buy signal: when MACD crosses above its signal line and RSI is below 70 (to avoid overbought conditions)
            macd_current = macd_data['MACD'][-1]
            macd_signal_current = macd_data['signal'][-1]
            rsi_current = rsi_data[-1]

            is_buy_signal = macd_current > macd_signal_current and rsi_current < 70

            if is_buy_signal:
                # Allocate a portion of the portfolio to the ticker
                allocation_dict[ticker] = 1/len(self.tickers) # Equally weighted for simplicity
                
            else:
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)