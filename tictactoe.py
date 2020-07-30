# write your code here
# from reportlab import xrange
import random


def print_game(string):
    string_list = [s for s in string]
    print("---------")
    while string_list:
        print("| " + ' '.join(string_list[:3]) + " |")
        string_list = string_list[3:]
    print("---------")


def make_game_matrix(string):
    l = []
    for i in range(9):
        if string[i] == 'X':
            l.append(1)
        elif string[i] == 'O':
            l.append(0)
        else:
            l.append(-10)
    game_matrix = []
    while l:
        game_matrix.append(l[:3])
        l = l[3:]
    return game_matrix


def eval_game(game_matrix):
    row_sum = []
    col_sum = []
    main_diag_sum = sum([game_matrix[i][i] for i in range(len(game_matrix))])
    sec_diag_sum = sum([row[-i - 1] for i, row in enumerate(game_matrix)])
    i = 0
    no_x = 0
    no_o = 0
    for row in game_matrix:
        row_sum.append(sum(row))
        col_sum.append(sum([col[i] for col in game_matrix]))
        i += 1
        no_x += len([x for x in row if x == 1])
        no_o += len([x for x in row if x == 0 and x != -10])
    # impossible game_matrix because of wrong number of X or O
    if no_x > no_o + 1:
        return -1
    elif no_o > no_x + 1:
        return -1

    # impossible game_matrix because it didn't end when it should
    # both players are winning or a player is winning twice
    if main_diag_sum == 3 and sec_diag_sum == 3:
        return -1
    if (row_sum[0] == 3 and (row_sum[1] == 3 or row_sum[2] == 3)) or \
            (row_sum[1] == 3 and (row_sum[0]) == 3 or row_sum[2] == 3) or \
            (row_sum[2] == 3 and (row_sum[0]) == 3 or row_sum[1] == 3):
        return -1
    if (row_sum[0] == 3 and (row_sum[1] == 0 or row_sum[2] == 0)) or \
            (row_sum[1] == 3 and (row_sum[0] == 0 or row_sum[2] == 0)) or \
            (row_sum[2] == 3 and (row_sum[0] == 0 or row_sum[1] == 0)):
        return -1
    if (col_sum[0] == 3 and (col_sum[1] == 3 or col_sum[2] == 3)) or \
            (col_sum[1] == 3 and (col_sum[0] == 3 or col_sum[2] == 3)) or \
            (col_sum[2] == 3 and (col_sum[0] == 3 or col_sum[1] == 3)):
        return -1
    if (col_sum[0] == 3 and (col_sum[1] == 0 or col_sum[2] == 0)) or \
            (col_sum[1] == 3 and (col_sum[0] == 0 or col_sum[2] == 0)) or \
            (col_sum[2] == 3 and (col_sum[0] == 0 or col_sum[1] == 0)):
        return -1

    # X wins
    if main_diag_sum == 3 or sec_diag_sum == 3 or row_sum[0] == 3 or row_sum[1] == 3 or row_sum[2] == 3 or \
            col_sum[0] == 3 or col_sum[1] == 3 or col_sum[2] == 3:
        return 1

    # O wins
    if main_diag_sum == 0 or sec_diag_sum == 0 or row_sum[0] == 0 or row_sum[1] == 0 or row_sum[2] == 0 or \
            col_sum[0] == 0 or col_sum[1] == 0 or col_sum[2] == 0:
        return 0

    # game not finished
    if no_x < 5:
        return 3

    # draw
    return 2


def eval_coordinates(input_x, input_y, game_matrix):
    if input_x.isdigit() and input_y.isdigit():
        x = int(input_x)
        y = int(input_y)
    else:
        return -1

    if x > 3 or y > 3:
        return -2

    if game_matrix[3-x][y-1] == 0 or game_matrix[3-x][y-1] == 1:
        return 1

    return 0


def take_input(game_matrix):
    while True:
        str_in = input("Enter the coordinates: ")
        if len(str_in.split()) == 1 and str_in != "exit":
            print("You should enter numbers!")
        elif str_in != "exit":
            y, x = [x for x in str_in.split()]
            check = eval_coordinates(x, y, game_matrix)
            if check == 0:
                return [x, y]
            elif check == -1:
                print("You should enter numbers!")
            elif check == 1:
                print("This cell is occupied! Choose another one!")
            elif check == -2:
                print("Coordinates should be from 1 to 3!")
        else:
            return [-1, -1]


def make_move(game_matrix, x, y, player):
    if player == 1:
        game_matrix[3-x][y-1] = 1
    else:
        game_matrix[3-x][y-1] = 0
    return game_matrix


def print_matrix(game_matrix):
    print("---------")
    for i in range(3):
        s = "| "
        for j in range(3):
            if game_matrix[i][j] == 1:
                s += "X "
            elif game_matrix[i][j] == 0:
                s += "O "
            else:
                s += "_ "
        s += "|"
        print(s)
    print("---------")


def get_player_to_move(game_matrix):
    no_x = 0
    no_o = 0
    for row in game_matrix:
        no_x += len([x for x in row if x == 1])
        no_o += len([x for x in row if x == 0 and x != -10])

    if no_x == no_o:
        return 1
    return 0


def generate_comp_move(game_matrix):
    while True:
        x = random.randint(1, 3)
        y = random.randint(1, 3)
        check = eval_coordinates(str(x), str(y), game_matrix)
        if check == 0:
            return [x, y]


