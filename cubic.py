import collections
import random

class Point(collections.namedtuple('Point', 'x y z')):
    __slots__ = ()

    def __str__(self):
        return '%d%d%d' % (self.z, self.y, self.x)
    def __repr__(self):
        return str(self)

State = collections.namedtuple('State', 'board turn depth')
Score = collections.namedtuple('Score', 'mmm yyy mm yy m b y')
ScoreSpread = collections.namedtuple('ScoreSpread', 'b m mm yy y')

MAX_SCORE = 50000
DEPTH_START = 6

score0 = Score(0, 0, 0, 0, 0, 0, 0)
my_score = dict([
    ((0, 0), Score(0, 0, 0, 0, 0, 1, 0)), # b=1
    ((0, 1), Score(0, 0, 0, 0, 0, 0, 1)), # y=1
    ((0, 2), Score(0, 0, 0, 1, 0, 0, 0)), # yy=1
    ((0, 3), Score(0, 1, 0, 0, 0, 0, 0)), # yyy=1
    ((1, 0), Score(0, 0, 0, 0, 1, 0, 0)), # m=1
    ((2, 0), Score(0, 0, 1, 0, 0, 0, 0)), # mm=1
    ((3, 0), Score(1, 0, 0, 0, 0, 0, 0)), # mmm=1
    ])

def add_my_score(ms, ys, score):
    if ms > 0 and ys > 0:
        return score
    return Score(*[x+y for x,y in zip(my_score[(ms, ys)], score)])

def parse_input(user_input):
    """Parse three-digit input into z, y, x coordinates."""
    try:
        if len(user_input) != 3:
            return None
        z, y, x = map(int, user_input)
        if not (0 <= z <= 3 and 0 <= y <= 3 and 0 <= x <= 3):
            return None
        return z, y, x
    except ValueError:
        return None


def minimax_alpha_beta(state, depth, alpha, beta, maximizing_player,
                       get_possible_moves, make_move, evaluate_state, is_terminal):
    """
    Generic minimax algorithm with alpha-beta pruning.

    Args:
        state: Current game state
        depth: Maximum search depth (0 = leaf node)
        alpha: Best value maximizing player can guarantee
        beta: Best value minimizing player can guarantee
        maximizing_player: True if current player is maximizing, False if minimizing
        get_possible_moves: Function that returns list of possible moves from state
        make_move: Function that returns new state after applying move
        evaluate_state: Function that returns numeric evaluation of state
        is_terminal: Function that returns True if state is terminal (game over)

    Returns:
        Tuple of (best_score, best_move)
    """

    #print('===================================')
    #print(depth, alpha, beta, maximizing_player)
    #game.print_board(None, state)

    # Base cases
    if depth == 0 or is_terminal(state):
        #print('TERMINAL:', depth, state)
        #game.print_board(None, state)
        return evaluate_state(state), None

    possible_moves = get_possible_moves(state, depth)
    #print('possible_moves:', possible_moves, 'depth:', depth)
    #print('possible_moves:', [Point(*game.i2xyz(i)) for i in possible_moves], 'depth:', depth)

    if maximizing_player:
        max_eval = -MAX_SCORE
        best_move = None

        for move in possible_moves:
            new_state = make_move(state, move)
            eval_score, _ = minimax_alpha_beta(new_state, depth - 1, alpha, beta, False,
                                               get_possible_moves, make_move, evaluate_state, is_terminal)
            #print('MAXING:', eval_score)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)

            # Alpha-beta pruning
            if beta <= alpha:
                break  # Beta cutoff

        return max_eval, best_move

    else:  # Minimizing player
        min_eval = MAX_SCORE
        best_move = None

        for move in possible_moves:
            new_state = make_move(state, move)
            eval_score, _ = minimax_alpha_beta(new_state, depth - 1, alpha, beta, True,
                                               get_possible_moves, make_move, evaluate_state, is_terminal)
            #print('MINING:', eval_score)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)

            # Alpha-beta pruning
            if beta <= alpha:
                break  # Alpha cutoff

        return min_eval, best_move


