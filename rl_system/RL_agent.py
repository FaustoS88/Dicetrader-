import numpy as np

class RLAgent:
    def __init__(self, actions, alpha_rl=0.1, gamma_rl=0.95, delta=1.0):
        """
        Initialize the RL agent.
        
        Parameters:
            actions (list): List of possible actions.
            alpha_rl (float): RL learning rate.
            gamma_rl (float): RL discount factor.
            delta (float): Scaling factor for incorporating Q(s,a) into the overall strategy.
        """
        self.alpha_rl = alpha_rl      # Learning rate for Q-updates.
        self.gamma_rl = gamma_rl      # Discount factor.
        self.delta = delta            # Scaling factor to adjust the influence of Q(s,a).
        self.actions = actions        # List of possible actions.
        self.Q = {}                   # Dictionary to store Q-values in the form {(state, action): value}.

    def get_Q(self, state, action):
        """Retrieve Q-value for a given state-action pair (defaulting to 0)."""
        return self.Q.get((state, action), 0.0)

    def update(self, state, action, reward, next_state):
        """
        Update Q(s,a) using the rule:
            Q(s,a) = Q(s,a) + alpha_rl * (reward + gamma_rl * max_a' Q(next_state, a') - Q(s,a))
        
        Parameters:
            state: Current state.
            action: Action taken.
            reward (float): Immediate reward received.
            next_state: Next state after taking the action.
        
        Returns:
            new_value (float): The updated Q-value.
        """
        current_value = self.get_Q(state, action)
        # Obtain maximum Q-value over all actions for the next state.
        next_Q_vals = [self.get_Q(next_state, a) for a in self.actions]
        max_next_Q = max(next_Q_vals) if next_Q_vals else 0.0
        # Perform Q-update.
        new_value = current_value + self.alpha_rl * (reward + self.gamma_rl * max_next_Q - current_value)
        # Optionally scale Q-value contribution using delta in a later integration step.
        self.Q[(state, action)] = new_value
        return new_value

    def choose_action(self, state, epsilon=0.1):
        """
        Choose an action using an epsilon-greedy policy.
        
        Parameters:
            state: Current state.
            epsilon (float): Probability of taking a random action for exploration.
        
        Returns:
            selected action.
        """
        if np.random.rand() < epsilon:
            return np.random.choice(self.actions)
        else:
            Q_vals = [self.get_Q(state, a) for a in self.actions]
            max_Q = max(Q_vals)
            # In case of ties, choose randomly among the best actions.
            best_actions = [a for a, q in zip(self.actions, Q_vals) if q == max_Q]
            return np.random.choice(best_actions)

if __name__ == "__main__":
    # Example usage:
    actions = ['buy', 'sell', 'hold']
    agent = RLAgent(actions, alpha_rl=0.1, gamma_rl=0.95, delta=1.0)
    
    # Simulated trading scenario:
    state = "bull_market"     # example state; in practice, this could be a feature vector.
    next_state = "bear_market"  # example next state.
    action = "buy"
    reward = 10  # simulated reward from taking 'buy' action in this state.
    
    print("Before update, Q({}, {}): {:.4f}".format(state, action, agent.get_Q(state, action)))
    agent.update(state, action, reward, next_state)
    print("After update, Q({}, {}): {:.4f}".format(state, action, agent.get_Q(state, action)))
    
    # Example of choosing an action:
    chosen_action = agent.choose_action(state, epsilon=0.1)
    print("Chosen action in state '{}': {}".format(state, chosen_action))