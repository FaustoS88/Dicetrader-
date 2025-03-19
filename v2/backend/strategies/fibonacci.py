from typing import List

def fibonacci(bankroll: float, bet_history: List[str]) -> float:
    """
    Fibonacci System: Follows the Fibonacci sequence to determine the stake.
    
    Args:
        bankroll: Current amount of money available.
        bet_history: List of previous bets (wins/losses).
        
    Returns:
        Stake for the next bet.
    """
    # Initialize Fibonacci sequence
    sequence = [1, 1]
    
    if not bet_history:
        return sequence[-1]
        
    # Calculate position in Fibonacci sequence based on consecutive losses
    consecutive_losses = 0
    for result in reversed(bet_history):
        if result == "loss":
            consecutive_losses += 1
        else:
            break
            
    # Generate Fibonacci sequence up to the required position
    while len(sequence) <= consecutive_losses + 1:
        sequence.append(sequence[-1] + sequence[-2])
        
    # Get the stake from the sequence
    stake = sequence[consecutive_losses + 1]
    
    # Don't bet more than the bankroll
    return min(stake, bankroll)
