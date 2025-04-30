import math

class TicTacToe:

    #Creates a 3x3 board and tracks current winner
    def __init__(self):
        # Initialize the board with empty spaces
        self.board = [' ' for _ in range(9)]
        # Human player is 'X', computer is 'O'
        self.current_winner = None

    
    def print_board(self):
       # Print the current state of the board
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Print the board with position numbers
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # Return list of available moves (indices with ' ')
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        # Check if there are empty squares left
        return ' ' in self.board

    def num_empty_squares(self):
        # Count how many empty squares remain
        return self.board.count(' ')

    def make_move(self, square, letter):
        # Make a move if the square is empty
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check if the current move caused a win
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Check diagonals
        if square % 2 == 0:  # only diagonal positions are 0, 2, 4, 6, 8
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # top-left to bottom-right
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # top-right to bottom-left
            if all([spot == letter for spot in diagonal2]):
                return True
        return False
# End of Class


def minimax(position, depth, max_player, alpha=-math.inf, beta=math.inf):
    # Minimax algorithm with alpha-beta pruning for optimal moves
    #position: the current game state
    # depth: how deep in the state space tree
    # max_player: computer turn
    # alpha: best already explored option for maximizer
    # beta: best already explored option for minimizer
    
    # Base cases - return score if game is over
    '''
        If human ('X') wins: returns negative score (bad for computer)
        If computer ('O') wins: returns positive score (good for computer)
        If tie: returns 0
    '''
    if position.current_winner == 'X':  # human player
        return {'position': None, 'score': -1 * (position.num_empty_squares() + 1)}
    elif position.current_winner == 'O':  # computer
        return {'position': None, 'score': 1 * (position.num_empty_squares() + 1)}
    elif not position.empty_squares():  # tie
        return {'position': None, 'score': 0}

    if max_player:  # Computer's turn (maximizing player)
        
        best = {'position': None, 'score': -math.inf}
        for possible_move in position.available_moves(): # for each move
            # Simulate making this move
            position.make_move(possible_move, 'O')
            sim_score = minimax(position, depth+1, False, alpha, beta) # Recursive calling
            
            # Undo the move (backtracking)
            position.board[possible_move] = ' '
            position.current_winner = None
            
            sim_score['position'] = possible_move
            if sim_score['score'] > best['score']: # If Maximum score
                best = sim_score  # updating best
            
            # Alpha-beta pruning
            alpha = max(alpha, best['score'])
            if beta <= alpha:
                break # pruned
        return best
    
    else:  # Human's turn (minimizing player)
        
        best = {'position': None, 'score': math.inf}
        for possible_move in position.available_moves():
            # Simulate making this move
            position.make_move(possible_move, 'X')
            sim_score = minimax(position, depth+1, True, alpha, beta) # Recursive calling
            
            # Undo the move
            position.board[possible_move] = ' '
            position.current_winner = None
            
            sim_score['position'] = possible_move
            if sim_score['score'] < best['score']: # If Minimum score
                best = sim_score # update best
            
            # Alpha-beta pruning
            beta = min(beta, best['score'])
            if beta <= alpha: 
                break # pruned
        return best
# End of minimax()


def play(game, x_player, o_player, print_game=True):
    # Main game loop
    if print_game:
        game.print_board_nums() # Initial set-up

    letter = 'X'  # Sets human player: X goes first
    
    while game.empty_squares(): # Until there no empty place
        if letter == 'X':
            # Human player's turn
            square = None
            while square is None:
                try:
                    square = int(input(f"{letter}'s turn. Input move (0-8): "))
                    if square not in game.available_moves(): # Checking for validity of move
                        print("Invalid move. Try again.")
                        square = None
                except ValueError:
                    print("Please enter a number between 0-8.")
        else:
            # Computer's turn (AI)
            # Minimax algorithm to determine the optimal move
            square = minimax(game, 0, True)['position'] # Returns a dictionary with best move
            print(f"Computer ({letter}) plays on square {square}")

        if game.make_move(square, letter): # Making a move
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print('')  # empty line: visual spacing

            if game.current_winner: # Checking winner
                if print_game:
                    print(f"{letter} wins!")
                return letter

            # Switch players
            letter = 'O' if letter == 'X' else 'X'

    if print_game: # Tie
        print("It's a tie!")
    return None
# End of play()


if __name__ == '__main__':
    print("Welcome to Tic Tac Toe!")
    print("Positions are numbered as follows:")
    print("| 0 | 1 | 2 |")
    print("| 3 | 4 | 5 |")
    print("| 6 | 7 | 8 |")
    print("You are X, and the computer is O.")
    
    while True:
        game = TicTacToe() # Declaring game object
        play(game, 'human', 'computer')
        
        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break
