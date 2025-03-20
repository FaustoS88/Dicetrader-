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

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const WinLossDistribution = ({ bets, results }) => {
  // Process data
  const processedData = useMemo(() => {
    const winsBySum = {};
    const lossesBySum = {};
    
    // Initialize all possible sums (2-12)
    for (let sum = 2; sum <= 12; sum++) {
      winsBySum[sum] = 0;
      lossesBySum[sum] = 0;
    }
    
    // Count wins and losses for each sum
    bets.forEach((betSum, index) => {
      if (results[index] === 1) {
        winsBySum[betSum]++;
      } else {
        lossesBySum[betSum]++;
      }
    });
    
    return {
      labels: Object.keys(winsBySum).map(Number),
      wins: Object.values(winsBySum),
      losses: Object.values(lossesBySum),
    };
  }, [bets, results]);

  const chartData = {
    labels: processedData.labels,
    datasets: [
      {
        label: 'Wins',
        data: processedData.wins,
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
      },
      {
        label: 'Losses',
        data: processedData.losses,
        backgroundColor: 'rgba(255, 99, 132, 0.8)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Win/Loss by Sum',
      },
    },
    scales: {
      x: {
        stacked: true,
        title: {
          display: true,
          text: 'Dice Sum',
        },
      },
      y: {
        stacked: true,
        title: {
          display: true,
          text: 'Count',
        },
      },
    },
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>Win/Loss Distribution</Typography>
      <Box sx={{ height: 300 }}>
        <Bar data={chartData} options={options} />
      </Box>
    </Paper>
  );
};

export default WinLossDistribution;