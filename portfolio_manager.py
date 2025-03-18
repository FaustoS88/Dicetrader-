import numpy as np

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class PortfolioManager:
    def __init__(self):
        """Initialize the portfolio manager."""
        self.portfolio = {}  # Dictionary to store bets {sum: amount}
        self.max_positions = 5  # Maximum number of different sums to bet on
    
    def add_position(self, bet_sum, amount):
        """
        Add a bet to the portfolio.
        
        Parameters:
            bet_sum (int): Sum to bet on
            amount (float): Amount to bet
            
        Returns:
            bool: True if successful, False if portfolio is full
        """
        # Check if portfolio is full
        if bet_sum not in self.portfolio and len(self.portfolio) >= self.max_positions:
            return False
        
        # Add or update position
        if bet_sum in self.portfolio:
            self.portfolio[bet_sum] += amount
        else:
            self.portfolio[bet_sum] = amount
            
        return True
    
    def remove_position(self, bet_sum):
        """
        Remove a bet from the portfolio.
        
        Parameters:
            bet_sum (int): Sum to remove
            
        Returns:
            float: Amount that was bet on this sum, or 0 if not found
        """
        if bet_sum in self.portfolio:
            amount = self.portfolio[bet_sum]
            del self.portfolio[bet_sum]
            return amount
        return 0
    
    def clear_portfolio(self):
        """Clear all bets from the portfolio."""
        self.portfolio = {}
    
    def get_total_investment(self):
        """
        Get the total amount invested in the portfolio.
        
        Returns:
            float: Total investment
        """
        return sum(self.portfolio.values())
    
    def get_portfolio_summary(self):
        """
        Get a summary of the portfolio.
        
        Returns:
            str: Portfolio summary
        """
        if not self.portfolio:
            return f"{Colors.YELLOW}Portfolio is empty.{Colors.RESET}"
        
        summary = f"{Colors.BOLD}{Colors.CYAN}Your Portfolio:{Colors.RESET}\n"
        summary += "=" * 20 + "\n"
        
        for bet_sum, amount in self.portfolio.items():
            summary += f"Sum {bet_sum}: {Colors.GREEN}${amount:.2f}{Colors.RESET}\n"
            
        summary += "=" * 20 + "\n"
        summary += f"Total Investment: {Colors.BOLD}{Colors.GREEN}${self.get_total_investment():.2f}{Colors.RESET}\n"
        
        return summary
    
    def calculate_return(self, dice_sum, payouts):
        """
        Calculate the return from a dice roll.
        
        Parameters:
            dice_sum (int): Result of dice roll
            payouts (dict): Payout multipliers for each sum
            
        Returns:
            tuple: (profit/loss, list of winning positions)
        """
        profit_loss = 0
        winning_positions = []
        
        # Calculate profit/loss
        for bet_sum, amount in self.portfolio.items():
            if bet_sum == dice_sum:
                # Win
                profit_loss += amount * payouts[bet_sum]
                winning_positions.append((bet_sum, amount * payouts[bet_sum]))
            else:
                # Loss
                profit_loss -= amount
                
        return profit_loss, winning_positions
    
    def calculate_risk_metrics(self, probabilities, payouts):
        """
        Calculate risk metrics for the portfolio.
        
        Parameters:
            probabilities (dict): Probability of each sum
            payouts (dict): Payout multipliers for each sum
            
        Returns:
            dict: Risk metrics
        """
        if not self.portfolio:
            return {
                "expected_return": 0,
                "max_loss": 0,
                "max_gain": 0,
                "win_probability": 0
            }
        
        # Calculate expected return
        expected_return = 0
        for bet_sum, amount in self.portfolio.items():
            # Expected value = probability * payout - (1-probability) * bet
            expected_return += (probabilities[bet_sum] * amount * payouts[bet_sum]) - ((1 - probabilities[bet_sum]) * amount)
        
        # Calculate maximum possible loss (lose all bets)
        max_loss = -self.get_total_investment()
        
        # Calculate maximum possible gain (win all bets)
        max_gain = 0
        for bet_sum, amount in self.portfolio.items():
            max_gain += amount * payouts[bet_sum] - amount
        
        # Calculate probability of winning at least one bet
        win_probability = 1 - np.prod([1 - probabilities[bet_sum] for bet_sum in self.portfolio])
        
        return {
            "expected_return": expected_return,
            "max_loss": max_loss,
            "max_gain": max_gain,
            "win_probability": win_probability
        }