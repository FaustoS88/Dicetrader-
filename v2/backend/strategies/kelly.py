from typing import List

def kelly(bankroll: float, bet_history: List[str], probability: float, payout: float, fraction: float = 0.5) -> float:
    """
    Kelly Criterion betting strategy.
    Calculates optimal bet size based on odds and probability.
    
    Args:
        bankroll: Current amount of money available.
        bet_history: List of previous bets (wins/losses).
        probability: Probability of winning.
        payout: Payout multiplier.
        fraction: Fraction of full Kelly to use (default: 0.5 for Half Kelly).
        
    Returns:
        Stake for the next bet.
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
    stake = bankroll * kelly_percentage
    
    # Ensure minimum bet of 1
    return max(1, stake)