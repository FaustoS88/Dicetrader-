import random
import numpy as np
from typing import Dict, List, Tuple, Optional
from models import GameState, BetResult, TrendType, DiceRoll, Portfolio, Position, RiskMetrics

# Payout multipliers based on the probability of the sum
PAYOUTS = {
    2: 36, 3: 18, 4: 12, 5: 9,
    6: 7, 7: 6, 8: 7, 9: 9,
    10: 12, 11: 18, 12: 36
}

# Base probabilities of each sum
BASE_PROBABILITIES = {
    2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36,
    6: 5/36, 7: 6/36, 8: 5/36, 9: 4/36,
    10: 3/36, 11: 2/36, 12: 1/36
}

MARKET_NEWS = {
    "bull": [
        "Market optimism rises as investors flock to higher sums!",
        "Analysts predict continued growth in high-value dice rolls!",
        "Bull market continues as high sums show strong performance!",
        "Investors confident in upper-range dice outcomes!",
        "Market rally continues with strong performance in sums 7-12!"
    ],
    "bear": [
        "Market caution as investors favor conservative bets!",
        "Analysts recommend focusing on lower sums in current climate!",
        "Bear market persists with strong performance in lower ranges!",
        "Investors seeking safety in lower-sum dice outcomes!",
        "Market downturn continues with strength in sums 2-6!"
    ],
    "volatile": [
        "Market volatility increases! Unexpected outcomes more likely!",
        "Unpredictable market conditions as volatility spikes!",
        "Analysts warn of increased uncertainty in dice outcomes!",
        "Market turbulence creates opportunities for risk-takers!",
        "High volatility market conditions reported by financial experts!"
    ]
}


def roll_dice() -> DiceRoll:
    """Roll two dice and return the sum and individual dice values"""
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return DiceRoll(dice_sum=dice1 + dice2, dice1=dice1, dice2=dice2)


def adjust_probabilities(trend: TrendType, volatility: float = 0.1) -> Dict[int, float]:
    """
    Adjust probabilities based on the current trend and volatility.
    
    Args:
        trend: "bull" or "bear"
        volatility: Level of volatility (0-1)
        
    Returns:
        Adjusted probabilities
    """
    probabilities = BASE_PROBABILITIES.copy()
    
    # Apply trend effect
    if trend == TrendType.BULL:
        for key in [7, 8, 9, 10, 11, 12]:
            probabilities[key] *= 1.5
    elif trend == TrendType.BEAR:
        for key in [2, 3, 4, 5, 6]:
            probabilities[key] *= 1.5
            
    # Apply volatility effect - higher volatility makes extreme outcomes more likely
    if volatility > 0.3:
        for key in [2, 3, 11, 12]:
            probabilities[key] *= (1 + volatility)
    
    # Normalize probabilities
    total = sum(probabilities.values())
    for key in probabilities:
        probabilities[key] /= total
        
    return probabilities


def update_market(dice_sum: int, game_state: GameState) -> Tuple[TrendType, bool, str]:
    """
    Update market trend based on dice roll.
    
    Args:
        dice_sum: Sum of the dice roll
        game_state: Current game state
        
    Returns:
        Tuple of (new trend, whether trend changed, market news)
    """
    # Update current round
    game_state.round_count += 1
    
    # Determine trend duration based on dice roll and round count
    trend_duration = random.randint(3, 7)
    
    # Check if we need to change trend
    trend_changed = False
    if game_state.round_count % trend_duration == 0:
        # 70% chance to change trend
        if random.random() < 0.7:
            new_trend = TrendType.BEAR if game_state.trend == TrendType.BULL else TrendType.BULL
            trend_changed = True
        else:
            new_trend = game_state.trend
    else:
        new_trend = game_state.trend
    
    # Generate market news
    if trend_changed:
        market_news = random.choice(MARKET_NEWS["bull" if new_trend == TrendType.BULL else "bear"])
    elif random.random() < game_state.volatility * 2:  # Higher volatility increases chance of volatility headlines
        market_news = random.choice(MARKET_NEWS["volatile"])
    else:
        market_news = random.choice(MARKET_NEWS["bull" if new_trend == TrendType.BULL else "bear"])
    
    return new_trend, trend_changed, market_news


