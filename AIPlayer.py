from ChessEngine import Move, Pawn, Knight, Bishop, Rook, Queen, King


class AIPlayer():
    def __init__(self, dim, move):
        self.move = move

    def play(self, board, current_location, next_location, Player_turn, last_move):
        # Checks if the move is valid
        return self.move.check_piece_and_play(board, current_location, next_location, Player_turn, last_move)