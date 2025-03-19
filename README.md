# 🎲📈 DiceTrader: AI-Powered Financial Dice Simulator

Welcome to the DiceTrader, a Python game that combines dice rolling, betting, and advanced risk management strategies. This project is designed to be both fun and educational, with a focus on simulating market-like dynamics in an interactive way.

---

<table>
  <tr>
    <td><img src="https://raw.githubusercontent.com/FaustoS88/Dicetrader-/main/assets/Image1.png" alt="Game Interface" width="400"></td>
    <td><img src="https://raw.githubusercontent.com/FaustoS88/Dicetrader-/main/assets/Image2.png" alt="Portfolio Management" width="400"></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><img src="https://raw.githubusercontent.com/FaustoS88/Dicetrader-/main/assets/Image3.png" alt="Analytics Dashboard" width="800"></td>
  </tr>
</table>

## 📚 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Game Rules](#-game-rules)
- [Probability and Payouts](#-probability-and-payouts)
- [Betting Strategies](#-betting-strategies)
- [AI Integration](#-ai-integration)
- [Advanced Features](#-advanced-features)
- [How to Play](#-how-to-play)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The DiceTrader is a Python-based game where players bet on the outcome of rolling two six-sided dice. The game includes:

- **Betting Mechanics**: Players can bet on the sum of two dice (2 to 12)
- **Probability Calculations**: The game displays the probability of each sum
- **Payouts**: Higher payouts for less likely sums, lower payouts for more likely sums
- **Risk Management**: Multiple betting strategies to manage bankroll
- **Market Simulation**: Dynamic trends and volatility that affect probabilities
- **AI Integration**: Real-time strategy recommendations from AI advisor

---

## ✨ Key Features

### 🎲 Core Gameplay
- Bet on dice sums (2-12) with dynamic payouts
- Multiple rounds with bankroll management
- Real-time probability calculations

### 📈 Market Simulation
- Dynamic market trends (bull/bear)
- Market volatility affecting outcomes
- Simulated financial news events

### 🧠 AI Strategy Advisor
- Personalized betting recommendations
- Strategy suggestions based on market conditions
- Reinforcement learning for optimal decisions
- Powered by Gemini 2.0 via OpenRouter API

### 💼 Portfolio Management
- Multiple simultaneous bets
- Risk analysis and expected returns
- Portfolio diversification

### 📊 Analytics Dashboard
- Performance tracking with key metrics
- Visual representations of betting history
- Sum profitability analysis

---

## 🎮 Game Rules

1. **Starting Money**: The player starts with $100
2. **Betting**: Choose a sum (2-12) and wager amount
3. **Dice Roll**: The game rolls two dice and calculates the sum
4. **Winning**: If your bet matches the dice sum, win bet × payout
5. **Losing**: If your bet doesn't match, lose your wager
6. **Game Over**: Continue until you run out of money or quit

---

## 📊 Probability and Payouts

| Sum | Ways to Roll | Probability | Payout |
|-----|--------------|-------------|--------|
| 2   | 1            | 2.78%       | 36x    |
| 3   | 2            | 5.56%       | 18x    |
| 4   | 3            | 8.33%       | 12x    |
| 5   | 4            | 11.11%      | 9x     |
| 6   | 5            | 13.89%      | 7x     |
| 7   | 6            | 16.67%      | 6x     |
| 8   | 5            | 13.89%      | 7x     |
| 9   | 4            | 11.11%      | 9x     |
| 10  | 3            | 8.33%       | 12x    |
| 11  | 2            | 5.56%       | 18x    |
| 12  | 1            | 2.78%       | 36x    |

---

## 📈 Betting Strategies

### 1. Masaniello Strategy
- **Risk Level**: Moderate
- **Approach**: Adjusts stake based on bankroll and previous results
- **Best For**: Balanced play with moderate risk

### 2. Martingale Strategy
- **Risk Level**: High
- **Approach**: Doubles stake after each loss to recover previous losses
- **Best For**: Players with large bankrolls willing to take risks

### 3. Fibonacci Strategy
- **Risk Level**: High
- **Approach**: Uses Fibonacci sequence to determine stake after losses
- **Best For**: Progressive recovery with somewhat controlled risk

### 4. D'Alembert Strategy
- **Risk Level**: Moderate
- **Approach**: Increases stake by 1 unit after loss, decreases by 1 after win
- **Best For**: More conservative alternative to Martingale

### 5. Percentage Strategy
- **Risk Level**: Low
- **Approach**: Bets a fixed percentage of current bankroll
- **Best For**: Bankroll preservation and steady play

### 6. Kelly Criterion
- **Risk Level**: Moderate
- **Approach**: Calculates optimal bet size based on odds and probability
- **Best For**: Mathematically optimal long-term growth

### 7. Fixed Stake
- **Risk Level**: Low
- **Approach**: Always bets the same amount
- **Best For**: Beginners and conservative players

---

## 🧠 AI Integration

### AI Strategy Advisor
- **Personalized Recommendations**: Suggests optimal sums to bet on
- **Strategy Selection**: Recommends the most appropriate betting strategy
- **Reasoning Explanation**: Provides clear rationale for its recommendations
- **Adaptive Learning**: Improves over time through reinforcement learning

### Reinforcement Learning System

#### State Representation
- **Bankroll Level**: Categorized as low/medium/high
- **Market Trend**: Current trend (bull/bear)
- **Streak Analysis**: Winning/losing streak tracking
- **Win Rate**: Recent win percentage

#### Learning Process
- **Q-Learning**: Updates Q-values after each bet
- **Reward System**: Positive/negative rewards tied to actual profit/loss
- **Exploration**: Epsilon-greedy strategy for balanced learning
- **Persistence**: Saves learned knowledge between sessions

#### Key Parameters
- **Learning Rate (α)**: 0.1 - Balances new vs existing knowledge
- **Discount Factor (γ)**: 0.95 - Values future rewards
- **Exploration Rate (ε)**: 1.0 - Ensures sufficient exploration

### Technical Implementation
- **API Integration**: Seamless connection to OpenRouter for Gemini 2.0 access
- **Fallback Mechanism**: Local prediction algorithms when API is unavailable
- **State Representation**: Sophisticated state encoding for RL model
- **Performance Tracking**: Evaluation of AI recommendation accuracy
- **Data Persistence**: Automatic saving/loading of Q-values
- **Statistical Tracking**: Win/loss counts, total profit, prediction accuracy

---

## 🚀 Advanced Features

### AI-Powered Strategy Advisor
- Analyzes betting history and performance
- Provides customized strategy recommendations
- Uses reinforcement learning models

### Market Simulation
- Dynamic probability adjustments
- Time-series models for market trends
- Bayesian probability models

### Financial Analytics
- Real-time performance tracking
- Risk-adjusted return calculations
- Interactive visualizations

---

## 🕹️ How to Play

1. **Run the Game**:
   ```bash
   python game.py
   ```

2. **Place Your Bet**:
   - Choose a sum (2-12)
   - Enter your wager amount

3. **Roll the Dice**: The game will roll and display the result

4. **Win or Lose**:
   - Match: Win payout × bet
   - No match: Lose your bet

5. **Continue or Quit**: Decide whether to play again or quit

---

## 🎮 Gameplay Example

Here's an example of what a game session might look like:

```bash
python game.py

Welcome to the DiceTrader!
You start with $100. Place your bets on the sum of two dice!

Current market trend: BULL
📰 Market optimism rises as investors flock to higher sums!
Type 'help' at any time to see available commands.
AI model loaded from /Users/dicetrader/data/q_values.json

Available strategies:
1. masaniello - Adjusts stake based on bankroll
2. martingale - Doubles stake after each loss
3. fibonacci - Uses Fibonacci sequence for stakes
4. d'alembert - Increases stake by 1 unit after loss, decreases by 1 after win
5. percentage - Bets a fixed percentage of your bankroll
6. kelly - Uses Kelly Criterion for optimal bet sizing
7. fixed - Uses a fixed stake amount
Choose a strategy (masaniello, martingale, fibonacci, dalembert, percentage, kelly, fixed): kelly
Using KELLY strategy with AI advisor

Current balance: $100.00
Current market trend: BULL
Here are the possible sums and their payouts:
Sum 2: Payout 36x (Probability: 2.15%)
Sum 3: Payout 18x (Probability: 4.30%)
Sum 4: Payout 12x (Probability: 6.45%)
Sum 5: Payout 9x (Probability: 8.60%)
Sum 6: Payout 7x (Probability: 10.75%)
Sum 7: Payout 6x (Probability: 19.35%)
Sum 8: Payout 7x (Probability: 16.13%)
Sum 9: Payout 9x (Probability: 12.90%)
Sum 10: Payout 12x (Probability: 9.68%)
Sum 11: Payout 18x (Probability: 6.45%)
Sum 12: Payout 36x (Probability: 3.23%)

Commands:
- Type a number (2-12) to bet on a single sum
- Type 'portfolio' to manage your bet portfolio
- Type 'stats' to view your performance analytics
- Type 'strategy' to change your betting strategy
- Type 'help' to see all available commands
Attempting to use DeepSeek API...
DeepSeek API response received successfully
Successfully used DeepSeek API

🧠 AI Strategy Advisor:
Recommended bet: Sum 7
Current KELLY strategy stake: $1.61
AI recommends KELLY strategy with stake: $1.61
Reasoning: The sum 7 has the highest probability of occurring at 19.35%, making it the most statistically favorable bet. The Kelly Criterion is recommended because it optimizes bet sizing based on the probability of winning and the current bankroll, ensuring long-term growth while minimizing risk. This is particularly suitable given the BULL market trend, which suggests a favorable environment for growth-oriented strategies.

Enter your choice (2-12 for bet, or command): 7

Betting options for sum 7:
1. Use your KELLY strategy stake: $1.61
2. Use AI recommended stake: $1.61 (AI also recommends this sum)
3. Enter a custom stake amount
Choose your stake option (1-3): 2
Using AI recommended stake: $1.61

The dice rolled a 7!
Congratulations! You won $9.68!
Winning bets:
Sum 7: $9.68
AI model saved to /Users/user/dicetrader/data/q_values.json

Do you want to play again? (yes/no): yes

Current balance: $109.68
Current market trend: BULL
Here are the possible sums and their payouts:
Sum 2: Payout 36x (Probability: 2.15%)
Sum 3: Payout 18x (Probability: 4.30%)
Sum 4: Payout 12x (Probability: 6.45%)
Sum 5: Payout 9x (Probability: 8.60%)
Sum 6: Payout 7x (Probability: 10.75%)
Sum 7: Payout 6x (Probability: 19.35%)
Sum 8: Payout 7x (Probability: 16.13%)
Sum 9: Payout 9x (Probability: 12.90%)
Sum 10: Payout 12x (Probability: 9.68%)
Sum 11: Payout 18x (Probability: 6.45%)
Sum 12: Payout 36x (Probability: 3.23%)

Commands:
- Type a number (2-12) to bet on a single sum
- Type 'portfolio' to manage your bet portfolio
- Type 'stats' to view your performance analytics
- Type 'strategy' to change your betting strategy
- Type 'help' to see all available commands
Attempting to use DeepSeek API...
DeepSeek API response received successfully
Successfully used DeepSeek API

🧠 AI Strategy Advisor:
Recommended bet: Sum 7
Current KELLY strategy stake: $1.77
AI recommends KELLY strategy with stake: $1.77
Reasoning: The sum 7 has the highest probability (19.35%) of occurring, making it the most statistically favorable bet. The Kelly Criterion is recommended because it optimizes bet sizing based on the probability of winning and the current bankroll, ensuring long-term growth while minimizing risk. Given the 100% win rate and BULL market trend, the Kelly Criterion will help capitalize on the favorable conditions while managing risk effectively.

Enter your choice (2-12 for bet, or command): stats

📊 PERFORMANCE REPORT 📊
==============================

Total Rounds: 1
Win Rate: 100.00%
Average Win: $1.61
Average Loss: $0.00
Starting Bankroll: $100.00
Current Bankroll: $109.68
Profit/Loss: $9.68
Sharpe Ratio: 0.10
Maximum Drawdown: 0.00%

Most Profitable Sums:
Sum 7: $1.61

Least Profitable Sums:
Sum 7: $1.61


Analytics data and plots have been saved:
Data: /Users/user/Documents/dicetrader/analytics/analytics_data_20250318_214648.json
Plot: /Users/user/Documents/dicetrader/analytics/bankroll_20250318_214647.png
Plot: /Users/user/Documents/dicetrader/analytics/win_loss_20250318_214647.png
Plot: /Users/user/Documents/dicetrader/analytics/trend_returns_20250318_214647.png

Press Enter to continue...
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FaustoS88/dicetrader.git
   ```

2. Navigate to the project directory:
   ```bash
   cd dicetrader
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up API access (optional):
   - Create a .env file in the project root
   - Add your OpenRouter API key: OPENROUTER_API_KEY=your_api_key_here
   - Add yout Deepseek API key: DEEPSEEK_KEY=your_deepseek_api_key

---

## 📂 Project Structure

```
dicetrader/
│
├── game.py                 # Main game script
├── README.md               # Project documentation
├── LICENSE                 # License file
├── requirements.txt        # Dependencies
│
├── strategies/             # Betting strategy implementations
│   ├── masaniello.py       # Masaniello system
│   ├── martingale.py       # Martingale system
│   ├── fibonacci.py        # Fibonacci system
│   ├── dalembert.py        # D'Alembert system
│   ├── percentage.py       # Percentage betting
│   ├── kelly.py            # Kelly Criterion
│   ├── fixed.py            # Fixed stake
│   └── ai_advisor.py       # AI strategy advisor
│
├── ai_services/            # AI integration
│   └── openrouter_client.py # OpenRouter API client
│
├── RL_Agent/               # Reinforcement learning
│   └── RL_agent.py         # RL implementation
│
├── analytics/              # Analytics data storage
│   └── *.json              # Saved game analytics
│
└── analytics_dashboard.py  # Analytics visualization
```

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository
2. Create a new branch for your feature/bug fix
3. Commit your changes
4. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Have fun!
