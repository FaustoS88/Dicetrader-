from typing import List

def masaniello(bankroll: float, bet_history: List[str], preset_percentage: float = 0.05) -> float:
    """
    Masaniello System: Adjusts the stake based on the current bankroll.
    
    Args:
        bankroll: Current amount of money available.
        bet_history: List of previous bets (wins/losses).
        preset_percentage: Percentage of bankroll to bet (default: 5%).
        
    Returns:
        Stake for the next bet.
    """
    return bankroll * preset_percentage
