class TicTacToeEnv:
    """
    TicTacToeEnv represents the game board and logic.

    Attributes:
        board (list of str): A list representing the 3x3 game board.
        current_winner (str or None): The winner of the game if any.
    """

    def __init__(self):
        """
        Initializes a new tic-tac-toe game environment.
        """
        
        #initialize empty string list for board there are nine slots for the 3x3 grid
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def available_moves(self):
        """
        Returns a list of valid actions on the current board.

        Returns:
            list of int: The indices of the empty slots on the board.
        """
        
        #find all indices containing a space character return these indices as a list of integers
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        """
        Checks if there are any empty squares remaining to be played.

        Returns:
            bool: True if empty squares exist, False otherwise.
        """
        
        #check if a space character exists in board return the boolean result of this evaluation
        return ' ' in self.board

    def num_empty_squares(self):
        """
        Counts the number of empty squares remaining.

        Returns:
            int: The total count of empty squares.
        """
        
        #count the occurrences of space characters return the total integer count
        return self.board.count(' ')

    def make_move(self, square, letter):
        """
        Places a letter on the board at the given square.

        Args:
            square (int): The index where the letter should be placed.
            letter (str): The letter representing the current player.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        
        #validate if the designated square is empty update the board and check for a winner
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        """
        Determines if the most recent move resulted in a win.

        Args:
            square (int): The index of the most recent move.
            letter (str): The letter of the player who made the move.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        
        #calculate the row index for the move check if all elements in the row match
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True

        #calculate the column index for the move check if all elements in the column match
        col_ind = square % 3
        col = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in col]):
            return True

        #check if the square lies on the main diagonal verify if diagonal elements match the letter
        if square % 2 == 0:
            diagonal1 = [self.board[0], self.board[4], self.board[8]]
            if all([s == letter for s in diagonal1]):
                return True
            #extract the antidiagonal elements from board verify if antidiagonal elements match
            diagonal2 = [self.board[2], self.board[4], self.board[6]]
            if all([s == letter for s in diagonal2]):
                return True

        #return false if no winning condition met this applies when all checks above fail
        return False

    def get_state_key(self):
        """
        Returns a string representation of the board for state tracking.

        Returns:
            str: The joined string of the game board.
        """
        
        #join the current board into string return string as unique state representation
        return "".join(self.board)

    def evaluate(self, ai_player):
        """
        Evaluates the board state and returns a score (+10, -10, 0).

        Args:
            ai_player (str): The letter representing the ai player.

        Returns:
            int: The score of the current board state.
        """
        
        #assign positive logic score for ai victory assign negative score if opponent wins game
        if self.current_winner == ai_player:
            return 10
        elif self.current_winner:
            return -10
        
        #return zero if there is no winner this indicates a draw or ongoing game
        return 0

    def reset(self):
        """
        Resets the board to the initial empty state.
        """
        
        #reset the board array to empty spaces reset the current winner to none
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
