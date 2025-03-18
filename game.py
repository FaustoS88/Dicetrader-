import random
import importlib
from strategies.ai_advisor import AIStrategyAdvisor
from market_simulator import MarketSimulator
from analytics_dashboard import AnalyticsDashboard
from portfolio_manager import PortfolioManager
import os

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

# Dice roll function
def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

# Payout multipliers based on the probability of the sum
payouts = {
    2: 36, 3: 18, 4: 12, 5: 9,
    6: 7, 7: 6, 8: 7, 9: 9,
    10: 12, 11: 18, 12: 36
}

# Base probabilities of each sum
base_probabilities = {
    2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36,
    6: 5/36, 7: 6/36, 8: 5/36, 9: 4/36,
    10: 3/36, 11: 2/36, 12: 1/36
}

def adjust_probabilities(trend, volatility=0.1):
    """
    Adjust probabilities based on the current trend and volatility.
    :param trend: "bull" or "bear".
    :param volatility: Level of volatility (0-1).
    :return: Adjusted probabilities.
    """
    probabilities = base_probabilities.copy()
    
    # Apply trend effect
    if trend == "bull":
        for key in [7, 8, 9, 10, 11, 12]:
            probabilities[key] *= 1.5
    elif trend == "bear":
        for key in [2, 3, 4, 5, 6]:
            probabilities[key] *= 1.5
            
    # Apply volatility effect - higher volatility makes extreme outcomes more likely
    if volatility > 0.3:
        for key in [2, 3, 11, 12]:
            probabilities[key] *= (1 + volatility)
    
    # Normalize probabilities
    total = sum(probabilities.values())
    for key in probabilities:
        probabilities[key] /= total
    return probabilities

