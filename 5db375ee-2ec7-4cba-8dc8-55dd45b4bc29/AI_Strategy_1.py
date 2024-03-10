from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    A simple momentum-based trading strategy that buys an asset when its price is above a certain Exponential 
    Moving Average (EMA) and sells when below. This example uses RSI for additional confirmation.
    """
    
    def __init__(self):
        self.tickers = ["SPY"]  # Example with SPY ETF, consider diversifying with more assets
        self.ema_period = 20  # Length of the EMA window
        self.rsi_period = 14  # Length of the RSI window
        self.rsi_overbought = 70  # RSI overbought threshold
        self.rsi_oversold = 30  # RSI oversold threshold
    
    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Using daily data for simplicity

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            ema = EMA(ticker, data["ohlcv"], self.ema_period)[-1]  # Get the last EMA value
            rsi = RSI(ticker, data["ohlcv"], self.rsi_period)[-1]  # Get the last RSI value
            current_price = data["ohlcv"][-1][ticker]["close"]  # Current closing price

            if current_price > ema and rsi < self.rsi_overbought:
                allocation_dict[ticker] = 1.0 / len(self.tickers)  # Full allocation if above EMA and not overbought
            elif current_price < ema or rsi > self.rsi_overbought:
                allocation_dict[ticker] = 0  # No allocation if below EMA or overbought

        return TargetAllocation(allocation_dict)