import chess

# Returns true or false depending upon whether the move by the player is valid or not.
def validity_check(move, board):
    try:
        chess.Move.from_uci(move)
    except ValueError:
        return False
    return chess.Move.from_uci(move) in board.legal_moves

# runner function for min_max algorithm
def best_move(board):
    best_score = -float('inf')
    best_move = None

    for move in board.legal_moves:
        board.push(move)
        score = min_max(board, 3, -float('inf'), float('inf'), False)
        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# the minmax algorithm that also conducts alpha beta pruning
def min_max(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluation(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            # FIRST WAS MAX, SO NOW MIN
            eval = min_max(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            # ALPHA BETA PRUNING    
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            # FIRST WAS MIN, SO NOW MAX
            eval = min_max(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            # ALPHA BETA PRUNING
            if beta <= alpha:
                break
        return min_eval

# TAKES BOARD AS PARAMETER AND RETURNS THE SCORE DEPENDING ON WEIGHTS OF PIECES LEFT.
def evaluation(board):
    score = 0
    weights = {
        "P": 1,
        "N": 3,
        "B": 3,
        "R": 5,
        "Q": 9,
        "K": 0
    }

    # loop runs for all pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        # evaluation considering the weights
        piece_weight = weights[piece.symbol().upper()]
        if piece.color == chess.WHITE:
            score += piece_weight
        else:
            score -= piece_weight

    return score

# checks whether the game has a result.
def game_check(board):
    if board.is_game_over():
        result = board.result()
        if result == "1-0":
            print("Checkmate! White wins.")
        elif result == "0-1":
            print("Checkmate! Black wins.")
        else:
            print("Stalemate! Draw.")
        return True
    return False



def display_board(board):
    print("\n")
    board_str = str(board)
    board_str = board_str.replace(".", "◼︎")
    board_str = board_str.replace("p", "♟︎")
    board_str = board_str.replace("r", "♜")
    board_str = board_str.replace("n", "♞")
    board_str = board_str.replace("b", "♝")
    board_str = board_str.replace("q", "♛")
    board_str = board_str.replace("k", "♚")
    board_str = board_str.replace("P", "♙")
    board_str = board_str.replace("R", "♖")
    board_str = board_str.replace("N", "♘")
    board_str = board_str.replace("B", "♗")
    board_str = board_str.replace("Q", "♕")
    board_str = board_str.replace("K", "♔")
    
    board_lines = board_str.split("\n")
    new_board = []
    for line in board_lines:
        new_line = "" *2
        for char in line:
            new_line += char*2
        new_board.append(new_line)
    new_board_str = "\n".join(new_board)
    print(new_board_str)
    print("\n")


def get_player_move(board):
    move = input("Enter your move: ")
    while not validity_check(move, board):
        move = input("Invalid move. Enter your move: ")
    return move

def get_computer_move(board):
    print("Computer is minmaxing the move...")
    move = best_move(board)
    return move


    # RUNNER FUNCTION
def play():
    board = chess.Board()
    while not game_check(board):
        display_board(board)
        if board.turn: # Player's turn
            move = get_player_move(board)
            board.push(chess.Move.from_uci(move))
        else: # Computer's turn
            move = get_computer_move(board)
            board.push(move)
            if board.is_check():
                print("Check!")
    display_board(board)
    print("Game over")



play()