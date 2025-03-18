def fibonacci(bankroll, bet_history, sequence=[1, 1]):
    """
    Fibonacci System: Follows the Fibonacci sequence to determine the stake.
    :param bankroll: Current amount of money available.
    :param bet_history: List of previous bets (wins/losses).
    :param sequence: Current state of the Fibonacci sequence (default: [1, 1]).
    :return: Stake for the next bet.
    """
    if not bet_history:
        return sequence[-1]
    if bet_history[-1] == "loss":
        sequence.append(sequence[-1] + sequence[-2])
        return sequence[-1]
    if len(sequence) > 2:
        sequence.pop()
    return sequence[-1]