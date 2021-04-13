import numpy as np
import copy
# from ChessEngine import Move, Pawn, Knight, Bishop, Rook, Queen, King

class AIPlayer():
    def __init__(self, dim, move, Player_turn):
        ## ToDo: Check if move instance should be created
        self.move = move
        self.dim = dim
        self.dept = 3
        self.Player_turn = Player_turn

    def play(self, board, last_move):
        current_location, next_location = self.Minimax(board, self.Player_turn, last_move, self.dept)
        # Checks if the move is valid
        return current_location, next_location

    ## Reference: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    def Minimax(self, board, Player_turn, last_move, dept):
        if (dept == 0) or (len(np.where(board == 1000)) == 0) or (len(np.where(board == -1000)) == 0):
            return self.board_score(board)

        if self.Player_turn == Player_turn:
            maxEval_score = -999999
            best_move = None
            ## Pawn Moves
            ## ToDo: make it dynamic
            all_pawns = np.where(board == 1*Player_turn)
            for p in range(len(all_pawns[0])):
                if Player_turn == 1:
                    all_pawn_moves = self.move.pawn.all_move_pawn_helper((all_pawns[0][p], all_pawns[1][p]))
                else:
                    all_pawn_moves = self.move.pawn.all_AI_black_move_pawn((all_pawns[0][p], all_pawns[1][p]))
                for each_move in all_pawn_moves:
                    # print((all_pawns[0][p], all_pawns[1][p]), each_move)
                    if self.move.check_piece_and_play(board, (all_pawns[0][p], all_pawns[1][p]), each_move, Player_turn, last_move) == 1:
                            # pawn.pawn_move_checker_en_passant(board, (all_pawns[0][p], all_pawns[1][p]), each_move, , Player_turn) == 1:
                        board_p = copy.deepcopy(board)
                        ## Making changes on the board
                        last_move_p = (board_p[all_pawns[0][p], all_pawns[1][p]], each_move[0], each_move[1])
                        board_p[each_move[0], each_move[1]] = board_p[all_pawns[0][p], all_pawns[1][p]]
                        board_p[all_pawns[0][p], all_pawns[1][p]] = 0

                        eval = self.Minimax(board_p, Player_turn *-1, last_move_p, 0)
                        maxEval_score = max(maxEval_score, eval)
                        if maxEval_score == eval:
                            best_move = [(all_pawns[0][p], all_pawns[1][p]), each_move]

        return best_move






    def board_score(self, board):
        ## ToDo:
        return 1