from typing import List

def percentage(bankroll: float, bet_history: List[str], percentage: float = 0.05) -> float:
    """
    Percentage betting strategy.
    Bets a fixed percentage of the current bankroll.
    
    Args:
        bankroll: Current amount of money available.
        bet_history: List of previous bets (wins/losses).
        percentage: Percentage of bankroll to bet (default: 5%).
        
    Returns:
        Stake for the next bet.
    """
    # Bet a fixed percentage of current bankroll
    stake = bankroll * percentage
    
    # Ensure minimum bet of 1
    return max(1, stake)