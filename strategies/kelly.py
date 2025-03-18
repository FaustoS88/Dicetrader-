"""
Kelly Criterion betting strategy.
Calculates optimal bet size based on odds and probability.
"""

def kelly(money, bet_history, probability, payout, fraction=0.5):
    """
    Kelly Criterion betting strategy.
    
    Parameters:
        money (float): Current bankroll
        bet_history (list): History of previous bets ('win' or 'loss')
        probability (float): Probability of winning
        payout (float): Payout multiplier
        fraction (float): Fraction of full Kelly to use (default: 0.5 for Half Kelly)
    
    Returns:
        float: Recommended stake
    """
    # Calculate Kelly fraction: (bp - q) / b
    # where b = payout - 1, p = probability of win, q = probability of loss
    b = payout - 1  # Net odds received on the wager
    p = probability
    q = 1 - p
    
    # Calculate Kelly percentage
    if b * p > q:
        kelly_percentage = (b * p - q) / b
    else:
        kelly_percentage = 0.01  # Minimum percentage
    
    # Apply fraction of Kelly (Half Kelly is more conservative)
    kelly_percentage *= fraction
    
    # Calculate stake
    stake = money * kelly_percentage
    
    # Ensure minimum bet of 1
    return max(1, stake)