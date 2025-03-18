import os
import json
import requests
import openai
import re
from dotenv import load_dotenv

load_dotenv()

class AIClient:
    """Base class for AI API clients"""
    def get_prediction(self, game_state):
        """Get prediction from AI model - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement get_prediction")

class OpenRouterClient(AIClient):
    """Client for OpenRouter API"""
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def get_prediction(self, game_state):
        """
        Get prediction from OpenRouter API.
        
        Parameters:
            game_state (dict): Current game state
            
        Returns:
            dict: Prediction including recommended sum and strategy
        """
        if not self.api_key:
            print("OpenRouter API key not found. Using fallback prediction.")
            return self._fallback_prediction(game_state)
            
        # Format the prompt
        prompt = self._format_prompt(game_state)
        
        # Prepare the request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
            "messages": [
                {"role": "system", "content": "You are an AI strategy advisor for a dice betting game."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            # Make the request
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Extract the recommendation
            recommendation = self._parse_recommendation(content)
            return recommendation
            
        except Exception as e:
            print(f"Error getting prediction from OpenRouter: {e}")
            return self._fallback_prediction(game_state)
    
    def _format_prompt(self, game_state):
        """Format the prompt for the AI model."""
        money = game_state['money']
        bet_history = game_state['bet_history'][-10:] if game_state['bet_history'] else []
        trend = game_state['trend']
        probabilities = game_state['probabilities']
        
        # Calculate win rate
        win_rate = bet_history.count("win") / len(bet_history) if bet_history else 0
        
        prompt = f"""
        As an AI strategy advisor for a dice betting game, analyze the current game state and recommend a betting strategy.
        
        Current Game State:
        - Bankroll: ${money:.2f}
        - Market Trend: {trend.upper()}
        - Recent Results: {', '.join(bet_history) if bet_history else 'No history yet'}
        - Win Rate: {win_rate:.2%}
        
        Current Probabilities:
        """
        
        for sum_value, prob in probabilities.items():
            prompt += f"- Sum {sum_value}: {prob*100:.2f}%\n"
            
        prompt += """
        Available Strategies:
        - masaniello: Adjusts stake based on bankroll
        - martingale: Doubles stake after each loss
        - fibonacci: Uses Fibonacci sequence for stakes
        - dalembert: Increases stake by 1 unit after loss, decreases by 1 after win
        - percentage: Bets a fixed percentage of bankroll
        - kelly: Uses Kelly Criterion for optimal bet sizing
        - fixed: Uses a fixed stake amount
        
        Please provide:
        1. Recommended sum to bet on (2-12)
        2. Recommended betting strategy
        3. Brief reasoning for your recommendation
        
        Format your response as JSON:
        {
            "recommended_sum": 7,
            "recommended_strategy": "masaniello",
            "reasoning": "Your reasoning here"
        }
        """
        
        return prompt
    
    def _parse_recommendation(self, content):
        """Parse the recommendation from the AI response."""
        try:
            # Try to extract JSON from the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                recommendation = json.loads(json_str)
                
                # Validate the recommendation
                if "recommended_sum" in recommendation and "recommended_strategy" in recommendation:
                    return recommendation
            
            # If JSON parsing fails, try to extract information from text
            recommendation = {
                "recommended_sum": 7,  # Default to 7 (most common sum)
                "recommended_strategy": "percentage",  # Default to percentage (safest)
                "reasoning": "Unable to parse AI response. Using default recommendation."
            }
            
            # Try to find the recommended sum
            sum_match = re.search(r"recommended_sum[\"']?\s*:\s*(\d+)", content)
            if sum_match:
                recommendation["recommended_sum"] = int(sum_match.group(1))
                
            # Try to find the recommended strategy
            strategy_match = re.search(r"recommended_strategy[\"']?\s*:\s*[\"'](\w+)[\"']", content)
            if strategy_match:
                recommendation["recommended_strategy"] = strategy_match.group(1)
                
            # Try to find the reasoning
            reasoning_match = re.search(r"reasoning[\"']?\s*:\s*[\"']([^\"']+)[\"']", content)
            if reasoning_match:
                recommendation["reasoning"] = reasoning_match.group(1)
                
            return recommendation
            
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._fallback_prediction(None)
    
    def _fallback_prediction(self, game_state):
        """Provide a fallback prediction when API fails."""
        if game_state:
            # Simple heuristic: recommend the sum with highest expected value
            probabilities = game_state['probabilities']
            payouts = {
                2: 36, 3: 18, 4: 12, 5: 9, 6: 7, 7: 6, 8: 7, 9: 9, 10: 12, 11: 18, 12: 36
            }
            
            expected_values = {sum_val: prob * payouts[sum_val] for sum_val, prob in probabilities.items()}
            recommended_sum = max(expected_values, key=expected_values.get)
            
            # Choose strategy based on bankroll
            money = game_state['money']
            if money < 50:
                strategy = "percentage"
                reasoning = "Low bankroll detected. Using percentage strategy to preserve capital."
            elif money < 150:
                strategy = "masaniello"
                reasoning = "Medium bankroll detected. Using masaniello for balanced risk."
            else:
                strategy = "kelly"
                reasoning = "High bankroll detected. Using kelly criterion for optimal growth."
        else:
            # Default values if no game state is provided
            recommended_sum = 7
            strategy = "percentage"
            reasoning = "Using fallback prediction with default values."
            
        return {
            "recommended_sum": recommended_sum,
            "recommended_strategy": strategy,
            "reasoning": reasoning
        }

class DeepSeekClient(AIClient):
    """Client for DeepSeek API"""
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_KEY")
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        else:
            self.client = None
            print("DeepSeek API key not found. Client will use fallback prediction.")
        
    def get_prediction(self, game_state):
        """
        Get prediction from DeepSeek API.
        
        Parameters:
            game_state (dict): Current game state
            
        Returns:
            dict: Prediction including recommended sum and strategy
        """
        if not self.client:
            print("DeepSeek client not initialized. Using fallback prediction.")
            return self._fallback_prediction(game_state)
            
        # Format the prompt
        prompt = self._format_prompt(game_state)
        
        try:
            print("Attempting to use DeepSeek API...")
            # Make the request
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are an AI strategy advisor for a dice betting game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse the response
            content = response.choices[0].message.content
            print("DeepSeek API response received successfully")
            
            # Extract the recommendation
            recommendation = self._parse_recommendation(content)
            return recommendation
            
        except Exception as e:
            print(f"Error getting prediction from DeepSeek: {str(e)}")
            print("Using fallback prediction due to DeepSeek API error")
            return self._fallback_prediction(game_state)
    
    def _format_prompt(self, game_state):
        """Format the prompt for the AI model."""
        money = game_state['money']
        bet_history = game_state['bet_history'][-10:] if game_state['bet_history'] else []
        trend = game_state['trend']
        probabilities = game_state['probabilities']
        
        # Calculate win rate
        win_rate = bet_history.count("win") / len(bet_history) if bet_history else 0
        
        prompt = f"""
        As an AI strategy advisor for a dice betting game, analyze the current game state and recommend a betting strategy.
        
        Current Game State:
        - Bankroll: ${money:.2f}
        - Market Trend: {trend.upper()}
        - Recent Results: {', '.join(bet_history) if bet_history else 'No history yet'}
        - Win Rate: {win_rate:.2%}
        
        Current Probabilities:
        """
        
        for sum_value, prob in probabilities.items():
            prompt += f"- Sum {sum_value}: {prob*100:.2f}%\n"
            
        prompt += """
        Available Strategies:
        - masaniello: Adjusts stake based on bankroll
        - martingale: Doubles stake after each loss
        - fibonacci: Uses Fibonacci sequence for stakes
        - dalembert: Increases stake by 1 unit after loss, decreases by 1 after win
        - percentage: Bets a fixed percentage of bankroll
        - kelly: Uses Kelly Criterion for optimal bet sizing
        - fixed: Uses a fixed stake amount
        
        Please provide:
        1. Recommended sum to bet on (2-12)
        2. Recommended betting strategy
        3. Brief reasoning for your recommendation
        
        Format your response as JSON:
        {
            "recommended_sum": 7,
            "recommended_strategy": "masaniello",
            "reasoning": "Your reasoning here"
        }
        """
        
        return prompt
    
    def _parse_recommendation(self, content):
        """Parse the recommendation from the AI response."""
        try:
            # Try to extract JSON from the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                recommendation = json.loads(json_str)
                
                # Validate the recommendation
                if "recommended_sum" in recommendation and "recommended_strategy" in recommendation:
                    return recommendation
            
            # If JSON parsing fails, try to extract information from text
            recommendation = {
                "recommended_sum": 7,  # Default to 7 (most common sum)
                "recommended_strategy": "percentage",  # Default to percentage (safest)
                "reasoning": "Unable to parse AI response. Using default recommendation."
            }
            
            # Try to find the recommended sum
            sum_match = re.search(r"recommended_sum[\"']?\s*:\s*(\d+)", content)
            if sum_match:
                recommendation["recommended_sum"] = int(sum_match.group(1))
                
            # Try to find the recommended strategy
            strategy_match = re.search(r"recommended_strategy[\"']?\s*:\s*[\"'](\w+)[\"']", content)
            if strategy_match:
                recommendation["recommended_strategy"] = strategy_match.group(1)
                
            # Try to find the reasoning
            reasoning_match = re.search(r"reasoning[\"']?\s*:\s*[\"']([^\"']+)[\"']", content)
            if reasoning_match:
                recommendation["reasoning"] = reasoning_match.group(1)
                
            return recommendation
            
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._fallback_prediction(None)
    
    def _fallback_prediction(self, game_state):
        """Provide a fallback prediction when API fails."""
        if game_state:
            # Simple heuristic: recommend the sum with highest expected value
            probabilities = game_state['probabilities']
            payouts = {
                2: 36, 3: 18, 4: 12, 5: 9, 6: 7, 7: 6, 8: 7, 9: 9, 10: 12, 11: 18, 12: 36
            }
            
            expected_values = {sum_val: prob * payouts[sum_val] for sum_val, prob in probabilities.items()}
            recommended_sum = max(expected_values, key=expected_values.get)
            
            # Choose strategy based on bankroll
            money = game_state['money']
            if money < 50:
                strategy = "percentage"
                reasoning = "Low bankroll detected. Using percentage strategy to preserve capital."
            elif money < 150:
                strategy = "masaniello"
                reasoning = "Medium bankroll detected. Using masaniello for balanced risk."
            else:
                strategy = "kelly"
                reasoning = "High bankroll detected. Using kelly criterion for optimal growth."
        else:
            # Default values if no game state is provided
            recommended_sum = 7
            strategy = "percentage"
            reasoning = "Using fallback prediction with default values."
            
        return {
            "recommended_sum": recommended_sum,
            "recommended_strategy": strategy,
            "reasoning": reasoning
        }
