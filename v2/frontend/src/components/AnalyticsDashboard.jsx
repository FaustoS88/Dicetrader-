import React, { useState, useEffect } from 'react';
import { Paper, Typography, Box, Grid, CircularProgress, Divider } from '@mui/material';
import { getAnalytics } from '../api';
import BankrollChart from './analytics/BankrollChart';
import WinLossDistribution from './analytics/WinLossDistribution';
import TrendAnalysis from './analytics/TrendAnalysis';
import MetricsSummary from './analytics/MetricsSummary';

const AnalyticsDashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const data = await getAnalytics();
        setAnalytics(data);
      } catch (err) {
        console.error("Failed to fetch analytics:", err);
        setError("Could not load analytics data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
    
    // Set up polling to refresh analytics
    const intervalId = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Paper sx={{ p: 3, bgcolor: 'error.light', color: 'error.contrastText' }}>
        <Typography variant="h6">{error}</Typography>
      </Paper>
    );
  }

  if (!analytics || analytics.bankroll_history.length < 2) {
    return (
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6">Not enough data yet</Typography>
        <Typography variant="body1">
          Place more bets to see analytics data. You need at least 2 rounds of data.
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Analytics Dashboard</Typography>
      <Divider sx={{ mb: 3 }} />
      
      <Grid container spacing={3}>
        {/* Performance metrics summary */}
        <Grid item xs={12}>
          <MetricsSummary analytics={analytics} />
        </Grid>
        
        {/* Bankroll history chart */}
        <Grid item xs={12} md={8}>
          <BankrollChart data={analytics.bankroll_history} />
        </Grid>
        
        {/* Win/Loss by Sum */}
        <Grid item xs={12} md={4}>
          <WinLossDistribution 
            bets={analytics.bet_sums} 
            results={analytics.win_history}
          />
        </Grid>
        
        {/* Market Trend Analysis */}
        <Grid item xs={12}>
          <TrendAnalysis 
            bankrollHistory={analytics.bankroll_history}
            trends={analytics.trends}
          />
        </Grid>
      </Grid>
    </Paper>
  );
};

export default AnalyticsDashboard;