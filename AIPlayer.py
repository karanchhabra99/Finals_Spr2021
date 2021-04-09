import numpy as np
# from ChessEngine import Move, Pawn, Knight, Bishop, Rook, Queen, King

class AIPlayer():
    def __init__(self, dim, move, Player_turn):
        self.move = move
        self.dim = dim
        self.dept = 3
        self.Player_turn = Player_turn

    def play(self, board, last_move):
        current_location, next_location = self.Minimax(board, self.Player_turn, last_move, self.dept)
        # Checks if the move is valid
        return self.move.check_piece_and_play(board, current_location, next_location, Player_turn, last_move)

    ## Reference: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    # def Minimax(self, board, Player_turn, last_move, dept):
    #     if (dept == 0) or (len(np.where(board == 1000)) == 0) or (len(np.where(board == -1000)) == 0):
    #         return self.board_score(board)
    #
    #     if self.Player_turn == Player_turn:
    #         maxEval_score = -999999
            # for possibel
            #     mini






    def board_score(self, board):
        ## ToDo:
        pass