class TicTacToe:
    def __init__(self):
        # mapping 4x4x4 onto single array. calculated from cubic_helper.py
        self.winners = (
                ( 0,  1,  2,  3), ( 0,  4,  8, 12), ( 0,  5, 10, 15), ( 0, 16, 32, 48),
                ( 0, 17, 34, 51), ( 0, 20, 40, 60), ( 0, 21, 42, 63), ( 1,  5,  9, 13),
                ( 1, 17, 33, 49), ( 1, 21, 41, 61), ( 2,  6, 10, 14), ( 2, 18, 34, 50),
                ( 2, 22, 42, 62), ( 3,  6,  9, 12), ( 3,  7, 11, 15), ( 3, 18, 33, 48),
                ( 3, 19, 35, 51), ( 3, 22, 41, 60), ( 3, 23, 43, 63), ( 4,  5,  6,  7),
                ( 4, 20, 36, 52), ( 4, 21, 38, 55), ( 5, 21, 37, 53), ( 6, 22, 38, 54),
                ( 7, 22, 37, 52), ( 7, 23, 39, 55), ( 8,  9, 10, 11), ( 8, 24, 40, 56),
                ( 8, 25, 42, 59), ( 9, 25, 41, 57), (10, 26, 42, 58), (11, 26, 41, 56),
                (11, 27, 43, 59), (12, 13, 14, 15), (12, 24, 36, 48), (12, 25, 38, 51),
                (12, 28, 44, 60), (12, 29, 46, 63), (13, 25, 37, 49), (13, 29, 45, 61),
                (14, 26, 38, 50), (14, 30, 46, 62), (15, 26, 37, 48), (15, 27, 39, 51),
                (15, 30, 45, 60), (15, 31, 47, 63), (16, 17, 18, 19), (16, 20, 24, 28),
                (16, 21, 26, 31), (17, 21, 25, 29), (18, 22, 26, 30), (19, 22, 25, 28),
                (19, 23, 27, 31), (20, 21, 22, 23), (24, 25, 26, 27), (28, 29, 30, 31),
                (32, 33, 34, 35), (32, 36, 40, 44), (32, 37, 42, 47), (33, 37, 41, 45),
                (34, 38, 42, 46), (35, 38, 41, 44), (35, 39, 43, 47), (36, 37, 38, 39),
                (40, 41, 42, 43), (44, 45, 46, 47), (48, 49, 50, 51), (48, 52, 56, 60),
                (48, 53, 58, 63), (49, 53, 57, 61), (50, 54, 58, 62), (51, 54, 57, 60),
                (51, 55, 59, 63), (52, 53, 54, 55), (56, 57, 58, 59), (60, 61, 62, 63)
                )

        self.state = State(' '*64, 'X', tuple([0]*64))
        self.last_user_move = None
        self.last_computer_move = None

    def i2xyz(self, i):
        z = i & 3
        y = (i >> 2) & 3
        x = (i >> 4) & 3
        return (x, y, z)

    def zyx2i(self, pt):
        z, y, x = pt
        return x * 16 + y * 4 + z

    def make_move(self, state, cell):
        nturn = 'X' if state.turn == 'O' else 'O'
        ndepth = max(state.depth) + 1
        nstate = State(state.board[:cell] + state.turn + state.board[cell+1:], nturn, tuple(state.depth[:cell] + (ndepth,) + state.depth[cell+1:]))
        return nstate

    def update_state(self, cell):
        self.state = self.make_move(self.state, cell)
        self.last_computer_move = cell

    def set_opponent_move(self, coords):
        cell = self.zyx2i(coords)
        self.state = self.make_move(self.state, cell)
        self.last_user_move = cell

    def check_win(self, player):
        """Check if the given player has won."""
        for ws in sorted(self.winners):
            if all(self.state[0][w] == player for w in ws):
                #self.print_board(ws)
                return ws
        return None

    def is_board_full(self):
        """Check if the board is full."""
        cnt = sum(1 for c in self.state.board if c == ' ')
        return cnt == 0

    def print_board(self, winner=None, state=None):
        """Print the 4x4x4 board with layers side by side, with specified indexing."""
        if state == None:
            state = self.state

        print('          0                1                2                3')
        print('    0   1   2   3    0   1   2   3    0   1   2   3    0   1   2   3')

        # Board rows with row indices
        for x in range(4):
            row_parts = [f"{x}"]  # Start with row index
            for z in range(4):  # For each layer
                row = []
                for y in range(4):
                    i = self.zyx2i((z, y, x))
                    #cell = ' '+state.board[i]+' '
                    #d = self.state.depth[i]
                    cell = state.board[i]
                    if winner and i in winner:
                        cell = f" \033[33m{cell}\033[0m "  # Some color for winnng user
                    else:
                        if i == self.last_user_move:
                            cell = f" \033[32m{cell}\033[0m "  # Green for user
                        elif i == self.last_computer_move:
                            cell = f" \033[31m{cell}\033[0m "  # Red for computer
                        else:
                            cell = ' '+cell+' '
                    row.append(cell)  # Center cell content in 4-char space
                row_parts.append("|".join(row))
            print("  ".join(row_parts))
            if x < 3:
                print('   '+ '  '.join(['+'.join(['---']*4)]*4))
        print()

    def is_valid_move(self, coords):
        """Check if the move is valid."""
        z, y, x = coords
        i = self.zyx2i(coords)
        return 0 <= z < 4 and 0 <= y < 4 and 0 <= x < 4 and self.state.board[i] == ' '

    def get_possible_moves(self, state, depth):
        """Return list of empty cell coordinates, ordered by "best" move first."""
        mvs = [i for i,cell in enumerate(state.board) if cell == ' ']

        # check for done
        if not mvs:
            return mvs

        # order the moves to help minmax find something good early
        # 1. score the moves, sorted according to immediate win
        scores = []
        for mv in mvs:
            score = score0
            for ws in self.winners:
                if mv in ws:
                    ms = ys = 0
                    for w in ws:
                        if state.board[w] == state.turn:
                            ms += 1
                        elif state.board[w] != ' ':
                            ys += 1
                    score = add_my_score(ms, ys, score)
            scores.append((score, mv))
        scores = list(reversed(sorted(scores)))

        # 2. look for (almost) immediate wins.
        # if mmm > 0, that means we can win with this move.
        # if yyy > 0, that means we must block opponent with this move.
        # if mm > 2, that means we can win in two moves (we place in this spot, and we forked two winners)
        # if yy > 2, that means we must block the user from forcing a win.
        if scores[0][0].mmm > 0 or scores[0][0].yyy > 0 or scores[0][0].mm > 2 or scores[0][0].yy > 2:
            # we only care about the winning move.
            #if depth == DEPTH_START:
            #    print('***', scores[0])
            return [scores[0][1]]

        # 3. pick a move looking forward
        s0 = scores[0][0]
        ix = 0
        for i,(s,m) in enumerate(scores):
            if s0 != s:
                ix = i
                break
        nscores = scores[:ix]
        random.shuffle(nscores)
        scores = nscores + scores[ix:]
        #if depth == DEPTH_START:
        #    print('+++', scores)

        return [mv for _,mv in scores]


    def is_terminal(self, state):
        # Check for winner or draw
        for ws in self.winners:
            if state.board[ws[0]] == state.board[ws[1]] == state.board[ws[2]] == state.board[ws[3]] != ' ':
                return True
        return ' ' not in state[0]  # Draw

    def evaluate_state(self, state):
        for ws in self.winners:
            if state.board[ws[0]] == state.board[ws[1]] == state.board[ws[2]] == state.board[ws[3]]:
                if state.board[ws[0]] == 'X':
                    return 1
                elif state.board[ws[0]] == 'O':
                    return -1
        return 0  # Draw or ongoing game

    def find_best_move(self):
        score, move = minimax_alpha_beta(
            self.state, DEPTH_START, -MAX_SCORE, MAX_SCORE, self.state.turn == 'X',
            self.get_possible_moves, self.make_move, self.evaluate_state, self.is_terminal
        )
        return move

    def find_first_move(self):
        moves = self.get_possible_moves(self.state, DEPTH_START)
        return moves[0]


