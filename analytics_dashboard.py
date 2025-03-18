import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from matplotlib.figure import Figure
import os
import json
from datetime import datetime

class AnalyticsDashboard:
    def __init__(self, save_dir=None):
        """Initialize the analytics dashboard."""
        self.bankroll_history = [100]  # Start with initial bankroll
        self.win_history = []  # Track wins/losses (1 for win, 0 for loss)
        self.bet_amounts = []  # Track bet amounts
        self.bet_sums = []  # Track which sums were bet on
        self.dice_results = []  # Track dice roll results
        self.trends = []  # Track market trends
        
        # Performance metrics
        self.win_rate = 0
        self.avg_win = 0
        self.avg_loss = 0
        self.sharpe_ratio = 0
        self.max_drawdown = 0
        
        # Create save directory if it doesn't exist
        if save_dir is None:
            # Use a relative path based on the current script location
            self.save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analytics')
        else:
            self.save_dir = save_dir
            
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def update(self, money, win, bet_amount, bet_sum, dice_result, trend):
        """
        Update dashboard with new game data.
        
        Parameters:
            money (float): Current bankroll
            win (bool): Whether the player won
            bet_amount (float): Amount bet
            bet_sum (int): Sum bet on
            dice_result (int): Result of dice roll
            trend (str): Current market trend
        """
        self.bankroll_history.append(money)
        self.win_history.append(1 if win else 0)
        self.bet_amounts.append(bet_amount)
        self.bet_sums.append(bet_sum)
        self.dice_results.append(dice_result)
        self.trends.append(trend)
        
        # Update performance metrics
        self._calculate_metrics()
    
    def _calculate_metrics(self):
        """Calculate performance metrics."""
        # Win rate
        if self.win_history:
            self.win_rate = sum(self.win_history) / len(self.win_history)
        
        # Average win and loss
        wins = [amt for amt, win in zip(self.bet_amounts, self.win_history) if win]
        losses = [amt for amt, win in zip(self.bet_amounts, self.win_history) if not win]
        
        self.avg_win = sum(wins) / len(wins) if wins else 0
        self.avg_loss = sum(losses) / len(losses) if losses else 0
        
        # Calculate returns
        returns = []
        for i in range(1, len(self.bankroll_history)):
            ret = (self.bankroll_history[i] - self.bankroll_history[i-1]) / self.bankroll_history[i-1]
            returns.append(ret)
        
        # Sharpe ratio (using risk-free rate of 0)
        if returns:
            mean_return = np.mean(returns)
            std_return = np.std(returns) if np.std(returns) > 0 else 1
            self.sharpe_ratio = mean_return / std_return
        
        # Maximum drawdown
        peak = self.bankroll_history[0]
        self.max_drawdown = 0
        
        for value in self.bankroll_history:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            self.max_drawdown = max(self.max_drawdown, drawdown)
    
    def generate_report(self):
        """
        Generate a text report of performance metrics.
        
        Returns:
            str: Performance report
        """
        report = "📊 PERFORMANCE REPORT 📊\n"
        report += "=" * 30 + "\n\n"
        
        report += f"Total Rounds: {len(self.win_history)}\n"
        report += f"Win Rate: {self.win_rate:.2%}\n"
        report += f"Average Win: ${self.avg_win:.2f}\n"
        report += f"Average Loss: ${self.avg_loss:.2f}\n"
        report += f"Starting Bankroll: ${self.bankroll_history[0]:.2f}\n"
        report += f"Current Bankroll: ${self.bankroll_history[-1]:.2f}\n"
        report += f"Profit/Loss: ${self.bankroll_history[-1] - self.bankroll_history[0]:.2f}\n"
        report += f"Sharpe Ratio: {self.sharpe_ratio:.2f}\n"
        report += f"Maximum Drawdown: {self.max_drawdown:.2%}\n\n"
        
        # Most profitable sums
        sum_profits = {}
        for i, sum_val in enumerate(self.bet_sums):
            if sum_val not in sum_profits:
                sum_profits[sum_val] = 0
            
            if self.win_history[i]:
                sum_profits[sum_val] += self.bet_amounts[i]
            else:
                sum_profits[sum_val] -= self.bet_amounts[i]
        
        report += "Most Profitable Sums:\n"
        sorted_sums = sorted(sum_profits.items(), key=lambda x: x[1], reverse=True)
        for sum_val, profit in sorted_sums[:3]:
            report += f"Sum {sum_val}: ${profit:.2f}\n"
        
        report += "\nLeast Profitable Sums:\n"
        for sum_val, profit in sorted_sums[-3:]:
            report += f"Sum {sum_val}: ${profit:.2f}\n"
        
        return report
    
    def save_plots(self):
        """Generate and save analytics plots."""
        # Create timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Plot 1: Bankroll over time
        fig1 = Figure(figsize=(10, 6))
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.bankroll_history, 'b-')
        ax1.set_title('Bankroll Over Time')
        ax1.set_xlabel('Round')
        ax1.set_ylabel('Bankroll ($)')
        ax1.grid(True)
        fig1.savefig(os.path.join(self.save_dir, f'bankroll_{timestamp}.png'))
        
        # Plot 2: Win/Loss Distribution
        fig2 = Figure(figsize=(10, 6))
        ax2 = fig2.add_subplot(111)
        
        # Count occurrences of each sum
        sum_counts = {}
        for sum_val in range(2, 13):
            wins = sum(1 for i, s in enumerate(self.bet_sums) if s == sum_val and self.win_history[i])
            losses = sum(1 for i, s in enumerate(self.bet_sums) if s == sum_val and not self.win_history[i])
            sum_counts[sum_val] = (wins, losses)
        
        sums = list(sum_counts.keys())
        wins = [sum_counts[s][0] for s in sums]
        losses = [sum_counts[s][1] for s in sums]
        
        width = 0.35
        ax2.bar(sums, wins, width, label='Wins')
        ax2.bar(sums, losses, width, bottom=wins, label='Losses')
        
        ax2.set_title('Win/Loss Distribution by Sum')
        ax2.set_xlabel('Sum')
        ax2.set_ylabel('Count')
        ax2.set_xticks(sums)
        ax2.legend()
        
        fig2.savefig(os.path.join(self.save_dir, f'win_loss_{timestamp}.png'))
        
        # Plot 3: Market Trend Analysis
        fig3 = Figure(figsize=(10, 6))
        ax3 = fig3.add_subplot(111)
        
        bull_returns = []
        bear_returns = []
        
        for i in range(1, len(self.bankroll_history)):
            ret = (self.bankroll_history[i] - self.bankroll_history[i-1]) / self.bankroll_history[i-1]
            if i-1 < len(self.trends):
                if self.trends[i-1] == "bull":
                    bull_returns.append(ret)
                else:
                    bear_returns.append(ret)
        
        labels = ['Bull Market', 'Bear Market']
        returns = [np.mean(bull_returns) if bull_returns else 0, 
                  np.mean(bear_returns) if bear_returns else 0]
        
        ax3.bar(labels, returns)
        ax3.set_title('Average Returns by Market Trend')
        ax3.set_ylabel('Average Return')
        
        fig3.savefig(os.path.join(self.save_dir, f'trend_returns_{timestamp}.png'))
        
        return [
            os.path.join(self.save_dir, f'bankroll_{timestamp}.png'),
            os.path.join(self.save_dir, f'win_loss_{timestamp}.png'),
            os.path.join(self.save_dir, f'trend_returns_{timestamp}.png')
        ]
    
    def save_data(self):
        """Save analytics data to JSON file."""
        data = {
            'bankroll_history': self.bankroll_history,
            'win_history': self.win_history,
            'bet_amounts': self.bet_amounts,
            'bet_sums': self.bet_sums,
            'dice_results': self.dice_results,
            'trends': self.trends,
            'metrics': {
                'win_rate': self.win_rate,
                'avg_win': self.avg_win,
                'avg_loss': self.avg_loss,
                'sharpe_ratio': self.sharpe_ratio,
                'max_drawdown': self.max_drawdown
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.save_dir, f'analytics_data_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        return filename