"""
Fixed stake betting strategy.
Always bets the same amount.
"""

def fixed(money, bet_history, amount=5):
    """
    Fixed stake betting strategy.
    
    Parameters:
        money (float): Current bankroll
        bet_history (list): History of previous bets ('win' or 'loss')
        amount (float): Fixed amount to bet (default: 5)
    
    Returns:
        float: Recommended stake
    """
    # Always return the fixed amount
    # But don't bet more than available
    return min(amount, money)