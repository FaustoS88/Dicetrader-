from typing import List

def martingale(bankroll: float, bet_history: List[str], base_stake: float = 1) -> float:
    """
    Martingale System: Doubles the stake after each loss.
    
    Args:
        bankroll: Current amount of money available.
        bet_history: List of previous bets (wins/losses).
        base_stake: Base stake to start with (default: 1).
        
    Returns:
        Stake for the next bet.
    """
    if not bet_history:
        return base_stake
        
    # Count consecutive losses
    consecutive_losses = 0
    for result in reversed(bet_history):
        if result == "loss":
            consecutive_losses += 1
        else:
            break
            
    # Calculate stake
    stake = base_stake * (2 ** consecutive_losses)
    
    # Don't bet more than the bankroll
    return min(stake, bankroll)
