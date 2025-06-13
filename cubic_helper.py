import collections
import itertools

State = collections.namedtuple('State', 'board turn')

# taken from cubic
def zyx2c(z, y, x):
    return x * 16 + y * 4 + z

def print_board(xs, os, winner=None, isnumbering=True):
    lastx = lasto = 100
    if xs:
        lastx = xs[-1]
    if os:
        lasto = os[-1]

    # We alternate, first x, then o, so in mid-turn, x might be longer than o by 1.
    pos = os + (None,) * (len(xs) - len(os))
    xos = zip(xs, pos)

    cells = ['   ']*64
    for ii,(x,o) in enumerate(xos):
        # numbering for debugging statements
        if isnumbering:
            i = ii+1
            if i < 10:
                cells[x] = ' X%d' % i
                if o is not None:
                    cells[o] = ' O%d' % i
            else:
                cells[x] = 'X%d' % i
                if o is not None:
                    cells[o] = 'O%d' % i
        else:
            cells[x] = ' X '
            if o is not None:
                cells[o] = ' O '

    # Print the 4x4x4 board with layers side by side, with specified indexing.
    print('          0                1                2                3')
    print('    0   1   2   3    0   1   2   3    0   1   2   3    0   1   2   3')

    # Board rows with row indices
    for x in range(4):
        row_parts = [f"{x}"]  # Start with row index
        for z in range(4):  # For each layer
            row = []
            for y in range(4):
                i = zyx2c(z, y, x)
                cell = cells[i]
                if winner and i in winner:
                    cell = f"\033[33m{cell}\033[0m"  # Some color for winnng user
                else:
                    if i == lastx:
                        cell = f"\033[32m{cell}\033[0m"  # Green for user
                    elif i == lasto:
                        cell = f"\033[31m{cell}\033[0m"  # Red for computer
                row.append(cell)  # Center cell content in 4-char space
            row_parts.append("|".join(row))
        print("  ".join(row_parts))
        if x < 3:
            print('   '+ '  '.join(['+'.join(['---']*4)]*4))
    print()

# The layout, for figuring out corners, etc.
#           0                1                2                3
#     0   1   2   3    0   1   2   3    0   1   2   3    0   1   2   3
# 0   0c| 4e| 8e|12c   1e| 5s| 9s|13e   2e| 6s|10s|14e   3c| 7e|11e|15c
#    ---+---+---+---  ---+---+---+---  ---+---+---+---  ---+---+---+---
# 1  16e|20s|24s|28e  17s|21i|25i|29s  18s|22i|26i|30s  19e|23s|27s|31e
#    ---+---+---+---  ---+---+---+---  ---+---+---+---  ---+---+---+---
# 2  32e|36s|40s|44e  33s|37i|41i|45s  34s|38i|42i|46s  35e|39s|43s|47e
#    ---+---+---+---  ---+---+---+---  ---+---+---+---  ---+---+---+---
# 3  48c|52e|56e|60c  49e|53s|57s|61e  50e|54s|58s|62e  51c|55e|59e|63c
if False:
    # prints above layout of index mapped to cell
    print_board(range(64), tuple())
    exit(0)

# constructed by hand from above chart
corners = [ 0,  3, 12, 15, 48, 51, 60, 63]
edges =   [ 1,  2,  4,  7,  8, 11, 13, 14, 16, 19, 28, 31, 32, 35, 44, 47, 49, 50, 52, 55, 56, 59, 61, 62]
inners  = [21, 22, 25, 26, 37, 38, 41, 42]
surface = [ 5,  6,  9, 10, 17, 18, 20, 23, 24, 27, 29, 30, 33, 34, 36, 39, 40, 43, 45, 46, 53, 54, 57, 58]

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
        ncs = tuple(zyx2c(z,y,x) for x,y,z in scs)
        winners.add(ncs)
winners = tuple(sorted(tuple(sorted(ws)) for ws in winners))
print('winners =', winners)

if False:
    # print out the winners, to verify
    for ws in winners:
        print(ws)
        print_board(ws, tuple(), winner=ws, isnumbering=False)
