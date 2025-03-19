import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { changeStrategy } from '../api';

const strategies = [
  {
    id: 'masaniello',
    name: 'Masaniello',
    description: 'Adjusts stake based on bankroll',
    riskLevel: 'Moderate',
    details: 'Bets a fixed percentage of your bankroll. Provides good balance between risk and reward.'
  },
  {
    id: 'martingale',
    name: 'Martingale',
    description: 'Doubles stake after each loss',
    riskLevel: 'High',
    details: 'After each loss, double your bet. After a win, return to your base stake. Aims to recover losses, but requires a large bankroll.'
  },
  {
    id: 'fibonacci',
    name: 'Fibonacci',
    description: 'Uses Fibonacci sequence for stakes',
    riskLevel: 'High',
    details: 'Follow the Fibonacci sequence (1, 1, 2, 3, 5, 8, 13, 21...) to determine stakes after losses. Move back 2 steps after a win.'
  },
  {
    id: 'dalembert',
    name: 'D\'Alembert',
    description: 'Increases by 1 unit after loss, decreases by 1 after win',
    riskLevel: 'Moderate',
    details: 'Increase your bet by one unit after a loss, decrease by one unit after a win. More conservative than Martingale.'
  },
  {
    id: 'percentage',
    name: 'Percentage',
    description: 'Bets a fixed percentage of bankroll',
    riskLevel: 'Low',
    details: 'Bets a fixed percentage (usually 5%) of your current bankroll. Good for capital preservation and steady play.'
  },
  {
    id: 'kelly',
    name: 'Kelly Criterion',
    description: 'Calculates optimal bet size based on odds and probability',
    riskLevel: 'Moderate',
    details: 'Uses mathematical formula to determine optimal bet size based on probabilities and payouts. Maximizes long-term growth.'
  },
  {
    id: 'fixed',
    name: 'Fixed Stake',
    description: 'Always bets the same amount',
    riskLevel: 'Low',
    details: 'Always bet the same amount regardless of wins or losses. Simple and straightforward, good for beginners.'
  },
];

const riskColors = {
  'Low': 'success.main',
  'Moderate': 'warning.main',
  'High': 'error.main'
};

const StrategyPicker = ({ currentStrategy, onStrategyChange, onError }) => {
  const [selectedStrategy, setSelectedStrategy] = useState(currentStrategy || 'percentage');
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setSelectedStrategy(event.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const updatedGameState = await changeStrategy(selectedStrategy);
      onStrategyChange(updatedGameState);
    } catch (error) {
      console.error('Error changing strategy:', error);
      onError(error.response?.data?.detail || 'Error changing strategy');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" gutterBottom>
        Betting Strategy
      </Typography>
      
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel id="strategy-select-label">Strategy</InputLabel>
          <Select
            labelId="strategy-select-label"
            value={selectedStrategy}
            label="Strategy"
            onChange={handleChange}
          >
            {strategies.map((strategy) => (
              <MenuItem key={strategy.id} value={strategy.id}>
                {strategy.name} - {strategy.description}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading || selectedStrategy === currentStrategy}
        >
          {loading ? <CircularProgress size={24} /> : 'Apply Strategy'}
        </Button>
      </form>
      
      <Box sx={{ mt: 3 }}>
        {strategies.map((strategy) => (
          <Accordion key={strategy.id} disabled={strategy.id !== selectedStrategy}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>
                {strategy.name}
                {strategy.id === selectedStrategy && ' (Selected)'}
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" gutterBottom>
                <strong>Risk Level:</strong> <span style={{ color: riskColors[strategy.riskLevel] }}>{strategy.riskLevel}</span>
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Description:</strong> {strategy.description}
              </Typography>
              <Typography variant="body2">
                {strategy.details}
              </Typography>
            </AccordionDetails>
          </Accordion>
        ))}
      </Box>
    </Paper>
  );
};

export default StrategyPicker;