def calculate_portfolio_return(portfolio: Portfolio, dice_sum: int) -> Tuple[float, List[Tuple[int, float]]]:
    """
    Calculate the return from a dice roll for a portfolio of bets.
    
    Args:
        portfolio: Player's betting portfolio
        dice_sum: Result of dice roll
        
    Returns:
        Tuple of (profit/loss, list of winning positions)
    """
    profit_loss = 0
    winning_positions = []
    
    # Calculate profit/loss
    for position in portfolio.positions:
        if position.bet_sum == dice_sum:
            # Win
            win_amount = position.amount * PAYOUTS[dice_sum]
            profit_loss += win_amount
            winning_positions.append((position.bet_sum, win_amount))
        else:
            # Loss
            profit_loss -= position.amount
                
    return profit_loss, winning_positions


def calculate_risk_metrics(portfolio: Portfolio, probabilities: Dict[int, float]) -> RiskMetrics:
    """
    Calculate risk metrics for a portfolio.
    
    Args:
        portfolio: Player's betting portfolio
        probabilities: Current probabilities for each sum
        
    Returns:
        Risk metrics including expected return, max loss, etc.
    """
    if not portfolio.positions:
        return RiskMetrics(
            expected_return=0,
            max_loss=0,
            max_gain=0,
            win_probability=0
        )
    
    # Calculate expected return
    expected_return = 0
    for position in portfolio.positions:
        # Expected value = probability * payout - (1-probability) * bet
        expected_return += (probabilities[position.bet_sum] * position.amount * PAYOUTS[position.bet_sum]) - \
                           ((1 - probabilities[position.bet_sum]) * position.amount)
    
    # Calculate maximum possible loss (lose all bets)
    max_loss = -sum(position.amount for position in portfolio.positions)
    
    # Calculate maximum possible gain (win all bets)
    max_gain = 0
    for position in portfolio.positions:
        max_gain += position.amount * PAYOUTS[position.bet_sum] - position.amount
    
    # Calculate probability of winning at least one bet
    win_probability = 1 - np.prod([1 - probabilities[position.bet_sum] 
                                 for position in portfolio.positions])
    
    return RiskMetrics(
        expected_return=expected_return,
        max_loss=max_loss,
        max_gain=max_gain,
        win_probability=win_probability
    )


def add_position(portfolio: Portfolio, bet_sum: int, amount: float) -> bool:
    """
    Add a bet to the portfolio.
    
    Args:
        portfolio: Current portfolio
        bet_sum: Sum to bet on
        amount: Amount to bet
        
    Returns:
        True if successful, False if portfolio is full
    """
    # Check if bet already exists in portfolio
    for position in portfolio.positions:
        if position.bet_sum == bet_sum:
            position.amount += amount
            return True
    
    # Check if portfolio is full
    if len(portfolio.positions) >= portfolio.max_positions:
        return False
    
    # Add new position
    portfolio.positions.append(Position(bet_sum=bet_sum, amount=amount))
    return True


def remove_position(portfolio: Portfolio, bet_sum: int) -> float:
    """
    Remove a bet from the portfolio.
    
    Args:
        portfolio: Current portfolio
        bet_sum: Sum to remove
        
    Returns:
        Amount that was bet on this sum, or 0 if not found
    """
    for i, position in enumerate(portfolio.positions):
        if position.bet_sum == bet_sum:
            amount = position.amount
            portfolio.positions.pop(i)
            return amount
    return 0


def get_total_investment(portfolio: Portfolio) -> float:
    """Get the total amount invested in the portfolio."""
    return sum(position.amount for position in portfolio.positions)


def clear_portfolio(portfolio: Portfolio) -> None:
    """Clear all bets from the portfolio."""
    portfolio.positions = []
