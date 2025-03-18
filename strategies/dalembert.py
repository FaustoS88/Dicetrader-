"""
D'Alembert betting strategy.
Increases stake by 1 unit after a loss, decreases by 1 unit after a win.
More conservative than Martingale.
"""

def dalembert(money, bet_history, base_unit=1):
    """
    D'Alembert betting strategy.
    
    Parameters:
        money (float): Current bankroll
        bet_history (list): History of previous bets ('win' or 'loss')
        base_unit (float): Base betting unit (default: 1)
    
    Returns:
        float: Recommended stake
    """
    # Start with base unit
    if not bet_history:
        return base_unit
    
    # Count consecutive wins and losses
    consecutive_count = 0
    for result in reversed(bet_history):
        if result == bet_history[-1]:
            consecutive_count += 1
        else:
            break
    
    # Adjust stake based on last result
    if bet_history[-1] == "win":
        # Decrease stake by 1 unit after a win (minimum is base_unit)
        return max(base_unit, base_unit + consecutive_count - 1)
    else:
        # Increase stake by 1 unit after a loss
        return base_unit + consecutive_count