import time

# A "winner" is a set of 4 points that make up 4 in a row.
#
# The general strategy is to look for a forced win, exhausting all possible winners that have 2 Os and 2 blanks,
# which hopefully leads to a point where I have two or more 3 Os and a blank (with the blank in common)
#
# The program first looks to see if the computer has a forced win.
# If not, it picks a cell that looks promising,
# then checks to see if the opponent has a forced win.
# If the opponent has a forced win, then the computer moves to block.
# The computer continues to pick promising cells until it stumbles on a forced win.

winners  = (
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
winners = tuple(set(ws) for ws in winners)

ordered_cells = (
        # corners
         0,  3, 12, 15, 48, 51, 60, 63,
        # inners
        21, 22, 25, 26, 37, 38, 41, 42,
        # edges
         1,  2,  4,  7,  8, 11, 13, 14, 16, 19, 28, 31, 32, 35, 44, 47, 49, 50, 52, 55, 56, 59, 61, 62,
        # surfaces
         5,  6,  9, 10, 17, 18, 20, 23, 24, 27, 29, 30, 33, 34, 36, 39, 40, 43, 45, 46, 53, 54, 57, 58,
        )

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

def zyx2c(z, y, x):
    return x * 16 + y * 4 + z

def c2xyz(c):
    z = c & 3
    y = (c >> 2) & 3
    x = (c >> 4) & 3
    return (x, y, z)

def check_win(c, cs):
    """Check if the given player has won."""
    scs = set(cs)
    for sws in winners:
        if sws <= scs:
            return sws
    return None

def is_board_full(xs, os):
    """Check if the board is full."""
    return len(xs + os) == 64

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

# XXX: TODO: Combine find_forced_win and find_opponent_forced_win
def find_forced_win(xs, os, min_len):
    #print('Entering', xs, os, min_len)
    #print_board(xs, os)

    olen = len(os)
    if olen >= min_len:
        #print('Returning due to cutoff:', olen, min_len)
        return (min_len, None) # discard

    # we are O, and second to move, so this move may fill board
    sxs = set(xs)
    sos = set(os)

    # look if we have a win
    for sws in winners:
        if len(sws & sos) == 3 and len(sws & sxs) == 0:
            o = (sws-sos).pop()
            #print('We have forced win:', sws, os, sws-sos)
            #print_board(xs, os, winner=sws)
            return (olen, o)

    # look if they have a win
    for sws in winners:
        if len(sws & sxs) == 3 and len(sws & sos) == 0:
            x = (sws-sxs).pop()
            #print('Blocking forced win:', 100+olen, sws, xs, sws-sxs)
            #print_board(xs, os, winner=sws)
            return (200, None)

    # exhaust all possible forced moves
    best_move = (min_len, None)

    for sws in winners:
        if len(sws & sos) == 2 and len(sws & sxs) == 0:
            c1, c2 = sws - sos
            for i,(x,o) in enumerate(((c1,c2), (c2,c1))):
                nxs = xs+(x,)
                nos = os+(o,)

                #print('Considering %d: X=%d, O=%d' % (i, x, o), best_move)
                #print_board(nxs, nos)

                depth, move = find_forced_win(nxs, nos, best_move[0])
                if depth < best_move[0]:
                    #print('Got new best_move:', (depth, o), 'replacing:', best_move)
                    best_move = (depth, o)

    #print('Returning:', olen, best_move)
    return best_move

def find_opponent_forced_win(xs, os):
    #print('Entering oppo', xs, os)
    #print_board(xs, os)

    # we are X, and first to move
    sxs = set(xs)
    sos = set(os)

    # look if they have a win
    for sws in winners:
        if len(sws & sxs) == 3 and len(sws & sos) == 0:
            x = (sws-sxs).pop()
            #print('We have oppo forced win:', sws, xs, sws-sxs)
            #print_board(xs, os, winner=sws)
            return x

    # look if we have a win
    for sws in winners:
        if len(sws & sos) == 3 and len(sws & sxs) == 0:
            o = (sws-sos).pop()
            #print('Blocking oppo forced win:', sws, os, sws-sos)
            #print_board(xs, os, winner=sws)
            return None

    for sws in winners:
        if len(sws & sxs) == 2 and len(sws & sos) == 0:
            c1, c2 = sws - sxs
            for x,o in ((c1,c2), (c2,c1)):
                nxs = xs+(x,)
                nos = os+(o,)

                #print('Considering oppo: X=%d, O=%d' % (x, o))
                #print_board(nxs, nos)

                move = find_opponent_forced_win(nxs, nos)
                # return first found
                if move is not None:
                    return x

    #print('Returning opp None')
    return None


def find_best_move(xs, os):
    global ordered_cells, winners

    #print('find_best_move:', xs, os)
    # find forced win, or block opponent forced win
    min_len = 200 # 200 represents no forced win, 100+depth represents blocking opponent win, else forced win in this many moves
    depth, move = find_forced_win(xs, os, min_len)
    if move is not None:
        #print('Forced win in', depth-len(os), 'moves')
        #print_board(xs, os)
        return move

    ## see if next move leads to forced win
    #best_move = (min_len, None)

    # no forced wins in next move.
    # find promising move.
    sxs = set(xs)
    sos = set(os)

    # remove used cells, but keep order
    #print('ordered_cells before:', ordered_cells)
    ordered_cells = tuple(c for c in ordered_cells if c not in (sxs|sos))
    #print('ordered_cells  after:', ordered_cells)

    # remove used winners
    def ispure(ws, sxs, sos):
        if (ws & sxs) and (ws & sos):
            #print('Removing winner:', ws)
            return False
        return True
    #print('winners before:', winners)
    winners = tuple(ws for ws in winners if ispure(ws, sxs, sos))
    #print('winners  after:', winners)

    # evaluate next move
    # [0] == number of wins with 0 X and O
    # [1] == number of wins with 1 O
    # [2] == number of wins with 2 O
    # [3] == number with 2 Xs
    # [4] == number with 1 Xs.
    bestv = (-1, -1, -1, -1, -1)
    bestc = ordered_cells[0]
    for c in ordered_cells:
        tbestv = [0, 0, 0, 0, 0]
        for sws in winners:
            if c not in sws:
                continue

            xcnt = len(sws & sxs)
            ocnt = len(sws & sos)
            if xcnt == 0:
                if ocnt == 0:
                    tbestv[0] += 1
                elif ocnt == 1:
                    tbestv[1] += 1
                else:
                    # we would have seen OOOB earlier
                    tbestv[2] += 1
            # we got rid of both Xs and Os, so must be ocnt == 0
            elif xcnt == 2:
                tbestv[3] += 1
            else:
                tbestv[4] += 1
        tbestv = tuple(tbestv)
        #print('tbestv:', tbestv, c, '(', bestv, bestc, ')')
        if bestv < tbestv:
            bestv = tbestv
            bestc = c

    # now see if X has a forced win, given this move
    move = find_opponent_forced_win(xs, os+(bestc,))
    if move is not None:
        #print("Blocking user's forced win")
        return move
    return bestc


def main():
    print("Welcome to 4x4x4 Tic-Tac-Toe!")
    print("Enter moves as three digits (zyx, e.g., 000 or 333).")
    print("The top most row of numbers (over the planes) are z.")
    print("The row of numbers over the columns are y.")
    print("The numbers at the start of each row are x.")
    print("You are 'X', computer is 'O'.")

    #print('Start of Game', file=flog)

    # All the Xs and all the Os
    xs = tuple()
    os = tuple()

    while True:
        # get and validate user move
        while True:
            print_board(xs, os, isnumbering=False)
            user_input = input('Your move (zyx): ').strip()
            coords = parse_input(user_input)
            if coords is None:
                print("Invalid move. Use three digits (0-3 each), e.g., '123' for plane 1, column 2, row 3.")
                continue
            z,y,x = coords
            cx = zyx2c(z,y,x)
            if cx in (xs+os):
                print("Invalid move.", user_input, "is already taken.")
                continue
            break

        # add opponent move to xs
        xs = xs+(cx,)
        #print('User Move:', user_input, coords, cx, flush=True)
        #print('User Move:', user_input, coords, cx, file=flog)

        ws = check_win(cx, xs)
        if ws:
            print("You win!")
            print_board(xs, os, winner=ws, isnumbering=False)
            break
        if is_board_full(xs, os):
            print("It's a tie! At AAA")
            print_board(xs, os, isnumbering=False)
            break

        # Computer's turn
        beg = time.perf_counter()
        co = find_best_move(xs, os)
        end = time.perf_counter()
        diff = end - beg
        os = os+(co,)
        x, y, z = c2xyz(co)
        print(f"Computer's move: {z}{y}{x} (elapsed time: {diff:.9f} seconds)")
        #print(f"Computer's move: {z}{y}{x} ({co}) (elapsed time: {diff:.9f} seconds)", file=flog, flush=True)

        ws = check_win(co, os)
        if ws:
            print("Computer wins!")
            print_board(xs, os, winner=ws, isnumbering=False)
            break
        if is_board_full(xs, os):
            print("It's a tie! At BBB")
            print_board(xs, os, isnumbering=False)
            break

if __name__ == "__main__":
    #flog = open('Log', 'a')
    main()
