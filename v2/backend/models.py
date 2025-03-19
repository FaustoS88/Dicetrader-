from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Literal
from enum import Enum
from datetime import datetime


class TrendType(str, Enum):
    BULL = "bull"
    BEAR = "bear"


class BetResult(str, Enum):
    WIN = "win"
    LOSS = "loss"


class Strategy(str, Enum):
    MASANIELLO = "masaniello"
    MARTINGALE = "martingale"
    FIBONACCI = "fibonacci"
    DALEMBERT = "dalembert"
    PERCENTAGE = "percentage"
    KELLY = "kelly"
    FIXED = "fixed"


class Bet(BaseModel):
    bet_sum: int = Field(..., ge=2, le=12, description="Sum to bet on (2-12)")
    amount: float = Field(..., gt=0, description="Amount to bet")


class Position(BaseModel):
    bet_sum: int = Field(..., ge=2, le=12)
    amount: float = Field(..., gt=0)


class Portfolio(BaseModel):
    positions: List[Position] = []
    max_positions: int = 5


class RiskMetrics(BaseModel):
    expected_return: float
    max_loss: float
    max_gain: float
    win_probability: float


class GameState(BaseModel):
    """Represents the current state of the game"""
    money: float = Field(100.0, description="Current bankroll")
    bet_history: List[BetResult] = Field([], description="History of bet results")
    trend: TrendType = Field(TrendType.BULL, description="Current market trend")
    volatility: float = Field(0.1, ge=0, le=1, description="Current market volatility")
    round_count: int = Field(0, ge=0, description="Number of rounds played")
    probabilities: Dict[int, float] = Field({}, description="Current probabilities for each sum")
    current_strategy: Strategy = Field(Strategy.PERCENTAGE, description="Current betting strategy")
    portfolio: Portfolio = Field(default_factory=Portfolio, description="Current betting portfolio")


class DiceRoll(BaseModel):
    """Result of rolling dice"""
    dice_sum: int = Field(..., ge=2, le=12)
    dice1: int = Field(..., ge=1, le=6)
    dice2: int = Field(..., ge=1, le=6)


class BetResponse(BaseModel):
    """Response after placing a bet"""
    dice_roll: DiceRoll
    profit_loss: float
    new_bankroll: float
    result: BetResult
    winning_positions: List[tuple] = []
    trend_changed: bool = False
    new_trend: Optional[TrendType] = None
    market_news: Optional[str] = None


class AIAdvice(BaseModel):
    """AI strategy recommendation"""
    recommended_sum: int = Field(..., ge=2, le=12)
    recommended_strategy: Strategy
    reasoning: str


class AnalyticsData(BaseModel):
    """Game analytics data"""
    bankroll_history: List[float] = []
    win_history: List[int] = []
    bet_amounts: List[float] = []
    bet_sums: List[int] = []
    dice_results: List[int] = []
    trends: List[str] = []
    win_rate: float = 0
    avg_win: float = 0
    avg_loss: float = 0
    sharpe_ratio: float = 0
    max_drawdown: float = 0
    timestamp: datetime = Field(default_factory=datetime.now)


class InitGameRequest(BaseModel):
    """Request to initialize a new game"""
    initial_bankroll: float = Field(100.0, gt=0)
    strategy: Strategy = Field(Strategy.PERCENTAGE)
