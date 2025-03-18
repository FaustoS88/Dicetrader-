"""
Percentage betting strategy.
Bets a fixed percentage of the current bankroll.
"""

def percentage(money, bet_history, percentage=0.05):
    """
    Percentage betting strategy.
    
    Parameters:
        money (float): Current bankroll
        bet_history (list): History of previous bets ('win' or 'loss')
        percentage (float): Percentage of bankroll to bet (default: 5%)
    
    Returns:
        float: Recommended stake
    """
    # Bet a fixed percentage of current bankroll
    stake = money * percentage
    
    # Ensure minimum bet of 1
    return max(1, stake)