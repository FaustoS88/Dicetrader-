from typing import List

def fixed(bankroll: float, bet_history: List[str], amount: float = 5) -> float:
    """
    Fixed stake betting strategy.
    Always bets the same amount.
    
    Args:
        bankroll: Current amount of money available.
        bet_history: List of previous bets (wins/losses).
        amount: Fixed amount to bet (default: 5).
        
    Returns:
        Stake for the next bet.
    """
    # Always return the fixed amount
    # But don't bet more than available
    return min(amount, bankroll)