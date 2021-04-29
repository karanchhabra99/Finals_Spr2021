import numpy as np
import copy

'''
Player _turn 1 means whites turn and -1 means blacks turn

White pieces are represented with following numbers:
1. Pawn: 1
2. Bishop: 2
3. Knight: 3
4. Rook: 5
5. Queen: 9
6. King: 1000

And black pieces are represented with negative numbers as white 
'''


class AIPlayer():
    def __init__(self, dim, move, Player_turn, modified):
        self.move = move
        self.dim = dim
        self.dept = 2
        self.Player_turn = Player_turn
        self.modified = modified
        self.board_state_heuristic_max, self.board_state_heuristic_min = self.heuristic_dim_player()


    def play(self, board, last_move):
        _, cur = self.Minimax(board, self.Player_turn, last_move, self.dept)
        # print(f"Top: {cur}")
        current_location, next_location = cur

        # _, (current_location, next_location) = self.Minimax(board, self.Player_turn, last_move, self.dept)
        # Checks if the move is valid
        return current_location, next_location

    ## Reference: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
    def Minimax(self, board, Player_turn, last_move, dept, best_move = None):
        if (dept == 0) or (len(np.where(board == 1000)) == 0) or (len(np.where(board == -1000)) == 0):
            return self.board_score(board), best_move

        if self.Player_turn == Player_turn:
            Score = -999999
        else:
            Score = 999999

        # #Knight Best Move
        Score, best_move = self.knight_best_move(board, Player_turn, Score, best_move, dept)
        # # ## Bishop Best Move
        Score, best_move = self.bishop_best_move(board, Player_turn, Score, best_move, dept)
        # ## Rooks Best Move
        Score, best_move = self.rook_best_move(board, Player_turn, Score, best_move, dept)
        # ## Queen Best Move
        Score, best_move = self.queen_best_move(board, Player_turn, Score, best_move, dept)
        # ## King Best Move
        Score, best_move = self.king_best_move(board, Player_turn, Score, best_move, dept)
        #Pawn Best move
        Score, best_move = self.pawn_best_move(board, Player_turn, Score, best_move, last_move, dept)

        # print(f"minmax {knight_best_move}")
        return Score, best_move

    def all_moves_helper(self, board, last_move_all, all_pieces, p, each_move, Player_turn, dept, best_move, Score, Queen = False, rook =False):
        board_all = copy.deepcopy(board)

        last_move_all = (board_all[all_pieces[0][p], all_pieces[1][p]], each_move[0], each_move[1])
        if Queen:
            board_all[each_move[0], each_move[1]] = 9 * Player_turn
        else:
            board_all[each_move[0], each_move[1]] = board_all[all_pieces[0][p], all_pieces[1][p]]
        board_all[all_pieces[0][p], all_pieces[1][p]] = 0
        ## Rook remove Pawn
        if rook:
            if self.modified == 1:
                self.move.rook.remove_pawns(board_all, (all_pieces[0][p], all_pieces[1][p]), (each_move[0], each_move[1]))

        eval, best_move = self.Minimax(board_all, Player_turn * -1, last_move_all, dept - 1, best_move)

        if eval != None:
            if self.Player_turn == Player_turn:
                Score = max(Score, eval)
            else:
                Score = min(Score, eval)

            if Score == eval:
                if dept == self.dept:
                    best_move = [(all_pieces[0][p], all_pieces[1][p]), each_move]

        return Score, best_move

    def king_best_move(self, board, Player_turn, Score, best_move, dept):
        all_king = np.where(board == 1000 * Player_turn)
        if len(all_king[0]) !=0:
            all_king_moves = self.move.king.king_moves(board, (all_king[0][0], all_king[1][0]), Player_turn)

            for each_move in all_king_moves:
                Score, best_move = self.all_moves_helper(board, None, all_king, 0, each_move, Player_turn, dept,
                                                         best_move,
                                                         Score)

        return Score, best_move

    def queen_best_move(self, board, Player_turn, Score, best_move, dept):
        all_queen = np.where(board == 9 * Player_turn)
        for p in range(len(all_queen[0])):
            all_queen_moves = self.move.queen.rook.straight_moves(board, (all_queen[0][p], all_queen[1][p]), Player_turn) + self.move.queen.bishop.diagonal_moves(board, (all_queen[0][p], all_queen[1][p]), Player_turn)

            for each_move in all_queen_moves:
                Score, best_move = self.all_moves_helper(board, None, all_queen, p, each_move, Player_turn, dept,
                                                         best_move,
                                                         Score)

        return Score, best_move

    def rook_best_move(self, board, Player_turn, Score, best_move, dept):
        all_rook = np.where(board == 5 * Player_turn)
        for p in range(len(all_rook[0])):
            all_rook_moves = self.move.rook.straight_moves(board, (all_rook[0][p], all_rook[1][p]), Player_turn)

            for each_move in all_rook_moves:
                Score, best_move = self.all_moves_helper(board, None, all_rook, p, each_move, Player_turn, dept,
                                                         best_move,
                                                         Score, False, True)

        return Score, best_move

    def bishop_best_move(self, board, Player_turn, Score, best_move, dept):
        all_bishop = np.where(board == 2 * Player_turn)
        for p in range(len(all_bishop[0])):
            all_bishop_moves = self.move.bishop.diagonal_moves(board, (all_bishop[0][p], all_bishop[1][p]), Player_turn)

            for each_move in all_bishop_moves:
                Score, best_move =self.all_moves_helper(board, None, all_bishop, p, each_move, Player_turn, dept, best_move,
                                 Score)

        return Score, best_move


    def knight_best_move(self, board, Player_turn, Score, best_move, dept):
        all_knight = np.where(board == 3 * Player_turn)
        for p in range(len(all_knight[0])):

            all_knight_moves = self.move.knight.all_move_knight_helper((all_knight[0][p], all_knight[1][p]))

            for each_move in all_knight_moves:
                if self.move.knight.knight_move_checker(board, (all_knight[0][p], all_knight[1][p]), (each_move[0], each_move[1]), Player_turn) == 1:
                    Score, best_move = self.all_moves_helper(board, None, all_knight, p, each_move, Player_turn, dept,
                                                             best_move,
                                                             Score)

        return Score, best_move


    def pawn_best_move(self, board, Player_turn, Score, best_move, last_move, dept):
        all_pawns = np.where(board == 1 * Player_turn)
        for p in range(len(all_pawns[0])):
            if Player_turn == 1:
                all_pawn_moves = self.move.pawn.all_move_pawn_helper((all_pawns[0][p], all_pawns[1][p]))
            else:
                all_pawn_moves = self.move.pawn.all_AI_black_move_pawn((all_pawns[0][p], all_pawns[1][p]))

            for each_move in all_pawn_moves:
                if (each_move[0] == 7) or (each_move[0] == 0):
                    board_pawn = copy.deepcopy(board)
                    if self.move.check_piece_and_play(board_pawn, (all_pawns[0][p], all_pawns[1][p]), each_move,
                                                      Player_turn, last_move, True) == 1:
                        Score, best_move = self.Minimax_pawn_helper(board, all_pawns, p, each_move,
                                                                    Score, Player_turn, best_move, dept, True)
                else:
                    if self.move.check_piece_and_play(board, (all_pawns[0][p], all_pawns[1][p]), each_move,
                                                        Player_turn, last_move, True) == 1:
                        Score, best_move = self.Minimax_pawn_helper(board, all_pawns, p, each_move,
                                                                        Score, Player_turn,
                                                                        best_move, dept)

        return Score, best_move


    def Minimax_pawn_helper(self, board, all_pawns, p, each_move, Score, Player_turn, best_move, dept, Queen = False):
        Score, best_move = self.all_moves_helper(board, None, all_pawns, p, each_move, Player_turn, dept,
                                                 best_move,
                                                 Score, Queen)
        return Score, best_move

    def board_score_helper_score_cal(self, board, piece, Player_turn,piece_heuristic, piece_score, multiple, modified_score):
        Score = 0
        all_piece = np.where(board == piece * Player_turn)
        for i in range(len(all_piece[0])):
            Score += multiple * piece_heuristic[all_piece[0][i], all_piece[1][i]] + piece_score + modified_score
        return Score
    def board_score_helper(self, board, Player_turn, board_state_heuristic):
        pawn_heuristic, knight_heuristic, bishop_heuristic, rook_heuristic, queen_heuristic = board_state_heuristic
        Score = 0
        if self.modified == 0:
            knight_modified = 0
            rook_modified = 0
            bishop_modified = 0
        else:
            knight_modified = 4
            rook_modified = 10
            bishop_modified = 7

        ## Getting all pawn of maximizing player
        #Pawn
        Score += self.board_score_helper_score_cal(board, 1, Player_turn, pawn_heuristic, 3,1, 0)
        # Queen
        Score += self.board_score_helper_score_cal(board, 9, Player_turn, queen_heuristic, 50,4, 0)
        # Knight
        Score += self.board_score_helper_score_cal(board, 3, Player_turn, knight_heuristic, 10,2, knight_modified)
        # Bishop
        Score += self.board_score_helper_score_cal(board, 2, Player_turn, bishop_heuristic, 10,2, bishop_modified)
        # Rook
        Score += self.board_score_helper_score_cal(board, 5, Player_turn, bishop_heuristic, 25,3, rook_modified)

        return Score

    def board_score(self, board):
        if len(np.where(abs(board) == 1000)[0]) !=2:
            if len(np.where(board == 1000 * self.Player_turn)[0]) == 0:
                return -100000
            else:
                return 100000

        maximizing_player_score = self.board_score_helper(board, self.Player_turn, self.board_state_heuristic_max)
        minimizing_player_score = self.board_score_helper(board, self.Player_turn * -1, self.board_state_heuristic_min)

        return maximizing_player_score - minimizing_player_score


    def remove_middle_col(self, arr):
        return arr[:, [0, 1, 2, 3, 5, 6, 7]]

    def remove_both_side_col(self,arr):
        return arr[:, 1:-1]

    def heuristic_dim_player(self):
        pawn, knight, bishop, rook, queen = self.heuristic()
        if self.dim%2 == 1:
            pawn = self.remove_middle_col(pawn)
            knight = self.remove_middle_col(knight)
            bishop = self.remove_middle_col(bishop)
            rook = self.remove_middle_col(rook)
            queen = self.remove_middle_col(queen)

        if self.dim <=6:
            pawn = self.remove_both_side_col(pawn)
            knight = self.remove_both_side_col(knight)
            bishop = self.remove_both_side_col(bishop)
            rook = self.remove_both_side_col(rook)
            queen = self.remove_both_side_col(queen)


        inverse_pawn = np.flipud(pawn)
        inverse_knight = np.flipud(knight)
        inverse_bishop = np.flipud(bishop)
        inverse_rook = np.flipud(rook)
        inverse_queen = np.flipud(queen)

        board_state_heuristic_white = [pawn, knight, bishop, rook, queen]
        board_state_heuristic_black = [inverse_pawn, inverse_knight, inverse_bishop, inverse_rook, inverse_queen]
        if self.Player_turn == -1:
            return board_state_heuristic_black, board_state_heuristic_white
        return board_state_heuristic_white, board_state_heuristic_black



    def heuristic(self):
        ## Reference: https://github.com/devinalvaro/yachess
        ## Basic Idea was taken from the above link and then the functions was modified
        pawn = np.array([[100, 100, 100, 100, 100, 100, 100, 100],
                         [7,7,7,8,8,7,7,7],
                         [6,6,6,7,7,6,6,6],
                         [5,5,5,6,6,5,5,5],
                         [4,4,4,5,5,4,4,4],
                         [2,2,2,2,2,2,2,2],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [0,0,0,0,0,0,0,0]])

        knight = np.array([[6,6,6,6,6,6,6,6],
                          [6,6,6,6,6,6,6,6],
                         [6,6,6,7,7,6,6,6],
                         [5,5,5,7,7,5,5,5],
                         [4,4,4,5,5,4,4,4],
                         [2,2,2,2,2,2,2,2],
                         [1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1]])

        bishop = np.array([[4,4,4,5,5,4,4,4],
                         [4,4,4,5,5,4,4,4],
                         [4,5,5,6,6,5,5,4],
                         [5,5,5,6,6,5,5,5],
                         [4,4,5,5,5,5,4,4],
                         [2,2,2,2,2,2,2,2],
                           [1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1]])

        rook = np.array([
            [8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8],
            [5, 5, 5, 6, 6, 5, 5, 5],
            [5, 5, 5, 6, 6, 5, 5, 5],
            [5, 5, 5, 6, 6, 5, 5, 5],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])

        queen = np.array([
            [5, 5, 5, 6, 6, 5, 5, 5],
            [5, 5, 5, 6, 6, 5, 5, 5],
            [5, 5, 5, 9, 9, 5, 5, 5],
            [5, 5, 5, 10, 10, 5, 5, 5],
            [5, 5, 5, 10, 10, 5, 5, 5],
            [2, 2, 2, 4, 4, 2, 2, 2],
            [2, 2, 2, 3, 3, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])

        return pawn, knight, bishop, rook, queen