def main():
    print("Welcome to 4x4x4 Tic-Tac-Toe!")
    print("Enter moves as three digits (zyx, e.g., 000 or 333).")
    print("The top most row of numbers (over the planes) are z.")
    print("The row of numbers over the columns are y.")
    print("The numbers at the start of each row are x.")
    print("You are 'X', computer is 'O'.")

    def do_user_move():
        while True:
            game.print_board(None)
            user_input = input("Your move (zyx): ").strip()
            coords = parse_input(user_input)
            if coords and game.is_valid_move(coords):
                game.set_opponent_move(coords)
                return
            print("Invalid move. Use three digits (0-3 each), e.g., '123' for layer 1, row 2, column 3.")

    # avoid minmax for first move
    do_user_move()
    move = game.find_first_move()
    game.update_state(move)
    x, y, z = game.i2xyz(move)
    print(f"Computer's move: {z}{y}{x} ({move})")

    while True:
        do_user_move()

        ws = game.check_win('X')
        if ws:
            print("You win!")
            game.print_board(ws)
            break
        if game.is_board_full():
            print("It's a tie!")
            game.print_board(None)
            break

        # Computer's turn
        move = game.find_best_move()
        if move:
            game.update_state(move)
            x, y, z = game.i2xyz(move)
            print(f"Computer's move: {z}{y}{x} ({move})")

            ws = game.check_win('O')
            if ws:
                print("Computer wins!")
                game.print_board(ws)
                break
            if game.is_board_full():
                print("It's a tie!")
                game.print_board(None)
                break
        else:
            print("It's a tie!")
            game.print_board(None)
            break

if __name__ == "__main__":
    game = TicTacToe()
    main()
