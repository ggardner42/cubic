import collections
import itertools

State = collections.namedtuple('State', 'board turn')
class Triple(collections.namedtuple('Triple', 'ws')):
    __slots__ = ()

    def __str__(self):
        return '(%2d, %2d, %2d)' % (self.ws[0], self.ws[1], self.ws[2])
    def __repr__(self):
        return str(self)


# Check the winners visually
# part of class from cubic.py
class TicTacToe:
    def __init__(self):
        self.state = State(' '*64, 'X')
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


# winner_check determines if the 4 points line in a line
# (i,i,i,i) in a straight line, and (0,1,2,3) and (3,2,1,0) for diagonals
winner_check = [(i,i,i,i) for i in range(4)] + [(0,1,2,3), (3,2,1,0)]

# find all points that lie in a line (a winning combo)
# by considering all combos of 4 points from (0,0,0,0) to (3,3,3,3)
# and testing with winner_check to see if the points are on a line
winners = set()
for cs in itertools.combinations(((x,y,z) for x in range(4) for y in range(4) for z in range(4)), 4):
    scs = tuple(cs)
    xs,ys,zs = zip(*scs)
    if all(wc in winner_check for wc in (xs,ys,zs)):
        ncs = tuple(TicTacToe.zyx2i(None, (z,y,x)) for x,y,z in scs)
        winners.add(ncs)

if True:
    # print out the 4-tuple version of winners
    print('len(winners):', len(winners))
    print('winners = [')
    for ws in sorted(winners):
        print('   ', ws, ',')
    print(']')
    exit(0)

# now that we have winners as a set of 4-tuple,
# figure out winners for each point in the cube
def mktrips(c):
    ts = set()
    for ws in winners:
        if c in ws:
            ts.add(Triple(tuple(sorted([w for w in ws if w != c]))))
    return tuple(sorted(ts))

# now create Triples: those cells that make a winner for some cell
winners = [mktrips(i) for i in range(64)]

# print them out, to copy-paste into cubic.py
print('winners = [')
for ws in winners:
    print('   ', ws, ',')
print(']')

exit(0)

# print out the winners, to verify
game = TicTacToe()
i = 0
for w0,ws in enumerate(winners):
    print(w0, ws)
    for w in ws:
        win = [w0, *w.ws]
        state = State(''.join([('W' if x in win else ' ') for x in range(64)]), 'X')
        print('===============================', i := i+1)
        print('index =', w0, tuple(reversed(game.i2xyz(w0))), '|', w.ws, [tuple(reversed(game.i2xyz(c))) for c in w.ws])
        game.print_board(win, state)
