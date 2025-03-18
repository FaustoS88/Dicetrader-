import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import random

class MarketSimulator:
    def __init__(self, volatility=0.1, trend_strength=0.5):
        """
        Initialize the market simulator.
        
        Parameters:
            volatility (float): Base volatility level (0-1)
            trend_strength (float): Strength of trends (0-1)
        """
        self.volatility = volatility
        self.trend_strength = trend_strength
        self.market_data = []
        self.current_trend = random.choice(["bull", "bear"])
        self.trend_duration = random.randint(3, 7)  # Random duration between 3-7 rounds
        self.current_round = 0
        self.model = None
        
    def generate_market_data(self, rounds=20):
        """
        Generate synthetic market data for initial training.
        
        Parameters:
            rounds (int): Number of rounds to generate
        """
        # Start with a random value
        value = 100
        trend = random.choice(["bull", "bear"])
        trend_rounds = 0
        trend_duration = random.randint(3, 7)
        
        for _ in range(rounds):
            # Check if we need to change trend
            trend_rounds += 1
            if trend_rounds >= trend_duration:
                trend = random.choice(["bull", "bear"])
                trend_duration = random.randint(3, 7)
                trend_rounds = 0
                
            # Generate a random change based on trend
            if trend == "bull":
                change = np.random.normal(0.02, self.volatility)
            else:
                change = np.random.normal(-0.02, self.volatility)
                
            # Apply the change
            value *= (1 + change)
            self.market_data.append(value)
            
    def train_model(self):
        """
        Train an ARIMA model on the market data.
        """
        if len(self.market_data) < 10:
            self.generate_market_data(20)
            
        # Convert to pandas Series
        data = pd.Series(self.market_data)
        
        # Fit ARIMA model
        try:
            self.model = ARIMA(data, order=(1, 1, 1))
            self.model_fit = self.model.fit()
        except:
            # If ARIMA fails, use a simpler model
            self.model = None
            
    def predict_next_trend(self):
        """
        Predict the next market trend.
        
        Returns:
            str: Predicted trend ("bull" or "bear")
        """
        if self.model is None or len(self.market_data) < 10:
            return random.choice(["bull", "bear"])
            
        # Make a forecast
        forecast = self.model_fit.forecast(steps=1)
        
        # Determine trend based on forecast
        if forecast[0] > self.market_data[-1]:
            return "bull"
        else:
            return "bear"
            
    def update_market(self, dice_sum):
        """
        Update market data based on dice roll.
        
        Parameters:
            dice_sum (int): Sum of the dice roll
            
        Returns:
            str: Current market trend
        """
        # Add the dice sum to market data (normalized)
        normalized_value = dice_sum / 7 * 100  # Scale to be around 100
        self.market_data.append(normalized_value)
        
        # Limit market data to last 50 points
        if len(self.market_data) > 50:
            self.market_data = self.market_data[-50:]
            
        # Update current round
        self.current_round += 1
        
        # Check if we need to change trend
        if self.current_round >= self.trend_duration:
            # Try to predict next trend
            if random.random() < 0.7:  # 70% chance to use model prediction
                try:
                    self.train_model()
                    self.current_trend = self.predict_next_trend()
                except:
                    self.current_trend = random.choice(["bull", "bear"])
            else:
                self.current_trend = random.choice(["bull", "bear"])
                
            self.trend_duration = random.randint(3, 7)
            self.current_round = 0
            return self.current_trend, True  # True indicates trend changed
            
        return self.current_trend, False  # False indicates trend didn't change
        
    def get_market_news(self):
        """
        Generate market news based on current trend and volatility.
        
        Returns:
            str: Market news headline
        """
        bull_headlines = [
            "Market optimism rises as investors flock to higher sums!",
            "Analysts predict continued growth in high-value dice rolls!",
            "Bull market continues as high sums show strong performance!",
            "Investors confident in upper-range dice outcomes!",
            "Market rally continues with strong performance in sums 7-12!"
        ]
        
        bear_headlines = [
            "Market caution as investors favor conservative bets!",
            "Analysts recommend focusing on lower sums in current climate!",
            "Bear market persists with strong performance in lower ranges!",
            "Investors seeking safety in lower-sum dice outcomes!",
            "Market downturn continues with strength in sums 2-6!"
        ]
        
        volatility_headlines = [
            "Market volatility increases! Unexpected outcomes more likely!",
            "Unpredictable market conditions as volatility spikes!",
            "Analysts warn of increased uncertainty in dice outcomes!",
            "Market turbulence creates opportunities for risk-takers!",
            "High volatility market conditions reported by financial experts!"
        ]
        
        # Determine which type of headline to use
        if random.random() < self.volatility * 2:  # Higher volatility increases chance of volatility headlines
            return random.choice(volatility_headlines)
        elif self.current_trend == "bull":
            return random.choice(bull_headlines)
        else:
            return random.choice(bear_headlines)