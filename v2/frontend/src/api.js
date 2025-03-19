import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const initializeGame = async (initialBankroll = 100, strategy = 'percentage') => {
  try {
    const response = await api.post('/init', { initial_bankroll: initialBankroll, strategy });
    return response.data;
  } catch (error) {
    console.error('Error initializing game:', error);
    throw error;
  }
};

export const getGameState = async () => {
  try {
    const response = await api.get('/state');
    return response.data;
  } catch (error) {
    console.error('Error getting game state:', error);
    throw error;
  }
};

export const placeBet = async (betSum, amount) => {
  try {
    const response = await api.post('/bet', { bet_sum: betSum, amount });
    return response.data;
  } catch (error) {
    console.error('Error placing bet:', error);
    throw error;
  }
};

export const addToPortfolio = async (betSum, amount) => {
  try {
    const response = await api.post('/portfolio/add', { bet_sum: betSum, amount });
    return response.data;
  } catch (error) {
    console.error('Error adding to portfolio:', error);
    throw error;
  }
};

export const removeFromPortfolio = async (betSum) => {
  try {
    const response = await api.post(`/portfolio/remove/${betSum}`);
    return response.data;
  } catch (error) {
    console.error('Error removing from portfolio:', error);
    throw error;
  }
};

export const clearPortfolio = async () => {
  try {
    const response = await api.post('/portfolio/clear');
    return response.data;
  } catch (error) {
    console.error('Error clearing portfolio:', error);
    throw error;
  }
};

export const getPortfolio = async () => {
  try {
    const response = await api.get('/portfolio');
    return response.data;
  } catch (error) {
    console.error('Error getting portfolio:', error);
    throw error;
  }
};

export const getRiskMetrics = async () => {
  try {
    const response = await api.get('/portfolio/risk');
    return response.data;
  } catch (error) {
    console.error('Error getting risk metrics:', error);
    throw error;
  }
};

export const getAIAdvice = async () => {
  try {
    const response = await api.get('/strategy/advice');
    return response.data;
  } catch (error) {
    console.error('Error getting AI advice:', error);
    throw error;
  }
};

export const changeStrategy = async (strategy) => {
  try {
    const response = await api.post(`/strategy/change/${strategy}`);
    return response.data;
  } catch (error) {
    console.error('Error changing strategy:', error);
    throw error;
  }
};

export const getAnalytics = async () => {
  try {
    const response = await api.get('/analytics');
    return response.data;
  } catch (error) {
    console.error('Error getting analytics:', error);
    throw error;
  }
};

export default api;
