import math
import random

class AIEngine:
    """
    AIEngine encapsulates algorithms for game decision making.

    Attributes:
        ai_letter (str): The letter assigned to the AI.
        human_letter (str): The letter assigned to the human player.
        q_table (dict): The q-learning state-action table.
        learning_rate (float): The learning rate for q-learning.
        discount_factor (float): The discount factor for q-learning.
        epsilon (float): The exploration rate for q-learning.
    """

    def __init__(self, ai_letter='O'):
        """
        Initializes the AI engine with specified letter configuration.

        Args:
            ai_letter (str): The designated letter for the ai.
        """
        
        #store letters for ai and human players initialize q-table and learning parameters
        self.ai_letter = ai_letter
        self.human_letter = 'X' if ai_letter == 'O' else 'O'
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1

    def minimax(self, state, is_maximizing, alpha=-math.inf, beta=math.inf):
        """
        Implements the recursive minimax algorithm with alphabeta pruning.

        Args:
            state (TicTacToeEnv): The current game environment.
            is_maximizing (bool): True if current turn is aiming to maximize score.
            alpha (float): best already explored option along path to root for maximizer
            beta (float): best already explored option along path to root for minimizer

        Returns:
            dict: The best move index and its corresponding score.
        """
        
        #evaluate terminal state and return dictionary the base cases include win loss or draw
        if state.current_winner:
            score = 10 if state.current_winner == self.ai_letter else -10
            return {'position': None, 'score': score * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if is_maximizing:
            #initialize best dictionary for maximizing player iterate through available moves on board
            best = {'position': None, 'score': -math.inf}
            for possible_move in state.available_moves():
                state.make_move(possible_move, self.ai_letter)
                sim_score = self.minimax(state, False, alpha, beta)
                
                #undo the simulated move and reset winner update the best score and corresponding position
                state.board[possible_move] = ' '
                state.current_winner = None
                sim_score['position'] = possible_move
                if sim_score['score'] > best['score']:
                    best = sim_score
                
                #implement alphabeta pruning for maximizing player break loop if beta is less than alpha
                alpha = max(alpha, best['score'])
                if beta <= alpha:
                    break
            return best
        
        else:
            #initialize best dictionary for minimizing player iterate through available moves on board
            best = {'position': None, 'score': math.inf}
            for possible_move in state.available_moves():
                state.make_move(possible_move, self.human_letter)
                sim_score = self.minimax(state, True, alpha, beta)
                
                #undo the simulated move and reset winner update the best score and corresponding position
                state.board[possible_move] = ' '
                state.current_winner = None
                sim_score['position'] = possible_move
                if sim_score['score'] < best['score']:
                    best = sim_score
                
                #implement alphabeta pruning for minimizing player break loop if beta is less than alpha
                beta = min(beta, best['score'])
                if beta <= alpha:
                    break
            return best

    def get_minimax_move(self, state):
        """
        Gets the optimal move using the minimax algorithm.

        Args:
            state (TicTacToeEnv): The current game environment.

        Returns:
            int: The chosen move index.
        """
        
        #call the recursive minimax method with maximizing return the position value from best dictionary
        if len(state.available_moves()) == 9:
            return random.choice([0, 2, 4, 6, 8])
        best_move = self.minimax(state, True)
        return best_move['position']

    def get_heuristic_move(self, state):
        """
        Gets a move based on predefined rule-based heuristics.
        Prioritizes: Win -> Block -> Center -> Corners -> Random Empty.

        Args:
            state (TicTacToeEnv): The current game environment.

        Returns:
            int: The chosen move index.
        """
        
        #check for immediate winning move capability simulate move and return if it wins
        for move in state.available_moves():
            state.make_move(move, self.ai_letter)
            winner = state.current_winner
            state.board[move] = ' '
            state.current_winner = None
            if winner == self.ai_letter:
                return move

        #check if human has immediate winning move simulate move and return to block opponent
        for move in state.available_moves():
            state.make_move(move, self.human_letter)
            winner = state.current_winner
            state.board[move] = ' '
            state.current_winner = None
            if winner == self.human_letter:
                return move

        #prioritize the center square if available the center square provides strategic board advantage
        if 4 in state.available_moves():
            return 4

        #prioritize corner squares over edge squares select a random available corner index
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if c in state.available_moves()]
        if available_corners:
            return random.choice(available_corners)

        #select randomly from remaining available structural moves this serves as fallback when other criteria fail
        return random.choice(state.available_moves())

    def get_q_value(self, state_key, action):
        """
        Retrieves the q-value for a specific state-action pair.

        Args:
            state_key (str): The string representation of board state.
            action (int): The move index being evaluated.

        Returns:
            float: The q-value, defaulting to zero.
        """
        
        #check if state exists within the table return corresponding initialized action value correctly
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in range(9) if state_key[a] == ' '}
        return self.q_table[state_key].get(action, 0.0)

    def train_q_learning(self, iterations=3000):
        """
        Briefly trains the q-learning model by playing against a random agent.

        Args:
            iterations (int): The number of games to simulate.
        """
        
        #import the environment to simulate learning battles local import avoids cyclical dependency during initialization
        from game_env import TicTacToeEnv
        
        #execute training loop across specified iteration count initialize variables per completely new simulation match
        for _ in range(iterations):
            env = TicTacToeEnv()
            state_history = []
            
            #simulate game until board lacks empty squares randomize whether ai begins game this sequence
            current_turn = random.choice([self.ai_letter, self.human_letter])
            while env.empty_squares():
                state_key = env.get_state_key()
                available_moves = env.available_moves()
                
                if current_turn == self.ai_letter:
                    #explore action randomly via epsilon greedy threshold or exploit learned q combinations maximally calculated
                    if random.uniform(0, 1) < self.epsilon:
                        action = random.choice(available_moves)
                    else:
                        q_values = [self.get_q_value(state_key, a) for a in available_moves]
                        max_q = max(q_values)
                        best_actions = [a for a, q in zip(available_moves, q_values) if q == max_q]
                        action = random.choice(best_actions)
                    
                    #execute selected action within simulated training space append state to memory sequence history buffer
                    env.make_move(action, self.ai_letter)
                    state_history.append((state_key, action))
                    
                    #check match conclusion and distribute respective rewards backpropagate values through recorded sequence history entries
                    if env.current_winner == self.ai_letter:
                        self._backpropagate_rewards(state_history, 1.0)
                        break
                    elif not env.empty_squares():
                        self._backpropagate_rewards(state_history, 0.5)
                        break
                    current_turn = self.human_letter
                    
                else:
                    #execute opponent random move directly upon available evaluate resulting state determining adversarial outcome conclusion
                    action = random.choice(available_moves)
                    env.make_move(action, self.human_letter)
                    if env.current_winner == self.human_letter:
                        self._backpropagate_rewards(state_history, -1.0)
                        break
                    elif not env.empty_squares():
                        self._backpropagate_rewards(state_history, 0.5)
                        break
                    current_turn = self.ai_letter

    def _backpropagate_rewards(self, state_history, final_reward):
        """
        Propagates the final reward backward through the state history.

        Args:
            state_history (list): List of (state, action) tuples.
            final_reward (float): The ultimate reward obtained.
        """
        
        #traverse recorded actions conversely calculating accumulated values apply learning decay utilizing configured engine discount multiplier
        reward = final_reward
        for state_key, action in reversed(state_history):
            current_q = self.get_q_value(state_key, action)
            new_q = current_q + self.learning_rate * (reward - current_q)
            self.q_table[state_key][action] = new_q
            reward = reward * self.discount_factor

    def get_q_learning_move(self, state, is_trained=True):
        """
        Gets a move using the q-learning model, trained or untrained.

        Args:
            state (TicTacToeEnv): The current game environment.
            is_trained (bool): Whether the model has been fully trained.

        Returns:
            int: The chosen move index.
        """
        
        #decide exploration versus exploitation utilizing boolean parameter adjust artificial exploration chance accordingly upon toggle
        effective_epsilon = self.epsilon if is_trained else 0.8
        state_key = state.get_state_key()
        available_moves = state.available_moves()

        #check threshold determining deterministic or randomized sequence selection return index corresponding random available valid board action
        if random.uniform(0, 1) < effective_epsilon:
            return random.choice(available_moves)
        
        #calculate q table maximization array iteratively across choices return index matching maximum historical expected utility output
        q_values = [self.get_q_value(state_key, a) for a in available_moves]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(available_moves, q_values) if q == max_q]
        return random.choice(best_actions)