def undo_move(game_matrix, x, y):
    game_matrix[3-x][y-1] = -10
    return game_matrix


def generate_comp_medium(game_matrix, player):
    s = 0
    for row in range(3):
        for col in range(3):
            if game_matrix[row][col] == -10:
                game_matrix[row][col] = (player) % 2
                check = eval_game(game_matrix)
                game_matrix[row][col] = -10
                if check == 0 or check == 1:
                    return [3-row, col+1]
    return generate_comp_move(game_matrix)


def play_user_comp(player1, player2):
    matrix = [[-10, -10, -10],
              [-10, -10, -10],
              [-10, -10, -10]]
    if player1 == 0:
        player1 = 1
        player2 = 0
        [x, y] = generate_comp_medium(matrix, player1)
        matrix = make_move(matrix, int(x), int(y), player1)
    print_matrix(matrix)
    s = 1
    while True:
        [x, y] = take_input(matrix)
        if x == -1 and y == -1:
            return -1
        matrix = make_move(matrix, int(x), int(y), player2)
        print_matrix(matrix)
        x = eval_game(matrix)
        if x == 1:
            print("X wins")
            return 0
        elif x == 0:
            print("O wins")
            return 0
        elif x == 2:
            print("Draw")
            return 0
        print("Making move level \"easy\"")
        if s < 2:
            [x, y] = generate_comp_medium(matrix, player1)
        else:
            [x, y] = best_com(matrix)
        print(x, y)
        matrix = make_move(matrix, int(x), int(y), player1)
        print_matrix(matrix)
        x = eval_game(matrix)
        if x == 1:
            print("X wins")
            return 0
        elif x == 0:
            print("O wins")
            return 0
        elif x == 2:
            print("Draw")
            return 0
        s += 1


def play_comp_comp():
    game_matrix = [[-10, -10, -10],
                   [-10, -10, -10],
                   [-10, -10, -10]]
    print_matrix(game_matrix)
    ply = 1
    while True:
        print("Making move level \"easy\"")
        [x, y] = generate_comp_medium(game_matrix, ply)
        game_matrix = make_move(game_matrix, int(x), int(y), ply)
        ply += 1
        ply %= 2
        print_matrix(game_matrix)
        x = eval_game(game_matrix)
        if x == 1:
            print("X wins")
            break
        elif x == 0:
            print("O wins")
            break
        elif x == 2:
            print("Draw")
            break


def play_user_user():
    matrix = [[-10, -10, -10],
              [-10, -10, -10],
              [-10, -10, -10]]
    print_matrix(matrix)
    player = 1
    while True:
        [x, y] = take_input(matrix)
        if x == -1 and y == -1:
            return -1
        matrix = make_move(matrix, int(x), int(y), player)
        player += 1
        player %= 2
        print_matrix(matrix)
        x = eval_game(matrix)
        if x == 1:
            print("X wins")
            break
        elif x == 0:
            print("O wins")
            break
        elif x == 2:
            print("Draw")
            break
        print("Making move level \"easy\"")
        [x, y] = take_input(matrix)
        if x == -1 and y == -1:
            return -1
        matrix = make_move(matrix, int(x), int(y), player)
        player += 1
        player %= 2
        print_matrix(matrix)
        x = eval_game(matrix)
        if x == 1:
            print("X wins")
            break
        elif x == 0:
            print("O wins")
            break
        elif x == 2:
            print("Draw")
            break


def play_game(player1, player2):
    if player1 == "user" and player2 == "medium":
        x = play_user_comp(1, 0)
        if x == -1:
            return -1
    elif player1 == "medium" and player2 == "user":
        x = play_user_comp(0, 1)
        if x == -1:
            return -1
    elif player1 == "medium" and player2 == "medium":
        play_comp_comp()
        return 1
    else:
        x = play_user_user()
        if x == -1:
            return -1


def eval_position(game_matrix):
    check_score = eval_game(game_matrix)
    if check_score == 1:
        return 10
    if check_score == 0:
        return -10
    if check_score == 2:
        return 5
    return 0


def minimax(game_matrix, depth, is_max):
    score = eval_position(game_matrix)

    if score == 10:
        return score
    if score == -10:
        return score
    if score == 5:
        return 0
    # minimize to move
    if is_max:
        best = -100
        for row in range(3):
            for col in range(3):
                if game_matrix[row][col] == -10:
                    game_matrix[row][col] = 1
                    best = max(best, minimax(game_matrix, depth + 1, not is_max))
                    game_matrix[row][col] = -10
        return best
    else:
        best = 100
        for row in range(3):
            for col in range(3):
                if game_matrix[row][col] == -10:
                    game_matrix[row][col] = 0
                    best = min(best, minimax(game_matrix, depth + 1, not is_max))
                    game_matrix[row][col] = -10
        return best


def best_com(game_matrix):
    best_val = -100
    r = -1
    c = -1
    for row in range(3):
        for col in range(3):
            if game_matrix[row][col] == -10:
                game_matrix[row][col] = 1
                score = minimax(game_matrix, 0, False)
                game_matrix[row][col] = -10
                if score >= best_val:
                    r = row
                    c = col
    return [(3-r), c+1]


def main():
    while True:
        command = input()
        if command == "exit":
            break
        inp_list = command.split()
        if len(inp_list) != 3:
            print("Bad parameters!")
        else:
            x = play_game(inp_list[1], inp_list[2])
            if x == -1:
                break


if __name__ == "__main__":
    main()