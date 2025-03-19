import React, { useState, useEffect } from 'react';
import { 
  Paper, 
  Typography, 
  Box, 
  Chip, 
  Grid,
  LinearProgress,
  Card,
  CardContent
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import EqualizerIcon from '@mui/icons-material/Equalizer';
import DiceAnimation from './DiceAnimation';

const GameStatus = ({ gameState, lastBet, loading }) => {
  const [diceRolling, setDiceRolling] = useState(false);
  const [showResult, setShowResult] = useState(false);
  
  // Reset and trigger animation when new bet is placed
  useEffect(() => {
    if (lastBet) {
      // Start dice rolling animation
      setDiceRolling(true);
      setShowResult(false);
    }
  }, [lastBet]);

  // Handle animation end
  const handleRollEnd = () => {
    setDiceRolling(false);
    setShowResult(true);
  };

  if (!gameState) return null;

  const renderDiceResult = () => {
    if (!lastBet) return null;
    
    return (
      <Box sx={{ mb: 3 }}>
        <Paper
          sx={{
            p: 3,
            bgcolor: lastBet.result === 'win' ? 'success.light' : 'error.light',
            color: 'white',
            textAlign: 'center'
          }}
        >
          <Typography variant="h4" gutterBottom>
            Dice Roll: {lastBet.dice_roll.dice_sum}
          </Typography>
          
          {/* Dice Animation */}
          <DiceAnimation 
            dice1={lastBet.dice_roll.dice1} 
            dice2={lastBet.dice_roll.dice2} 
            rolling={diceRolling}
            onRollEnd={handleRollEnd}
          />
          
          {showResult && (
            <>
              <Typography variant="h5" gutterBottom>
                {lastBet.result === 'win' ? 'You Won!' : 'You Lost!'}
              </Typography>
              <Typography variant="h6">
                {lastBet.result === 'win' ? '+' : ''}${Math.abs(lastBet.profit_loss).toFixed(2)}
              </Typography>
            </>
          )}
        </Paper>
      </Box>
    );
  };

  const renderMarketTrend = () => {
    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Market Trend
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {gameState.trend === 'bull' ? (
              <>
                <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                <Chip label="BULL MARKET" color="success" />
              </>
            ) : (
              <>
                <TrendingDownIcon color="error" sx={{ mr: 1 }} />
                <Chip label="BEAR MARKET" color="error" />
              </>
            )}
          </Box>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Volatility
            </Typography>
            <LinearProgress
              variant="determinate"
              value={gameState.volatility * 100}
              color={gameState.volatility > 0.5 ? "warning" : "primary"}
              sx={{ height: 10, borderRadius: 5 }}
            />
            <Typography variant="caption" color="text.secondary">
              {(gameState.volatility * 100).toFixed(0)}%
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const renderBankrollInfo = () => {
    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <AttachMoneyIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
            Bankroll
          </Typography>
          <Typography variant="h4" color="primary">
            ${gameState.money.toFixed(2)}
          </Typography>

          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Strategy: <Chip size="small" label={gameState.current_strategy.toUpperCase()} />
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const renderStats = () => {
    const winCount = gameState.bet_history.filter(result => result === 'win').length;
    const totalBets = gameState.bet_history.length;
    const winRate = totalBets > 0 ? (winCount / totalBets) * 100 : 0;

    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <EqualizerIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
            Statistics
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography variant="body2" color="text.secondary">
                Rounds Played
              </Typography>
              <Typography variant="h6">
                {gameState.round_count}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="body2" color="text.secondary">
                Win Rate
              </Typography>
              <Typography variant="h6" color={winRate >= 50 ? "success.main" : "error.main"}>
                {winRate.toFixed(1)}%
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      {loading && <LinearProgress />}
      
      {renderDiceResult()}
      
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          {renderBankrollInfo()}
        </Grid>
        <Grid item xs={12} md={6}>
          {renderMarketTrend()}
        </Grid>
        <Grid item xs={12}>
          {renderStats()}
        </Grid>
      </Grid>
    </Paper>
  );
};

export default GameStatus;
