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

planes = (
        ('000', '001', '002', '003', '010', '011', '012', '013', '020', '021', '022', '023', '030', '031', '032', '033'),
        ('100', '101', '102', '103', '110', '111', '112', '113', '120', '121', '122', '123', '130', '131', '132', '133'),
        ('200', '201', '202', '203', '210', '211', '212', '213', '220', '221', '222', '223', '230', '231', '232', '233'),
        ('300', '301', '302', '303', '310', '311', '312', '313', '320', '321', '322', '323', '330', '331', '332', '333'),

        ('000', '010', '020', '030', '100', '110', '120', '130', '200', '210', '220', '230', '300', '310', '320', '330'),
        ('001', '011', '021', '031', '101', '111', '121', '131', '201', '211', '221', '231', '301', '311', '321', '331'),
        ('002', '012', '022', '032', '102', '112', '122', '132', '202', '212', '222', '232', '302', '312', '322', '332'),
        ('003', '013', '023', '033', '103', '113', '123', '133', '203', '213', '223', '233', '303', '313', '323', '333'),

        ('000', '001', '002', '003', '100', '101', '102', '103', '200', '201', '202', '203', '300', '301', '302', '303'),
        ('010', '011', '012', '013', '110', '111', '112', '113', '210', '211', '212', '213', '310', '311', '312', '313'),
        ('020', '021', '022', '023', '120', '121', '122', '123', '220', '221', '222', '223', '320', '321', '322', '323'),
        ('030', '031', '032', '033', '130', '131', '132', '133', '230', '231', '232', '233', '330', '331', '332', '333'),

        ('000', '010', '020', '030', '101', '111', '121', '131', '202', '212', '222', '232', '303', '313', '323', '333'),
        ('003', '013', '023', '033', '102', '112', '122', '132', '201', '211', '221', '231', '300', '310', '320', '330'),

        ('000', '001', '002', '003', '110', '111', '112', '113', '220', '221', '222', '223', '330', '331', '332', '333'),
        ('030', '031', '032', '033', '120', '121', '122', '123', '210', '211', '212', '213', '300', '301', '302', '303'),

        ('000', '011', '022', '033', '100', '111', '122', '133', '200', '211', '222', '233', '300', '311', '322', '333'),
        ('003', '012', '021', '030', '103', '112', '121', '130', '203', '212', '221', '230', '303', '312', '321', '330'),
        )

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
