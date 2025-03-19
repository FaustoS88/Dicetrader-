from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import importlib

from models import (
    GameState, Bet, BetResponse, BetResult, TrendType, 
    Position, Portfolio, RiskMetrics, AIAdvice, Strategy,
    InitGameRequest, DiceRoll, AnalyticsData
)
import game_logic

import sys
import random
import os
import numpy as np

# Import AI Advisor if available
try:
    sys.path.append("../")  # Add parent directory to path to import original modules
    from ai_services.openrouter_client import OpenRouterClient, DeepSeekClient
    from strategies.ai_advisor import AIStrategyAdvisor
    AI_AVAILABLE = True
except ImportError:
    print("Warning: AI modules not found. AI features will be disabled.")
    AI_AVAILABLE = False

app = FastAPI(title="DiceTrader API", version="2.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for the game state
# In a production app, this would be stored in a database
game_state = None
analytics = AnalyticsData()
ai_advisor = None


@app.post("/init", response_model=GameState)
def initialize_game(request: InitGameRequest):
    """Initialize a new game with the given settings"""
    global game_state, ai_advisor
    
    # Initialize AI advisor if available
    if AI_AVAILABLE:
        ai_advisor = AIStrategyAdvisor()
    else:
        ai_advisor = None
    
    # Create new game state
    game_state = GameState(
        money=request.initial_bankroll,
        current_strategy=request.strategy,
        trend=TrendType.BULL if random.random() > 0.5 else TrendType.BEAR,
        volatility=0.2
    )
    
    # Initialize probabilities based on trend
    game_state.probabilities = game_logic.adjust_probabilities(game_state.trend, game_state.volatility)
    
    # Reset analytics
    global analytics
    analytics = AnalyticsData(bankroll_history=[request.initial_bankroll])
    
    return game_state


@app.get("/state", response_model=GameState)
def get_game_state():
    """Get the current game state"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    return game_state


@app.post("/bet", response_model=BetResponse)
def place_bet(bet: Bet):
    """Place a bet on a specific sum"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    # Check if player has enough money
    if bet.amount > game_state.money:
        raise HTTPException(status_code=400, detail="Not enough money to place bet")
    
    # Check if bet sum is valid
    if bet.bet_sum < 2 or bet.bet_sum > 12:
        raise HTTPException(status_code=400, detail="Invalid bet sum. Must be between 2 and 12")
    
    # Clear portfolio for single bet
    game_state.portfolio.positions = []
    
    # Add bet to portfolio
    game_logic.add_position(game_state.portfolio, bet.bet_sum, bet.amount)
    
    # Roll the dice
    dice_roll = game_logic.roll_dice()
    
    # Calculate returns
    profit_loss, winning_positions = game_logic.calculate_portfolio_return(
        game_state.portfolio, dice_roll.dice_sum)
    
    # Update money and bet history
    old_money = game_state.money
    game_state.money += profit_loss
    
    # Determine if this was a win or loss
    if profit_loss > 0:
        result = BetResult.WIN
        game_state.bet_history.append(BetResult.WIN)
    else:
        result = BetResult.LOSS
        game_state.bet_history.append(BetResult.LOSS)
    
    # Update market based on dice roll
    new_trend, trend_changed, market_news = game_logic.update_market(dice_roll.dice_sum, game_state)
    if trend_changed:
        game_state.trend = new_trend
        # Update probabilities when trend changes
        game_state.probabilities = game_logic.adjust_probabilities(game_state.trend, game_state.volatility)
    
    # Update analytics
    global analytics
    analytics.bankroll_history.append(game_state.money)
    analytics.win_history.append(1 if result == BetResult.WIN else 0)
    analytics.bet_amounts.append(bet.amount)
    analytics.bet_sums.append(bet.bet_sum)
    analytics.dice_results.append(dice_roll.dice_sum)
    analytics.trends.append(game_state.trend.value)
    _update_analytics_metrics()
    
    # Prepare response
    response = BetResponse(
        dice_roll=dice_roll,
        profit_loss=profit_loss,
        new_bankroll=game_state.money,
        result=result,
        winning_positions=winning_positions,
        trend_changed=trend_changed,
        new_trend=new_trend if trend_changed else None,
        market_news=market_news if trend_changed else None
    )
    
    # Clear portfolio after bet
    game_state.portfolio.positions = []
    
    return response


@app.post("/portfolio/add", response_model=bool)
def add_to_portfolio(position: Position):
    """Add a position to the portfolio"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    # Check if player has enough money
    total_invested = game_logic.get_total_investment(game_state.portfolio)
    if position.amount > (game_state.money - total_invested):
        raise HTTPException(status_code=400, detail="Not enough available funds")
    
    # Add position to portfolio
    success = game_logic.add_position(game_state.portfolio, position.bet_sum, position.amount)
    return success


@app.post("/portfolio/remove/{bet_sum}", response_model=float)
def remove_from_portfolio(bet_sum: int):
    """Remove a position from the portfolio"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    amount = game_logic.remove_position(game_state.portfolio, bet_sum)
    return amount


@app.post("/portfolio/clear")
def clear_portfolio():
    """Clear all positions from the portfolio"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    game_logic.clear_portfolio(game_state.portfolio)
    return {"status": "Portfolio cleared"}


@app.get("/portfolio", response_model=Portfolio)
def get_portfolio():
    """Get the current portfolio"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    return game_state.portfolio


@app.get("/portfolio/risk", response_model=RiskMetrics)
def get_risk_metrics():
    """Get risk metrics for the current portfolio"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    metrics = game_logic.calculate_risk_metrics(
        game_state.portfolio, game_state.probabilities)
    return metrics


@app.get("/strategy/advice", response_model=AIAdvice)
def get_ai_advice():
    """Get AI strategy advice"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    if not AI_AVAILABLE:
        # Provide a fallback recommendation if AI is not available
        # Find the sum with highest expected value
        payouts = {
            2: 36, 3: 18, 4: 12, 5: 9, 6: 7, 7: 6, 8: 7, 9: 9, 10: 12, 11: 18, 12: 36
        }
        expected_values = {s: p * payouts[s] for s, p in game_state.probabilities.items()}
        recommended_sum = max(expected_values, key=expected_values.get)
        
        return AIAdvice(
            recommended_sum=recommended_sum,
            recommended_strategy=game_state.current_strategy,
            reasoning="AI advisor not available. Recommendation based on expected value calculation."
        )
        
    if not ai_advisor:
        raise HTTPException(status_code=500, detail="AI advisor not initialized")
    
    try:
        advice = ai_advisor.get_strategy_advice(
            game_state.money, 
            [r.value for r in game_state.bet_history], 
            game_state.trend.value, 
            game_state.probabilities
        )
        
        return AIAdvice(
            recommended_sum=advice["recommended_sum"],
            recommended_strategy=advice["recommended_strategy"],
            reasoning=advice["reasoning"]
        )
    except Exception as e:
        # Fallback if AI advisor fails
        return AIAdvice(
            recommended_sum=7,  # Most common outcome
            recommended_strategy=game_state.current_strategy,
            reasoning=f"AI advisor encountered an error. Using statistical recommendation. Error: {str(e)}"
        )


@app.post("/strategy/change/{strategy}", response_model=GameState)
def change_strategy(strategy: Strategy):
    """Change the current betting strategy"""
    if not game_state:
        raise HTTPException(status_code=404, detail="Game not initialized")
    
    game_state.current_strategy = strategy
    return game_state


@app.get("/analytics", response_model=AnalyticsData)
def get_analytics():
    """Get game analytics data"""
    global analytics
    if not analytics:
        raise HTTPException(status_code=404, detail="No analytics data available")
    
    return analytics


def _update_analytics_metrics():
    """Update performance metrics in analytics"""
    global analytics
    
    # Win rate
    if analytics.win_history:
        analytics.win_rate = sum(analytics.win_history) / len(analytics.win_history)
    
    # Average win and loss
    wins = [amt for amt, win in zip(analytics.bet_amounts, analytics.win_history) if win]
    losses = [amt for amt, win in zip(analytics.bet_amounts, analytics.win_history) if not win]
    
    analytics.avg_win = sum(wins) / len(wins) if wins else 0
    analytics.avg_loss = sum(losses) / len(losses) if losses else 0
    
    # Calculate Sharpe ratio and max drawdown from bankroll history
    if len(analytics.bankroll_history) > 1:
        # Calculate returns
        returns = []
        for i in range(1, len(analytics.bankroll_history)):
            ret = (analytics.bankroll_history[i] - analytics.bankroll_history[i-1]) / analytics.bankroll_history[i-1]
            returns.append(ret)
        
        # Sharpe ratio (using risk-free rate of 0)
        mean_return = np.mean(returns)
        std_return = np.std(returns) if np.std(returns) > 0 else 1
        analytics.sharpe_ratio = mean_return / std_return
        
        # Maximum drawdown
        peak = analytics.bankroll_history[0]
        drawdown = 0
        
        for value in analytics.bankroll_history:
            if value > peak:
                peak = value
            current_drawdown = (peak - value) / peak
            drawdown = max(drawdown, current_drawdown)
        
        analytics.max_drawdown = drawdown


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
