import React, { useMemo } from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const TrendAnalysis = ({ bankrollHistory, trends }) => {
  // Process data to calculate returns by trend
  const chartData = useMemo(() => {
    const bullReturns = [];
    const bearReturns = [];
    
    // Calculate returns
    for (let i = 1; i < bankrollHistory.length; i++) {
      const prevBalance = bankrollHistory[i-1];
      const currBalance = bankrollHistory[i];
      const returnPct = ((currBalance - prevBalance) / prevBalance) * 100;
      
      // Only include returns where we have trend data
      if (i-1 < trends.length) {
        if (trends[i-1] === 'bull') {
          bullReturns.push(returnPct);
        } else {
          bearReturns.push(returnPct);
        }
      }
    }
    
    // Calculate average returns
    const avgBullReturn = bullReturns.length ? 
      bullReturns.reduce((sum, val) => sum + val, 0) / bullReturns.length : 0;
    
    const avgBearReturn = bearReturns.length ? 
      bearReturns.reduce((sum, val) => sum + val, 0) / bearReturns.length : 0;
    
    return {
      labels: ['Bull Market', 'Bear Market'],
      datasets: [
        {
          label: 'Average Return (%)',
          data: [avgBullReturn, avgBearReturn],
          backgroundColor: [
            'rgba(255, 206, 86, 0.8)',
            'rgba(54, 162, 235, 0.8)',
          ],
        },
      ],
    };
  }, [bankrollHistory, trends]);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Returns by Market Trend',
      },
    },
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>Market Trend Analysis</Typography>
      <Box sx={{ height: 300 }}>
        <Bar data={chartData} options={options} />
      </Box>
    </Paper>
  );
};

export default TrendAnalysis;