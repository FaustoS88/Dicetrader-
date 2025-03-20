import React, { useState, useEffect } from 'react';
import { 
  Container, 
  CssBaseline, 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Button, 
  Alert,
  Snackbar,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import BetForm from './components/BetForm';
import GameStatus from './components/GameStatus';
import StrategyPicker from './components/StrategyPicker';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import { initializeGame } from './api';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

function App() {
  const [gameState, setGameState] = useState(null);
  const [lastBet, setLastBet] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [initDialogOpen, setInitDialogOpen] = useState(false);
  const [initialBankroll, setInitialBankroll] = useState(100);

  // Initialize game on first load
  useEffect(() => {
    handleInitializeGame();
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleInitializeGame = async (customBankroll = 100) => {
    setLoading(true);
    setError(null);
    
    try {
      const newGameState = await initializeGame(customBankroll, 'percentage');
      setGameState(newGameState);
      setLastBet(null);
      
      toast.success('Game initialized successfully!');
    } catch (err) {
      console.error('Error initializing game:', err);
      setError('Failed to initialize game. Please try again.');
      toast.error('Failed to initialize game');
    } finally {
      setLoading(false);
      setInitDialogOpen(false);
    }
  };

  const handleBetPlaced = (response) => {
    // Reset lastBet first to ensure animation triggers on consecutive bets with same values
    setLastBet(null);
    
    // Update state after a small delay to ensure the animation component resets
    setTimeout(() => {
      setLastBet(response);
      setGameState((prev) => ({
        ...prev,
        money: response.new_bankroll,
        bet_history: [...prev.bet_history, response.result],
        round_count: prev.round_count + 1,
        trend: response.trend_changed ? response.new_trend : prev.trend,
      }));
      
      if (response.result === 'win') {
        toast.success(`You won $${response.profit_loss.toFixed(2)}!`);
      } else {
        toast.error(`You lost $${Math.abs(response.profit_loss).toFixed(2)}`);
      }
      
      if (response.trend_changed) {
        toast.info(`Market trend changed to ${response.new_trend.toUpperCase()}`);
      }
    }, 50);
  };

  const handleStrategyChange = (updatedGameState) => {
    setGameState(updatedGameState);
    toast.info(`Strategy changed to ${updatedGameState.current_strategy.toUpperCase()}`);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    toast.error(errorMessage);
  };

  const handleCloseError = () => {
    setError(null);
  };

  const handleOpenInitDialog = () => {
    setInitDialogOpen(true);
  };

  const handleCloseInitDialog = () => {
    setInitDialogOpen(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ToastContainer position="top-right" autoClose={3000} hideProgressBar={false} />
      
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🎲📈 DiceTrader v2
          </Typography>
          <Button color="inherit" onClick={handleOpenInitDialog}>New Game</Button>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {error && (
          <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseError}>
            <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
              {error}
            </Alert>
          </Snackbar>
        )}
        
        {gameState ? (
          <>
            <GameStatus gameState={gameState} lastBet={lastBet} loading={loading} />
            
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
              <Tabs value={activeTab} onChange={handleTabChange} aria-label="game tabs">
                <Tab label="Place Bet" />
                <Tab label="Strategy" />
                <Tab label="Analytics" />
              </Tabs>
            </Box>
            
            {activeTab === 0 && (
              <BetForm 
                gameState={gameState} 
                onBetPlaced={handleBetPlaced} 
                onError={handleError} 
              />
            )}
            
            {activeTab === 1 && (
              <StrategyPicker 
                currentStrategy={gameState.current_strategy} 
                onStrategyChange={handleStrategyChange} 
                onError={handleError} 
              />
            )}
            
            {activeTab === 2 && (
              <AnalyticsDashboard />
            )}
          </>
        ) : (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
            <Typography variant="h4">Loading game...</Typography>
          </Box>
        )}
      </Container>
      
      <Dialog open={initDialogOpen} onClose={handleCloseInitDialog}>
        <DialogTitle>Start New Game</DialogTitle>
        <DialogContent>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Are you sure you want to start a new game? Your current progress will be lost.
          </Typography>
          <TextField
            autoFocus
            margin="dense"
            id="bankroll"
            label="Initial Bankroll"
            type="number"
            fullWidth
            variant="outlined"
            value={initialBankroll}
            onChange={(e) => setInitialBankroll(Number(e.target.value))}
            inputProps={{ min: 10, step: 10 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseInitDialog}>Cancel</Button>
          <Button 
            onClick={() => handleInitializeGame(initialBankroll)} 
            variant="contained" 
            color="primary"
          >
            Start New Game
          </Button>
        </DialogActions>
      </Dialog>
    </ThemeProvider>
  );
}

export default App;
