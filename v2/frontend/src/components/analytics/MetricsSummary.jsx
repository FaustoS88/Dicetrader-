import React from 'react';
import { Paper, Typography, Grid, Box, Chip } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

const MetricsSummary = ({ analytics }) => {
  const metrics = [
    { 
      label: 'Win Rate', 
      value: `${(analytics.win_rate * 100).toFixed(1)}%`,
      color: analytics.win_rate >= 0.5 ? 'success' : 'error'
    },
    { 
      label: 'Average Win', 
      value: `$${analytics.avg_win.toFixed(2)}`,
      color: 'success'
    },
    { 
      label: 'Average Loss', 
      value: `$${analytics.avg_loss.toFixed(2)}`,
      color: 'error'
    },
    { 
      label: 'Sharpe Ratio', 
      value: analytics.sharpe_ratio.toFixed(2),
      color: analytics.sharpe_ratio > 0 ? 'success' : 'error'
    },
    { 
      label: 'Max Drawdown', 
      value: `${(analytics.max_drawdown * 100).toFixed(1)}%`,
      color: 'warning'
    },
  ];

  const startingBankroll = analytics.bankroll_history[0] || 0;
  const currentBankroll = analytics.bankroll_history[analytics.bankroll_history.length - 1] || 0;
  const netProfit = currentBankroll - startingBankroll;
  const percentageReturn = startingBankroll ? (netProfit / startingBankroll) * 100 : 0;

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>Performance Summary</Typography>
      
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Typography variant="body2" sx={{ mr: 2 }}>
          Starting Balance: ${startingBankroll.toFixed(2)}
        </Typography>
        {netProfit >= 0 ? (
          <TrendingUpIcon color="success" sx={{ mr: 1 }} />
        ) : (
          <TrendingDownIcon color="error" sx={{ mr: 1 }} />
        )}
        <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
          Current Balance: ${currentBankroll.toFixed(2)}
        </Typography>
        <Chip 
          label={`${netProfit >= 0 ? '+' : ''}${netProfit.toFixed(2)} (${percentageReturn.toFixed(1)}%)`}
          color={netProfit >= 0 ? 'success' : 'error'}
          size="small"
          sx={{ ml: 2 }}
        />
      </Box>
      
      <Grid container spacing={2}>
        {metrics.map((metric) => (
          <Grid item xs={6} sm={4} md={2} key={metric.label}>
            <Paper sx={{ p: 2, textAlign: 'center' }} elevation={1}>
              <Typography variant="body2" color="text.secondary">
                {metric.label}
              </Typography>
              <Typography 
                variant="h6" 
                color={`${metric.color}.main`}
                sx={{ fontWeight: 'bold' }}
              >
                {metric.value}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default MetricsSummary;