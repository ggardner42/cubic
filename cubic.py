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

corners = ( 0,  3, 12, 15, 48, 51, 60, 63)
inners  = (21, 22, 25, 26, 37, 38, 41, 42)
edges   = ( 1,  2,  4,  7,  8, 11, 13, 14, 16, 19, 28, 31, 32, 35, 44, 47, 49, 50, 52, 55, 56, 59, 61, 62)
surface = ( 5,  6,  9, 10, 17, 18, 20, 23, 24, 27, 29, 30, 33, 34, 36, 39, 40, 43, 45, 46, 53, 54, 57, 58)

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

def is_board_full(ys, ms):
    """Check if the board is full."""
    return len(ys + ms) == 64

def print_board(xs, os, markx='X', marko='O', winner=None, isnumbering=True):
    lastx = lasto = 100
    if xs:
        lastx = xs[-1]
    if os:
        lasto = os[-1]

    if len(xs) < len(os):
        xs = xs + (None,) * (len(os) - len(xs))
        os = os
    elif len(os) < len(xs):
        xs = xs
        os = os + (None,) * (len(xs) - len(os))
    xos = zip(xs, os)

    cells = ['   ']*64
    for i,(x,o) in enumerate(xos):
        # numbering for debugging statements
        def mk(i, m, mark):
            if m is not None:
                if isnumbering:
                    ii = i+1
                    if ii < 10:
                        cells[m] = ' %s%d' % (mark, ii)
                    else:
                        cells[m] = '%s%d' % (mark, ii)
                else:
                    cells[m] = ' %s ' % mark
        mk(i, x, markx)
        mk(i, o, marko)

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

# y=you, m=me
def find_forced_win(ys, ms, marky, markm, min_len, findfirst=False):

    #print('Entering', ys, ms, marky, markm, min_len)
    #print_board(ys, ms, marky, markm)

    mlen = len(ms)
    if mlen >= min_len:
        #print('Returning due to cutoff:', mlen, min_len)
        return (min_len, None) # discard

    # we are O, and second to move, so this move may fill board
    sys = set(ys)
    sms = set(ms)

    # look if we have a win
    for sws in winners:
        if len(sws & sms) == 3 and len(sws & sys) == 0:
            m = (sws-sms).pop()
            #print('We have forced win:', sws, ms, sws-sms)
            #print_board(ys, ms, marky, markm, winner=sws)
            return (mlen, m)

    # look if they have a win
    for sws in winners:
        if len(sws & sys) == 3 and len(sws & sms) == 0:
            #print('Blocking forced win:', sws, ys, sws-sys)
            #print_board(ys, ms, marky, markm, winner=sws)
            return (200, None)

    # exhaust all possible forced moves
    best_move = (min_len, None)

    for sws in winners:
        if len(sws & sms) == 2 and len(sws & sys) == 0:
            c1, c2 = sws - sms
            for i,(y,m) in enumerate(((c1,c2), (c2,c1))):
                nys = ys+(y,)
                nms = ms+(m,)

                #print('Considering %d: YOU=%d, ME=%d' % (i, y, m), best_move)
                #print_board(nys, nms, marky, markm)

                depth, move = find_forced_win(nys, nms, marky, markm, best_move[0])
                if depth and depth < best_move[0]:
                    #print('Got new best_move:', (depth, move), 'replacing:', best_move)
                    best_move = (depth, m)
                    if findfirst:
                        return best_move

    #print('Returning:', mlen, best_move)
    return best_move


