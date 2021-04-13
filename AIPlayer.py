import numpy as np
import copy

# from ChessEngine import Move, Pawn, Knight, Bishop, Rook, Queen, King

class AIPlayer():
    def __init__(self, dim, move, Player_turn):
        ## ToDo: Check if move instance should be created
        self.move = move
        self.dim = dim
        self.dept = 1
        self.Player_turn = Player_turn

        ## ToDo: After board_score is set-up
        self.count = 1

    def play(self, board, last_move):
        current_location, next_location = self.Minimax(board, self.Player_turn, last_move, self.dept)
        # Checks if the move is valid
        return current_location, next_location

    ## Reference: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    def Minimax(self, board, Player_turn, last_move, dept, best_move = None):
        if (dept == 0) or (len(np.where(board == 1000)) == 0) or (len(np.where(board == -1000)) == 0):
            return self.board_score(board)

        if self.Player_turn == Player_turn:
            maxEval_score = -999999
            ## Pawn Moves
            best_move = self.pawn_best_move(board, Player_turn, maxEval_score, best_move, last_move, dept)
        else:
            minEval_score = 999999
            ## Pawn Moves
            best_move = self.pawn_best_move(board, Player_turn, minEval_score, best_move, last_move, dept)


        return best_move


    def pawn_best_move(self, board, Player_turn, Score, best_move, last_move, dept):
        all_pawns = np.where(board == 1 * Player_turn)
        for p in range(len(all_pawns[0])):
            if Player_turn == 1:
                all_pawn_moves = self.move.pawn.all_move_pawn_helper((all_pawns[0][p], all_pawns[1][p]))
            else:
                all_pawn_moves = self.move.pawn.all_AI_black_move_pawn((all_pawns[0][p], all_pawns[1][p]))

            for each_move in all_pawn_moves:
                # print((all_pawns[0][p], all_pawns[1][p]), each_move)
                if Player_turn == -1:
                    if each_move[0] == 7:
                        Score, best_move = self.Minimax_pawn_helper(board, all_pawns, p, each_move,
                                                                            Score,  Player_turn, best_move, dept,True)
                    elif self.move.check_piece_and_play(board, (all_pawns[0][p], all_pawns[1][p]), each_move,
                                                        Player_turn, last_move) == 1:
                        Score, best_move = self.Minimax_pawn_helper(board, all_pawns, p, each_move,
                                                                            Score, Player_turn,
                                                                            best_move, dept)
                else:
                    if each_move[0] == 0:
                        Score, best_move = self.Minimax_pawn_helper(board, all_pawns, p, each_move,
                                                                            Score,  Player_turn, best_move, dept, True)
                    elif self.move.check_piece_and_play(board, (all_pawns[0][p], all_pawns[1][p]), each_move,
                                                        Player_turn, last_move) == 1:
                        Score, best_move = self.Minimax_pawn_helper(board, all_pawns, p, each_move,
                                                                            Score, Player_turn,
                                                                            best_move, dept)
        return best_move


    def Minimax_pawn_helper(self, board, all_pawns, p, each_move, Score, Player_turn, best_move, dept, Queen = False):
        board_p = copy.deepcopy(board)
        ## Making changes on the board
        last_move_p = (board_p[all_pawns[0][p], all_pawns[1][p]], each_move[0], each_move[1])
        if Queen:
            board_p[each_move[0], each_move[1]] = 9 * Player_turn
        else:
            board_p[each_move[0], each_move[1]] = board_p[all_pawns[0][p], all_pawns[1][p]]
        board_p[all_pawns[0][p], all_pawns[1][p]] = 0

        eval = self.Minimax(board_p, Player_turn * -1, last_move_p, dept -1, best_move)
        if eval != None:
            if self.Player_turn == Player_turn:
                Score = max(Score, eval)
            else:
                Score = min(Score, eval)
            if Score == eval:
                if dept == self.dept:
                    best_move = [(all_pawns[0][p], all_pawns[1][p]), each_move]

        return Score, best_move

    def board_score(self, board):
        ## ToDo:
        self.count+= 1
        if self.count <1000:
            # print(board)
            print(self.count)
            return self.count

        else:
            return -self.count