import sys
import os
import numpy as np
import random
import json
import re

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rl_system.RL_agent import RLAgent

# Import the AI clients
from ai_services.openrouter_client import OpenRouterClient, DeepSeekClient

class AIStrategyAdvisor:
    def __init__(self):
        # Define possible actions (betting on different sums)
        self.actions = list(range(2, 13))  # Sums 2-12
        
        # Initialize the RL agent for local learning
        self.agent = RLAgent(self.actions, alpha_rl=0.1, gamma_rl=0.95, delta=1.0)
        
        # Load saved Q-values if they exist
        self.load_q_values()
        
        # Initialize the AI clients with fallback mechanism
        self.openrouter = OpenRouterClient()
        self.deepseek = DeepSeekClient()
        
        # Track which API was last used successfully
        self.last_successful_api = None
        
        # Track performance metrics
        self.win_count = 0
        self.loss_count = 0
        self.total_profit = 0
        
        # Track prediction accuracy
        self.predictions = []
        
    def save_q_values(self):
        """Save the Q-values to a file for persistence between sessions."""
        save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        save_path = os.path.join(save_dir, 'q_values.json')
        
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Convert tuple keys to strings for JSON serialization
        # Fix: Use self.agent.Q instead of self.agent.q_values
        serializable_q_values = {str(k): v for k, v in self.agent.Q.items()}
        
        # Save Q-values
        try:
            with open(save_path, 'w') as f:
                json.dump(serializable_q_values, f)
            print(f"AI model saved to {save_path}")
        except Exception as e:
            print(f"Error saving AI model: {e}")
    
    def load_q_values(self):
        """Load Q-values from file if it exists."""
        load_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        load_path = os.path.join(load_dir, 'q_values.json')
        
        if os.path.exists(load_path):
            try:
                with open(load_path, 'r') as f:
                    q_values = json.load(f)
                    # Convert string keys back to tuples
                    # Fix: Use self.agent.Q instead of self.agent.q_values
                    self.agent.Q = {eval(k): v for k, v in q_values.items()}
                print(f"AI model loaded from {load_path}")
            except (json.JSONDecodeError, SyntaxError, Exception) as e:
                print(f"Error loading AI model: {e}")
                # If file is corrupted, start with fresh Q-values
                pass
        
    def get_state(self, money, bet_history, trend):
        """
        Create a state representation based on current game state.
        
        Parameters:
            money (float): Current bankroll
            bet_history (list): History of wins and losses
            trend (str): Current market trend ("bull" or "bear")
            
        Returns:
            str: A string representation of the state
        """
        # Calculate win rate
        if bet_history:
            win_rate = bet_history[-10:].count("win") / len(bet_history[-10:]) if bet_history[-10:] else 0
        else:
            win_rate = 0
            
        # Categorize bankroll
        if money < 50:
            bankroll_state = "low"
        elif money < 150:
            bankroll_state = "medium"
        else:
            bankroll_state = "high"
            
        # Detect streak
        streak = 0
        streak_type = None
        if bet_history:
            streak_type = bet_history[-1]
            for result in reversed(bet_history):
                if result == streak_type:
                    streak += 1
                else:
                    break
                    
        streak_state = f"{streak_type}_{min(streak, 3)}" if streak_type else "none_0"
        
        # Combine features into a state string
        return f"{bankroll_state}_{trend}_{streak_state}_{int(win_rate*10)}"
    
    def recommend_bet(self, money, bet_history, trend, probabilities=None, epsilon=0.2):
        """
        Recommend a sum to bet on based on the current state.
        
        Parameters:
            money (float): Current bankroll
            bet_history (list): History of wins and losses
            trend (str): Current market trend
            probabilities (dict): Current probabilities for each sum
            epsilon (float): Exploration rate
            
        Returns:
            int: Recommended sum to bet on (2-12)
        """
        # Create game state dictionary
        game_state = {
            'money': money,
            'bet_history': bet_history,
            'trend': trend,
            'probabilities': probabilities
        }
        
        # Try to get prediction from API with fallback mechanism
        prediction = self._get_api_prediction(game_state)
        
        # Store the prediction for later evaluation
        self.predictions.append({
            'state': game_state,
            'prediction': prediction
        })
        
        return prediction['recommended_sum']
    
    def _get_api_prediction(self, game_state):
        """
        Get prediction from API with fallback mechanism.
        
        Parameters:
            game_state (dict): Current game state
            
        Returns:
            dict: Prediction including recommended sum and strategy
        """
        # Try the last successful API first if available
        if self.last_successful_api == "openrouter":
            try:
                prediction = self.openrouter.get_prediction(game_state)
                print("Successfully used OpenRouter API")
                self.last_successful_api = "openrouter"
                return prediction
            except Exception as e:
                print(f"OpenRouter API failed: {e}")
                # Don't return here, continue to try DeepSeek
        elif self.last_successful_api == "deepseek":
            try:
                prediction = self.deepseek.get_prediction(game_state)
                print("Successfully used DeepSeek API")
                self.last_successful_api = "deepseek"
                return prediction
            except Exception as e:
                print(f"DeepSeek API failed: {e}")
                # Don't return here, continue to try OpenRouter as fallback
        
        # If no last successful API or it failed, try both in sequence
        # First try DeepSeek since OpenRouter has payment issues
        try:
            prediction = self.deepseek.get_prediction(game_state)
            self.last_successful_api = "deepseek"
            print("Successfully used DeepSeek API")
            return prediction
        except Exception as e:
            print(f"DeepSeek API failed: {e}")
            
            try:
                prediction = self.openrouter.get_prediction(game_state)
                self.last_successful_api = "openrouter"
                print("Successfully used OpenRouter API")
                return prediction
            except Exception as e:
                print(f"OpenRouter API failed: {e}")
                
                # If both APIs fail, use local RL agent
                print("Using local RL agent for prediction")
                return self._local_prediction(game_state)
    
    def _local_prediction(self, game_state):
        """
        Generate a prediction using the local RL agent when APIs fail.
        
        Parameters:
            game_state (dict): Current game state
            
        Returns:
            dict: Prediction including recommended sum and strategy
        """
        money = game_state['money']
        bet_history = game_state['bet_history']
        trend = game_state['trend']
        probabilities = game_state['probabilities']
        
        # Get current state
        state = self.get_state(money, bet_history, trend)
        
        # Use epsilon-greedy policy to select action
        if random.random() < 0.2:  # Exploration
            recommended_sum = random.choice(self.actions)
        else:  # Exploitation
            # Get Q-values for current state
            q_values = {a: self.agent.get_q_value(state, a) for a in self.actions}
            
            # Select action with highest Q-value
            recommended_sum = max(q_values, key=q_values.get)
        
        # Choose strategy based on bankroll and trend
        if money < 50:
            strategy = "percentage"
            reasoning = "Low bankroll detected. Using percentage strategy to preserve capital."
        elif money < 150:
            if trend == "bull":
                strategy = "masaniello"
                reasoning = "Medium bankroll in bull market. Using masaniello for balanced risk."
            else:
                strategy = "dalembert"
                reasoning = "Medium bankroll in bear market. Using d'Alembert for conservative approach."
        else:
            if trend == "bull":
                strategy = "kelly"
                reasoning = "High bankroll in bull market. Using Kelly criterion for optimal growth."
            else:
                strategy = "masaniello"
                reasoning = "High bankroll in bear market. Using masaniello for balanced risk."
        
        return {
            "recommended_sum": recommended_sum,
            "recommended_strategy": strategy,
            "reasoning": reasoning + " (Local RL prediction)"
        }
    
    def update_model(self, old_state, action, reward, new_state):
        """
        Update the RL model based on the outcome of a bet.
        
        Parameters:
            old_state (str): State before the bet
            action (int): Sum that was bet on
            reward (float): Profit/loss from the bet
            new_state (str): State after the bet
        """
        # Update local RL agent
        self.agent.update(old_state, action, reward, new_state)
        
        # Update performance metrics
        if reward > 0:
            self.win_count += 1
        else:
            self.loss_count += 1
        self.total_profit += reward
        
        # Evaluate prediction accuracy if we have predictions
        if self.predictions:
            last_prediction = self.predictions[-1]
            last_prediction['actual_outcome'] = {
                'action': action,
                'reward': reward
            }
        
        # Save Q-values after update
        self.save_q_values()
    
    def update_q_values(self, old_state, action, reward, new_state):
        """
        Update Q-values based on the outcome and save to disk.
        
        Parameters:
            old_state (str): State before the bet
            action (int): Sum that was bet on
            reward (float): Profit/loss from the bet
            new_state (str): State after the bet
        """
        # Update the agent's Q-values
        self.agent.update(old_state, action, reward, new_state)
        
        # Save Q-values to disk
        self.save_q_values()
    
    def get_strategy_advice(self, money, bet_history, trend, probabilities=None):
        """
        Provide strategic advice based on current game state.
        
        Parameters:
            money (float): Current bankroll
            bet_history (list): History of wins and losses
            trend (str): Current market trend
            probabilities (dict): Current probabilities for each sum
            
        Returns:
            dict: Advice including recommended bet and reasoning
        """
        # Create game state dictionary
        game_state = {
            'money': money,
            'bet_history': bet_history,
            'trend': trend,
            'probabilities': probabilities
        }
        
        # Get prediction with fallback mechanism
        prediction = self._get_api_prediction(game_state)
        
        # Store the prediction for later evaluation
        self.predictions.append({
            'state': game_state,
            'prediction': prediction
        })
        
        return prediction