def find_best_move(xs, os):
    global winners

    #print('find_best_move:', xs, os)
    # find forced win, or block opponent forced win
    min_len = 200 # 200 represents no forced win, 100+depth represents blocking opponent win, else forced win in this many moves
    #beg = time.perf_counter()
    depth, move = find_forced_win(xs, os, 'X', 'O', min_len)
    #end = time.perf_counter()
    #diff = end - beg
    #print("best for computer:", (depth, move), f"(elapsed time: {diff:.9f} seconds)")
    if move is not None:
        #print('Forced win in', depth-len(os), 'moves')
        #print_board(xs, os)
        return move

    # no forced wins in next move.
    # find promising move.
    sxs = set(xs)
    sos = set(os)

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
    def best(cells):
        bestv = (-1, -1, -1, -1, -1)
        bc = None
        for c in cells:
            if c in (sxs|sos):
                continue
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
            #print('tbestv:', tbestv, c, '(', bestv, bc, ')', cells)
            if bestv < tbestv:
                bestv = tbestv
                bc = c
        return bc

    for cs in (corners, inners, edges, surface):
        bestc = best(cs)
        if bestc is not None:
            break

    # now see if X has a forced win, given this move
    #print('find_best_move for user:', xs, os)
    #beg = time.perf_counter()
    depth, move = find_forced_win(os+(bestc,), xs, 'O', 'X', min_len, findfirst=True)
    #end = time.perf_counter()
    #diff = end - beg
    #print("best for user:", (depth, move), f"(elapsed time: {diff:.9f} seconds)")
    if move is not None:
        #print("Blocking user's forced win")
        return move
    return bestc

def main():
    print("Welcome to 4x4x4 Tic-Tac-Toe!")
    print("'X' always goes first.")

    while True:
        user_input = input("Do you wish to be 'X' and go first? ").strip()
        if 'yes'.startswith(user_input):
            print("You are 'X', computer is 'O'.")
            your_mark = 'X'
            my_mark = 'O'
            ys = tuple() # your marks
            ms = tuple() # my marks
            break
        elif 'no'.startswith(user_input):
            print("Computer is 'X', you are 'O'.")
            my_mark = 'X'
            your_mark = 'O'
            ms = (0,) # my marks, starting with 000
            ys = tuple() # your marks
            break
        else:
            print("Please answer [y]es or [n]o.")

    print()
    print("Enter moves as three digits (zyx, e.g., 000 or 333).")
    print("The top most row of numbers (over the planes) are z.")
    print("The row of numbers over the columns are y.")
    print("The numbers at the start of each row are x.")

    #print('Start of Game', file=flog)

    # All the Xs and all the Os
    while True:
        # get and validate user move
        while True:
            print_board(ys, ms, markx=your_mark, marko=my_mark, isnumbering=False)
            user_input = input('Your move (zyx): ').strip()
            coords = parse_input(user_input)
            if coords is None:
                print("Invalid move. Use three digits (0-3 each), e.g., '123' for plane 1, column 2, row 3.")
                continue
            z,y,x = coords
            cx = zyx2c(z,y,x)
            if cx in (ys+ms):
                print("Invalid move.", user_input, "is already taken.")
                continue
            break

        # add opponent move
        ys = ys+(cx,)
        #print('User Move:', user_input, coords, cx, flush=True)
        #print('User Move:', user_input, coords, cx, file=flog)

        ws = check_win(cx, ys)
        if ws:
            print("You win!")
            print_board(ys, ms, markx=your_mark, marko=my_mark, winner=ws, isnumbering=False)
            break
        if is_board_full(ys, ms):
            print("It's a tie! At AAA")
            print_board(ys, ms, markx=your_mark, marko=my_mark, isnumbering=False)
            break

        # Computer's turn
        beg = time.perf_counter()
        co = find_best_move(ys, ms)
        end = time.perf_counter()
        diff = end - beg
        ms = ms+(co,)
        x, y, z = c2xyz(co)
        print(f"Computer's move: {z}{y}{x} (elapsed time: {diff:.9f} seconds)")
        #print(f"Computer's move: {z}{y}{x} ({co}) (elapsed time: {diff:.9f} seconds)", file=flog, flush=True)

        ws = check_win(co, ms)
        if ws:
            print("Computer wins!")
            print_board(ys, ms, markx=your_mark, marko=my_mark, winner=ws, isnumbering=False)
            break
        if is_board_full(ys, ms):
            print("It's a tie! At BBB")
            print_board(ys, ms, markx=your_mark, marko=my_mark, isnumbering=False)
            break

if __name__ == "__main__":
    #flog = open('Log', 'a')
    main()
