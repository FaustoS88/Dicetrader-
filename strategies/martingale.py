def martingale(bankroll, bet_history, base_stake=1):
    """
    Martingale System: Doubles the stake after each loss.
    :param bankroll: Current amount of money available.
    :param bet_history: List of previous bets (wins/losses).
    :param base_stake: Base stake to start with (default: 1).
    :return: Stake for the next bet.
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
    return base_stake * (2 ** consecutive_losses)