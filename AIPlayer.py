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

        ## ToDo: After board_score is set-up
        self.count = 1

    def play(self, board, last_move):
        _, cur = self.Minimax(board, self.Player_turn, last_move, self.dept)
        print(f"Top: {cur}")
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

        #Pawn Best move
        ## ToDo: Make the output of 2 parameters
        # pawn_best_score, pawn_best_move = self.pawn_best_move(board, Player_turn, Score, best_move, last_move, dept)
        #Knight Best Move
        Score, best_move = self.knight_best_move(board, Player_turn, Score, best_move, dept)
        ## Bishop Best Move
        Score, best_move = self.bishop_best_move(board, Player_turn, Score, best_move, dept)

        # print(f"minmax {knight_best_move}")
        return Score, best_move

    def all_moves_helper(self, board, last_move_all, all_pieces, p, each_move, Player_turn, dept, best_move, Score):
        board_all = copy.deepcopy(board)

        last_move_all = (board_all[all_pieces[0][p], all_pieces[1][p]], each_move[0], each_move[1])
        board_all[each_move[0], each_move[1]] = board_all[all_pieces[0][p], all_pieces[1][p]]
        board_all[all_pieces[0][p], all_pieces[1][p]] = 0

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

    def bishop_best_move(self, board, Player_turn, Score, best_move, dept):
        all_bishop = np.where(board == 2 * Player_turn)
        for p in range(len(all_bishop[0])):
            all_bishop_moves = self.move.bishop.diagonal_moves(board, (all_bishop[0][p], all_bishop[1][p]), Player_turn)

            for each_move in all_bishop_moves:
                Score, best_move =self.all_moves_helper(board, None, all_bishop, p, each_move, Player_turn, dept, best_move,
                                 Score)

        return Score, best_move


    def knight_best_move(self, board, Player_turn, Score, best_move, dept):
        ## ToDo: Reduce Redandancy
        all_knight = np.where(board == 3 * Player_turn)
        for p in range(len(all_knight[0])):

            all_knight_moves = self.move.knight.all_move_knight_helper((all_knight[0][p], all_knight[1][p]))

            for each_move in all_knight_moves:
                if self.move.knight.knight_move_checker(board, (all_knight[0][p], all_knight[1][p]), (each_move[0], each_move[1]), Player_turn) == 1:
                    board_k = copy.deepcopy(board)

                    ## Making changes on the board
                    last_move_k = (board_k[all_knight[0][p], all_knight[1][p]], each_move[0], each_move[1])
                    board_k[each_move[0], each_move[1]] = board_k[all_knight[0][p], all_knight[1][p]]
                    board_k[all_knight[0][p], all_knight[1][p]] = 0
                    # print(p, best_move)
                    eval, best_move = self.Minimax(board_k, Player_turn * -1, last_move_k, dept - 1, best_move)

                    # print(dept, Player_turn, best_move, [(all_pawns[0][p], all_pawns[1][p]), each_move])
                    # print(f"Score: {Score}, Eval: {eval} Dept: {dept} Total_Dept: {self.dept}, Best Move: {best_move}, Player_Turn: {Player_turn}")
                    if eval != None:
                        if self.Player_turn == Player_turn:
                            Score = max(Score, eval)
                            # print(board_k)
                        else:
                            Score = min(Score, eval)
                            # print(board_k)

                        if Score == eval:
                            if dept == self.dept:
                                best_move = [(all_knight[0][p], all_knight[1][p]), each_move]
                                # print(f"Minmax_knight_helper: {Score},  {best_move}")
        # print(f"Score: {Score}, Eval: {eval} Dept: {dept} Total_Dept: {self.dept}")
        return Score, best_move














    def pawn_best_move(self, board, Player_turn, Score, best_move, last_move, dept):
        all_pawns = np.where(board == 1 * Player_turn)
        ## ToDo: Uncomment
        for p in range(1):#===len(all_pawns[0])):
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
        # print(f"pawn_best_move: {best_move}")
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
        print(dept)
        eval = self.Minimax(board_p, Player_turn * -1, last_move_p, dept -1, best_move)

        # print(dept, Player_turn, best_move, [(all_pawns[0][p], all_pawns[1][p]), each_move])
        if eval != None:
            if self.Player_turn == Player_turn:
                Score = max(Score, eval)

            else:
                Score = min(Score, eval)

            print(f"Score: {Score}, Eval: {eval} Dept: {dept} Total_Dept: {self.dept}")
            if Score == eval:
                if dept == self.dept:
                    print("\n\n\nInside")
                    best_move = [(all_pawns[0][p], all_pawns[1][p]), each_move]
        print(f"Minmax_pawn_helper: {best_move}")
        return Score, best_move

    def board_score(self, board):
        ## ToDo:
        self.count+= 1
        if self.count < 70:
            # print(board)
            # print(self.count)
            return self.count

        else:
            return -self.count