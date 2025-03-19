import React, { useState, useEffect } from 'react';
import { 
  Paper, 
  Typography, 
  Box, 
  Button, 
  TextField, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem,
  Grid,
  Chip,
  Tooltip,
  CircularProgress
} from '@mui/material';
import { placeBet, getAIAdvice } from '../api';

const BetForm = ({ gameState, onBetPlaced, onError }) => {
  const [betSum, setBetSum] = useState(7);
  const [betAmount, setBetAmount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiAdvice, setAiAdvice] = useState(null);
  // Added to track if we need to refresh advice
  const [lastGameStateRound, setLastGameStateRound] = useState(0);

  // Get AI advice only when game state changes significantly
  useEffect(() => {
    const fetchAIAdvice = async () => {
      if (!gameState) return;
      
      // Only fetch new advice if round count or trend has changed
      if (
        !aiAdvice || 
        gameState.round_count !== lastGameStateRound || 
        gameState.trend !== (aiAdvice._gameStateSnapshot?.trend || '')
      ) {
        setAiLoading(true);
        try {
          const advice = await getAIAdvice();
          // Store game state snapshot with the advice
          advice._gameStateSnapshot = {
            round: gameState.round_count,
            trend: gameState.trend,
            money: gameState.money
          };
          setAiAdvice(advice);
          setLastGameStateRound(gameState.round_count);
        } catch (error) {
          console.error('Error fetching AI advice:', error);
          onError('Unable to fetch AI advice');
        } finally {
          setAiLoading(false);
        }
      }
    };

    fetchAIAdvice();
  }, [gameState, aiAdvice, lastGameStateRound, onError]);

  const handleBetSubmit = async (e) => {
    e.preventDefault();
    
    if (!gameState) {
      onError('Game not initialized');
      return;
    }
    
    if (betAmount <= 0) {
      onError('Bet amount must be greater than 0');
      return;
    }
    
    if (betAmount > gameState.money) {
      onError('Bet amount cannot exceed your bankroll');
      return;
    }
    
    setLoading(true);
    try {
      const response = await placeBet(betSum, betAmount);
      onBetPlaced(response);
    } catch (error) {
      console.error('Error placing bet:', error);
      onError(error.response?.data?.detail || 'Error placing bet');
    } finally {
      setLoading(false);
    }
  };

  const handleUseAIAdvice = () => {
    if (aiAdvice) {
      setBetSum(aiAdvice.recommended_sum);
      
      // Calculate appropriate bet amount based on recommended strategy
      const strategy = aiAdvice.recommended_strategy;
      
      switch (strategy) {
        case 'percentage':
          // 5% of bankroll for percentage strategy
          setBetAmount(Math.round(gameState.money * 0.05 * 100) / 100);
          break;
        case 'fixed':
          // Fixed amount (5 units)
          setBetAmount(5);
          break;
        case 'kelly':
          // Simplified Kelly calculation (approximately 2-7% of bankroll based on odds)
          const sum = aiAdvice.recommended_sum;
          const prob = gameState.probabilities[sum] || 0.1;
          const payout = getPayoutForSum(sum);
          const kelly = Math.max(0.02, Math.min(0.25, prob * payout - (1 - prob))) * gameState.money;
          setBetAmount(Math.round(kelly * 100) / 100);
          break;
        case 'martingale':
          // Start with 1% of bankroll for martingale
          setBetAmount(Math.round(gameState.money * 0.01 * 100) / 100);
          break;
        case 'fibonacci':
        case 'dalembert':
          // Start with 2% of bankroll for these progressive strategies
          setBetAmount(Math.round(gameState.money * 0.02 * 100) / 100);
          break;
        case 'masaniello':
          // 3% of bankroll for masaniello
          setBetAmount(Math.round(gameState.money * 0.03 * 100) / 100);
          break;
        default:
          // Default to 5% of bankroll if strategy is unknown
          setBetAmount(Math.round(gameState.money * 0.05 * 100) / 100);
      }
    }
  };

  const renderProbabilityChips = () => {
    if (!gameState || !gameState.probabilities) return null;
    
    return Object.entries(gameState.probabilities).map(([sum, probability]) => (
      <Grid item key={sum}>
        <Tooltip title={`Payout: ${getPayoutForSum(parseInt(sum))}x`}>
          <Chip
            label={`${sum}: ${(probability * 100).toFixed(1)}%`}
            color={parseInt(sum) === betSum ? 'primary' : 'default'}
            onClick={() => setBetSum(parseInt(sum))}
            variant={parseInt(sum) === betSum ? 'filled' : 'outlined'}
          />
        </Tooltip>
      </Grid>
    ));
  };

  const getPayoutForSum = (sum) => {
    const payouts = {
      2: 36, 3: 18, 4: 12, 5: 9,
      6: 7, 7: 6, 8: 7, 9: 9,
      10: 12, 11: 18, 12: 36
    };
    return payouts[sum] || 0;
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" gutterBottom>
        Place Your Bet
      </Typography>

      {gameState && (
        <>
          <Box sx={{ mb: 3 }}>
            <Typography>
              Market Trend: <Chip 
                              label={gameState.trend.toUpperCase()} 
                              color={gameState.trend === 'bull' ? 'success' : 'error'} 
                            />
            </Typography>
            
            <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
              Probabilities:
            </Typography>
            <Grid container spacing={1}>
              {renderProbabilityChips()}
            </Grid>
          </Box>

          {aiAdvice && (
            <Box sx={{ mb: 3, p: 2, bgcolor: '#27273D', borderRadius: 1 }}>
              <Typography variant="h6">
                AI Recommendation:
              </Typography>
              <Typography>
                Sum: <Chip label={aiAdvice.recommended_sum} color="primary" />
              </Typography>
              <Typography>
                Strategy: <Chip label={aiAdvice.recommended_strategy.toUpperCase()} />
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                {aiAdvice.reasoning}
              </Typography>
              <Button 
                variant="contained" 
                color="info" 
                sx={{ mt: 2 }} 
                onClick={handleUseAIAdvice}
                disabled={aiLoading}
              >
                Use AI Recommendation
              </Button>
            </Box>
          )}

          <form onSubmit={handleBetSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel id="bet-sum-label">Bet Sum</InputLabel>
                  <Select
                    labelId="bet-sum-label"
                    value={betSum}
                    label="Bet Sum"
                    onChange={(e) => setBetSum(e.target.value)}
                  >
                    {Array.from({ length: 11 }, (_, i) => i + 2).map((sum) => (
                      <MenuItem key={sum} value={sum}>
                        {sum} (Payout: {getPayoutForSum(sum)}x)
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Bet Amount"
                  type="number"
                  fullWidth
                  value={betAmount}
                  onChange={(e) => {
                    const value = e.target.value;
                    // Only update if there's a value
                    if (value) {
                      setBetAmount(Number(value));
                    } else {
                      setBetAmount('');
                    }
                  }}
                  inputProps={{ 
                    min: 1, 
                    step: "any" // Use "any" instead of 0.1 to allow any decimal value
                  }}
                  helperText={`Max: $${gameState.money.toFixed(2)}`}
                />
              </Grid>
              <Grid item xs={12}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Place Bet'}
                </Button>
              </Grid>
            </Grid>
          </form>
        </>
      )}
    </Paper>
  );
};

export default BetForm;