def manage_portfolio(portfolio, money, probabilities, payouts):
    """
    Manage the betting portfolio.
    
    Parameters:
        portfolio (PortfolioManager): Portfolio manager instance
        money (float): Current bankroll
        probabilities (dict): Current probabilities for each sum
        payouts (dict): Payout multipliers for each sum
    """
    while True:
        print(f"\n{Colors.BOLD}{Colors.CYAN}===== PORTFOLIO MANAGEMENT ====={Colors.RESET}")
        print(portfolio.get_portfolio_summary())
        
        # Calculate and display risk metrics
        risk_metrics = portfolio.calculate_risk_metrics(probabilities, payouts)
        print(f"\n{Colors.BOLD}Risk Analysis:{Colors.RESET}")
        print(f"Expected Return: {Colors.GREEN if risk_metrics['expected_return'] > 0 else Colors.RED}${risk_metrics['expected_return']:.2f}{Colors.RESET}")
        print(f"Maximum Loss: {Colors.RED}${risk_metrics['max_loss']:.2f}{Colors.RESET}")
        print(f"Maximum Gain: {Colors.GREEN}${risk_metrics['max_gain']:.2f}{Colors.RESET}")
        print(f"Win Probability: {Colors.CYAN}{risk_metrics['win_probability']:.2%}{Colors.RESET}")
        
        # Display available funds
        total_invested = portfolio.get_total_investment()
        available_funds = money - total_invested
        print(f"\nAvailable Funds: {Colors.GREEN}${available_funds:.2f}{Colors.RESET}")
        
        # Display options
        print("\nOptions:")
        print("1. Add position")
        print("2. Remove position")
        print("3. Clear portfolio")
        print("4. Done (return to game)")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            # Add position
            try:
                bet_sum = int(input("Enter sum to bet on (2-12): ").strip())
                if bet_sum < 2 or bet_sum > 12:
                    print("Invalid sum. Please choose a number between 2 and 12.")
                    continue
                    
                amount = float(input(f"Enter amount to bet (max ${available_funds:.2f}): ").strip())
                if amount <= 0 or amount > available_funds:
                    print(f"Invalid amount. Please enter a value between 0 and {available_funds:.2f}.")
                    continue
                    
                success = portfolio.add_position(bet_sum, amount)
                if success:
                    print(f"Added ${amount:.2f} bet on sum {bet_sum}.")
                else:
                    print(f"Portfolio is full (max {portfolio.max_positions} positions). Remove a position first.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                
        elif choice == "2":
            # Remove position
            try:
                bet_sum = int(input("Enter sum to remove from portfolio: ").strip())
                amount = portfolio.remove_position(bet_sum)
                if amount > 0:
                    print(f"Removed ${amount:.2f} bet on sum {bet_sum}.")
                else:
                    print(f"No bet found on sum {bet_sum}.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
                
        elif choice == "3":
            # Clear portfolio
            confirm = input("Are you sure you want to clear the entire portfolio? (yes/no): ").strip().lower()
            if confirm == "yes":
                portfolio.clear_portfolio()
                print("Portfolio cleared.")
                
        elif choice == "4":
            # Return to game
            return
            
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def show_help():
    """Display help information with available commands."""
    print("\n===== HELP MENU =====")
    print("Available Commands:")
    print("- Type a number (2-12) to bet on a specific sum")
    print("- Type 'portfolio' to manage your betting portfolio")
    print("- Type 'stats' to view your performance analytics")
    print("- Type 'strategy' to change your betting strategy")
    print("- Type 'help' to see this help menu")
    print("- Type 'exit' to quit the game")
    
    print("\nPress Enter to return to the game...")
    input()

def change_strategy():
    """Allow the user to change their betting strategy."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}===== CHANGE STRATEGY ====={Colors.RESET}")
    print("Available strategies:")
    print(f"1. {Colors.MAGENTA}masaniello{Colors.RESET} - Adjusts stake based on bankroll")
    print(f"2. {Colors.MAGENTA}martingale{Colors.RESET} - Doubles stake after each loss")
    print(f"3. {Colors.MAGENTA}fibonacci{Colors.RESET} - Uses Fibonacci sequence for stakes")
    print(f"4. {Colors.MAGENTA}d'alembert{Colors.RESET} - Increases stake by 1 unit after loss, decreases by 1 after win")
    print(f"5. {Colors.MAGENTA}percentage{Colors.RESET} - Bets a fixed percentage of your bankroll")
    print(f"6. {Colors.MAGENTA}kelly{Colors.RESET} - Uses Kelly Criterion for optimal bet sizing")
    print(f"7. {Colors.MAGENTA}fixed{Colors.RESET} - Uses a fixed stake amount")
    
    strategy_name = input("\nChoose a strategy (masaniello, martingale, fibonacci, dalembert, percentage, kelly, fixed): ").strip().lower()
    try:
        if strategy_name == "dalembert":
            strategy_name = "dalembert"  # Normalize name for import
        
        strategy_module = importlib.import_module(f"strategies.{strategy_name}")
        strategy = strategy_module.__dict__[strategy_name]
        print(f"\nStrategy changed to {Colors.BOLD}{Colors.MAGENTA}{strategy_name.upper()}{Colors.RESET}")
        return strategy_name, strategy
    except (ImportError, KeyError):
        print("Invalid strategy. No changes made.")
        return None, None

def main():
    money = 100
    bet_history = []
    
    # Initialize market simulator
    market_sim = MarketSimulator(volatility=0.2, trend_strength=0.6)
    trend = market_sim.current_trend
    
    # Initialize analytics dashboard
    analytics = AnalyticsDashboard()
    
    # Initialize portfolio manager
    portfolio = PortfolioManager()
    
    print(f"{Colors.BOLD}{Colors.CYAN}Welcome to the DiceTrader!{Colors.RESET}")
    print(f"You start with {Colors.GREEN}${money}{Colors.RESET}. Place your bets on the sum of two dice!")
    print(f"\nCurrent market trend: {Colors.YELLOW if trend == 'bull' else Colors.BLUE}{trend.upper()}{Colors.RESET}")
    print(f"📰 {market_sim.get_market_news()}")
    print(f"{Colors.UNDERLINE}Type 'help' at any time to see available commands.{Colors.RESET}")

    # Initialize the AI advisor - always present regardless of strategy
    ai_advisor = AIStrategyAdvisor()
    
    # Ask the player to choose a strategy
    print("\nAvailable strategies:")
    print("1. masaniello - Adjusts stake based on bankroll")
    print("2. martingale - Doubles stake after each loss")
    print("3. fibonacci - Uses Fibonacci sequence for stakes")
    print("4. d'alembert - Increases stake by 1 unit after loss, decreases by 1 after win")
    print("5. percentage - Bets a fixed percentage of your bankroll")
    print("6. kelly - Uses Kelly Criterion for optimal bet sizing")
    print("7. fixed - Uses a fixed stake amount")
    
    strategy_name = input("Choose a strategy (masaniello, martingale, fibonacci, dalembert, percentage, kelly, fixed): ").strip().lower()
    try:
        if strategy_name == "dalembert":
            strategy_name = "dalembert"  # Normalize name for import
            
        strategy_module = importlib.import_module(f"strategies.{strategy_name}")
        strategy = strategy_module.__dict__[strategy_name]
        print(f"Using {strategy_name.upper()} strategy with AI advisor")
    except (ImportError, KeyError):
        print("Invalid strategy. Defaulting to Percentage (5% of bankroll).")
        strategy_module = importlib.import_module("strategies.percentage")
        strategy = strategy_module.__dict__["percentage"]
        strategy_name = "percentage"

    round_count = 0
    while money > 0:
        round_count += 1
        
        # Get current probabilities based on market trend and volatility
        probabilities = adjust_probabilities(trend, market_sim.volatility)
        
        print(f"\nCurrent balance: {Colors.GREEN}${money:.2f}{Colors.RESET}")
        print(f"Current market trend: {Colors.YELLOW if trend == 'bull' else Colors.BLUE}{trend.upper()}{Colors.RESET}")
        print("Here are the possible sums and their payouts:")
        for key, value in payouts.items():
            print(f"Sum {key}: Payout {Colors.MAGENTA}{value}x{Colors.RESET} (Probability: {Colors.CYAN}{probabilities[key]*100:.2f}%{Colors.RESET})")

        # Show portfolio and analytics options
        print("\nCommands:")
        print("- Type a number (2-12) to bet on a single sum")
        print("- Type 'portfolio' to manage your bet portfolio")
        print("- Type 'stats' to view your performance analytics")
        print("- Type 'strategy' to change your betting strategy")
        print("- Type 'help' to see all available commands")
        
        # Always get AI advice regardless of strategy
        advice = ai_advisor.get_strategy_advice(money, bet_history, trend, probabilities)
        print(f"\n{Colors.BOLD}🧠 AI Strategy Advisor:{Colors.RESET}")
        print(f"Recommended bet: Sum {Colors.BOLD}{Colors.GREEN}{advice['recommended_sum']}{Colors.RESET}")
        
        # Calculate the stake using the recommended strategy
        recommended_stake = 0
        if advice['recommended_strategy'] == "masaniello":
            from strategies.masaniello import masaniello
            recommended_stake = masaniello(money, bet_history)
        elif advice['recommended_strategy'] == "martingale":
            from strategies.martingale import martingale
            recommended_stake = martingale(money, bet_history)
        elif advice['recommended_strategy'] == "fibonacci":
            from strategies.fibonacci import fibonacci
            recommended_stake = fibonacci(money, bet_history)
        elif advice['recommended_strategy'] == "dalembert":
            from strategies.dalembert import dalembert
            recommended_stake = dalembert(money, bet_history)
        elif advice['recommended_strategy'] == "percentage":
            from strategies.percentage import percentage
            recommended_stake = percentage(money, bet_history)
        elif advice['recommended_strategy'] == "kelly":
            from strategies.kelly import kelly
            recommended_stake = kelly(money, bet_history, probabilities[advice['recommended_sum']], payouts[advice['recommended_sum']])
        elif advice['recommended_strategy'] == "fixed":
            from strategies.fixed import fixed
            recommended_stake = fixed(money, bet_history)
        else:
            # Fallback to percentage if an invalid strategy is recommended
            from strategies.percentage import percentage
            recommended_stake = percentage(money, bet_history)
            advice['recommended_strategy'] = "percentage"
        
        # Ensure recommended stake is never zero or negative and never more than 25% of bankroll
        if recommended_stake <= 0:
            recommended_stake = max(1, money * 0.05)  # Default to 5% of bankroll
        
        # Add bankroll protection - never bet more than 25% of bankroll
        recommended_stake = min(recommended_stake, money * 0.25)
        
        # Calculate the stake using the current selected strategy
        current_stake = 0
        if strategy_name == "kelly":
            # For Kelly strategy, we need to provide probability and payout
            # We'll use the AI's recommended sum for this calculation
            bet_sum = advice['recommended_sum']
            current_stake = strategy(money, bet_history, probabilities[bet_sum], payouts[bet_sum])
        else:
            # For other strategies, just pass money and bet_history
            current_stake = strategy(money, bet_history)
        
        # Add bankroll protection for current strategy too
        current_stake = min(current_stake, money * 0.25)
        
        print(f"Current {strategy_name.upper()} strategy stake: ${current_stake:.2f}")
        print(f"AI recommends {advice['recommended_strategy'].upper()} strategy with stake: ${recommended_stake:.2f}")
        print(f"Reasoning: {advice['reasoning']}")
        
        # Get user input
        user_input = input("\nEnter your choice (2-12 for bet, or command): ").strip().lower()
        
        # Handle help command
        if user_input == 'help':
            show_help()
            continue
            
        # Handle exit command
        if user_input == 'exit':
            print(f"\nThanks for playing! You leave with ${money}.")
            show_analytics(analytics)
            break
            
        # Handle strategy change command
        if user_input == 'strategy' or user_input == 'strat':
            new_strategy_name, new_strategy = change_strategy()
            if new_strategy_name:
                strategy_name = new_strategy_name
                strategy = new_strategy
            continue
            
        # Handle portfolio management
        if user_input == 'portfolio' or user_input == 'port':
            manage_portfolio(portfolio, money, probabilities, payouts)
            continue
            
        # Handle analytics
        if user_input == 'stats' or user_input == 'stat':
            show_analytics(analytics)
            continue
            
        # Check for single letter commands that might be incomplete
        if user_input in ['s', 'p', 'h']:
            print("Did you mean:")
            if user_input == 's':
                print("- 'strategy' to change your betting strategy")
                print("- 'stats' to view your performance analytics")
            elif user_input == 'p':
                print("- 'portfolio' to manage your bet portfolio")
            elif user_input == 'h':
                print("- 'help' to see all available commands")
            
            # Ask for clarification
            clarification = input("Please type the full command: ").strip().lower()
            
            # Process the clarified command
            if clarification == 'strategy' or clarification == 'strat':
                new_strategy_name, new_strategy = change_strategy()
                if new_strategy_name:
                    strategy_name = new_strategy_name
                    strategy = new_strategy
            elif clarification == 'stats' or clarification == 'stat':
                show_analytics(analytics)
            elif clarification == 'portfolio' or clarification == 'port':
                manage_portfolio(portfolio, money, probabilities, payouts)
            elif clarification == 'help':
                show_help()
            else:
                print("Invalid command. Please try again.")
            
            continue
            
        # Handle AI recommendation
        if user_input == 'ai' or user_input == 'recommend':
            bet_sum = advice['recommended_sum']
            bet_amount = recommended_stake
            
            print(f"Following AI recommendation: Betting ${bet_amount:.2f} on sum {bet_sum} using {advice['recommended_strategy'].upper()} strategy")
            
            # Clear portfolio for single bet mode
            portfolio.clear_portfolio()
            
            # Store the current state for RL update
            old_state = ai_advisor.get_state(money, bet_history, trend)
            
            # Add to portfolio (single bet)
            portfolio.add_position(bet_sum, bet_amount)
        
        # Handle single bet
        elif user_input.isdigit():
            try:
                bet_sum = int(user_input)
                if bet_sum < 2 or bet_sum > 12:
                    print("Invalid sum. Please choose a number between 2 and 12.")
                    continue
                    
                # Clear portfolio for single bet mode
                portfolio.clear_portfolio()
                
                # Store the current state for RL update
                old_state = ai_advisor.get_state(money, bet_history, trend)
                
                # Present betting options in a clearer way
                print(f"\nBetting options for sum {bet_sum}:")
                
                # Fix for Kelly strategy which requires probability and payout parameters
                if strategy_name == "kelly":
                    # For Kelly strategy, we need to provide probability and payout
                    stake = strategy(money, bet_history, probabilities[bet_sum], payouts[bet_sum])
                    print(f"1. Use your {strategy_name.upper()} strategy stake: ${stake:.2f}")
                else:
                    # For other strategies, just pass money and bet_history
                    print(f"1. Use your {strategy_name.upper()} strategy stake: ${strategy(money, bet_history):.2f}")
                
                if bet_sum == advice['recommended_sum']:
                    print(f"2. Use AI recommended stake: ${recommended_stake:.2f} (AI also recommends this sum)")
                else:
                    print(f"2. Use AI recommended stake: ${recommended_stake:.2f} (AI recommends sum {advice['recommended_sum']})")
                    
                print("3. Enter a custom stake amount")
                
                stake_choice = input("Choose your stake option (1-3): ").strip()
                
                if stake_choice == "1":
                    bet_amount = strategy(money, bet_history)
                    print(f"Using {strategy_name.upper()} strategy stake: ${bet_amount:.2f}")
                elif stake_choice == "2":
                    bet_amount = recommended_stake
                    print(f"Using AI recommended stake: ${bet_amount:.2f}")
                else:
                    bet_amount = float(input(f"Enter your bet amount (1-{money}): "))
                    if bet_amount < 1 or bet_amount > money:
                        print("Invalid bet amount. Please try again.")
                        continue
                
                # Add to portfolio (single bet)
                portfolio.add_position(bet_sum, bet_amount)
                
            except ValueError:
                print("Invalid input. Please enter a valid command or number.")
                continue
        else:
            print("Invalid input. Please enter a valid command or number.")
            continue
            
        # Check if portfolio is empty
        if portfolio.get_total_investment() == 0:
            print("No bets placed. Please place a bet or manage your portfolio.")
            continue
            
        # Roll the dice
        dice_sum = roll_dice()
        print(f"\nThe dice rolled a {Colors.BOLD}{Colors.MAGENTA}{dice_sum}{Colors.RESET}!")
        
        # Calculate returns from portfolio
        profit_loss, winning_positions = portfolio.calculate_return(dice_sum, payouts)
        
        # Update money and bet history
        old_money = money
        money += profit_loss
        
        # Determine if this was a win or loss overall
        if profit_loss > 0:
            bet_history.append("win")
            print(f"Congratulations! You won {Colors.GREEN}${profit_loss:.2f}!")
            
            # Show winning positions
            if winning_positions:
                print(f"{Colors.GREEN}Winning bets:{Colors.RESET}")
                for bet_sum, payout in winning_positions:
                    print(f"Sum {bet_sum}: ${payout:.2f}")
                    
            reward = profit_loss  # Positive reward for winning
            win = True
        else:
            bet_history.append("loss")
            print(f"Sorry, you lost {Colors.RED}${-profit_loss:.2f}{Colors.RESET}.")
            reward = profit_loss  # Negative reward for losing
            win = False
            
        # Update analytics dashboard with the total portfolio bet
        total_bet = portfolio.get_total_investment()
        analytics.update(money, win, total_bet, dice_sum, dice_sum, trend)
        
        # Update the AI model
        new_state = ai_advisor.get_state(money, bet_history, trend)
        ai_advisor.update_q_values(old_state, dice_sum, reward, new_state)
        
        # Clear portfolio after the round
        portfolio.clear_portfolio()
        
        # Update market based on dice roll
        new_trend, trend_changed = market_sim.update_market(dice_sum)
        if trend_changed:
            trend = new_trend
            print(f"\n📈 Market Update: Trend has changed to {Colors.YELLOW if trend == 'bull' else Colors.BLUE}{trend.upper()}{Colors.RESET}!")
            print(f"📰 {market_sim.get_market_news()}")
        
        # Ask if the player wants to continue
        if money <= 0:
            print("\nYou're out of money! Game over.")
            show_analytics(analytics)
            break

        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print(f"\nThanks for playing! You leave with ${money}.")
            show_analytics(analytics)
            break

def show_analytics(analytics):
    """Display analytics report and save plots."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}" + analytics.generate_report() + f"{Colors.RESET}")
    
    # Save plots and data
    plot_files = analytics.save_plots()
    data_file = analytics.save_data()
    
    print("\nAnalytics data and plots have been saved:")
    print(f"Data: {data_file}")
    for plot in plot_files:
        print(f"Plot: {plot}")
    
    print("\nPress Enter to continue...")
    input()

if __name__ == "__main__":
    main()