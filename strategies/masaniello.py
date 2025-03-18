def masaniello(bankroll, bet_history, preset_percentage=0.05):
    """
    Masaniello System: Adjusts the stake based on the current bankroll.
    :param bankroll: Current amount of money available.
    :param bet_history: List of previous bets (wins/losses).
    :param preset_percentage: Percentage of bankroll to bet (default: 5%).
    :return: Stake for the next bet.
    """
    return bankroll * preset_percentage