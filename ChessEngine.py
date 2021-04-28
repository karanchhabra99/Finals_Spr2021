### Reference: https://github.com/MikeCreator-put/Chess/tree/887e6d08b27dc79d61a447a8c31236cfb7dbbfbc
# https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick

## Assumption : No Castling
            # Pawn can't check King
import numpy as np
from AIPlayer import *
import copy
import time

class GameState():
    def __init__(self, dim, game_type, modified):
        self.move = Move(dim, modified)
        self.dim = dim
        self.board = self.get_board()
        self.Player_turn = 1
        self.last_move = None
        self.game_type = game_type
        self.modified = modified

        self.game_over = False

        if self.game_type == 1:
            self.player1 = HumanPlayer(self.dim, self.move)
            self.player2 = HumanPlayer(self.dim, self.move)
        elif self.game_type == 2:
            self.player1 = HumanPlayer(self.dim, self.move)
            self.player2 = AIPlayer(self.dim, self.move, -1, modified)
        else:
            self.player1 = AIPlayer(self.dim, self.move, 1, modified)
            self.player2 = AIPlayer(self.dim, self.move, -1, modified)


    def get_board(self):
        board = np.array([
            [-5, -3, -2, -9, -1000, -2, -3, -5],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [5, 3, 2, 9, 1000, 2, 3, 5]])

        # # board[0,:] = np.random.shuffle(board[0,:])

        return copy.deepcopy(board[:,:self.dim])

    def AIvsAI(self):
        if self.Player_turn == 1:
            start_square, end_square = self.player1.play(self.board, self.last_move)
            print(f"White Played: {start_square}, {end_square}")


        elif self.Player_turn == -1:
            start_square, end_square = self.player2.play(self.board, self.last_move)
            print(f"Black Played: {start_square}, {end_square}")

        return start_square, end_square

    def makeMove(self, start_square, end_square):
        flag = 0
        if self.game_type == 3:
            if not self.game_over:
                start_square, end_square = self.AIvsAI()
                flag = 1

        if not self.game_over:
            if self.game_type == 1:
                # Change Player turns and Check if move is valid
                if self.Player_turn == 1:
                    ## Checking if the correct piece is chosen
                    if self.board[start_square[0], start_square[1]] > 0:
                        flag = self.player1.play(self.board, start_square, end_square, self.Player_turn, self.last_move)
                else:
                    if self.board[start_square[0], start_square[1]] < 0:
                        flag = self.player2.play(self.board, start_square, end_square, self.Player_turn, self.last_move)
            elif self.game_type == 2:
                if self.Player_turn == 1:
                    ## Verified Player 2 moves also in case of Game Type 2
                    flag = self.player1.play(self.board, start_square, end_square, self.Player_turn, self.last_move)
                else:
                    flag = 1

        ## Makes the move
        if flag == 1:
            if self.game_type != 1:
                if self.modified == 1:
                    if abs(self.board[start_square[0], start_square[1]]) == 5:
                        self.move.rook.remove_pawns(self.board, (start_square[0], start_square[1]), (end_square[0], end_square[1]))
                if abs(self.board[start_square[0], start_square[1]]) == 1:
                    if (end_square[0] == 0) or (end_square[0] == 7):
                        self.board[start_square[0], start_square[1]] = 9 * self.Player_turn
            self.last_move = (self.board[start_square[0], start_square[1]], end_square[0], end_square[1])
            self.board[end_square[0], end_square[1]] = self.board[start_square[0], start_square[1]]
            self.board[start_square[0], start_square[1]] = 0


            ### Game Over
            if len(np.where(abs(self.board) == 1000)[0]) == 1:
                self.game_over = True
                print("\n\n\nGame Over")
                if self.Player_turn == 1:
                    print("White Wins\n\n\n")
                else:
                    print("Black Wins\n\n\n")


            if self.Player_turn == 1:
                if not self.game_over:
                    self.Player_turn = -1
                    print('\n\nBlacks Turn')
                    if self.game_type == 2:
                        S, E = self.player2.play(self.board, self.last_move)
                        self.makeMove(S, E)
                        print("\n\nWhites Turn")
                        self.Player_turn = 1

            elif self.game_type != 2:
                if not self.game_over:
                    self.Player_turn = 1
                    print("\n\nWhites Turn")

class Pawn():
    def __init__(self, dim):
        self.en_passant_potentials = None
        self.dim = dim
        self.Player_turn = 1

    def pawn_move_checker_en_passant(self, board, current_location, next_location, last_move, Player_turn, AI = False):
        self.Player_turn = Player_turn

        if next_location in self.all_move_pawn(current_location, next_location):
            check = self.is_possible_pawn(board, current_location, next_location, last_move)
            if check[0]:
                flag = 1
                if (next_location[0] == 0):
                    if AI:
                        board[current_location[0], current_location[1]] = self.Player_turn * 9
                    else:
                        new_piece = input("Q or R or K or B: ")
                        if new_piece.lower() == "q":
                            board[current_location[0], current_location[1]] = self.Player_turn * 9
                        elif new_piece.lower() == "r":
                            board[current_location[0], current_location[1]] = self.Player_turn * 5
                        elif new_piece.lower() == "k":
                            board[current_location[0], current_location[1]] = self.Player_turn * 3
                        elif new_piece.lower() == "b":
                            board[current_location[0], current_location[1]] = self.Player_turn * 2
                        else:
                            print("Invalid Input\nConverting the piece to Queen")
                            board[current_location[0], current_location[1]] = self.Player_turn * 9

                ## En passant
                if check[1] == 1:
                    board[current_location[0], next_location[1]] = 0
                return flag
        return 0

    def all_move_pawn(self, start_square, end_square):
        if end_square[1] >= self.dim:
            return []

        return self.all_move_pawn_helper(start_square)


    def all_move_pawn_helper(self, start_square):
        if start_square[0]- 1 < 0:
            return []
        result = [(start_square[0] - 1, start_square[1])]
        if not start_square[0]-2 <= 0:
            result.append((start_square[0] - 2, start_square[1]))
        if not (start_square[1] - 1) < 0:
            result.append((start_square[0] - 1, start_square[1] - 1))
        if (start_square[1] + 1) < self.dim:
            result.append((start_square[0] - 1, start_square[1] + 1))

        return result

    def all_AI_black_move_pawn(self, start_square):#, end_square):
        if start_square[0]+1 >= 8:
            return []

        result = [(start_square[0]+ 1, start_square[1])]
        if not start_square[0]+2 >= 7:
            result.append((start_square[0]+2, start_square[1]))
        if not (start_square[1]-1) < 0:
            result.append((start_square[0]+1, start_square[1]-1))
        if (start_square[1]+1) < self.dim:
            result.append((start_square[0] + 1, start_square[1] + 1))
        return result


    def is_possible_pawn(self, board, current_location, next_location, last_move):
        # Checking if it is attack or straight move
        if board[next_location[0], next_location[1]] == 0:
            ## Straight move
            ## Checking if the move is possible or not
            check= self.is_possible_pawn_helper(board, current_location, next_location)
            ## if the move is possible
            if check[0]:
                ## Checking if the move is 2 steps ahead
                if check[1] ==1:
                    if self.Player_turn == -1:
                        temp_piece = board[next_location[0], next_location[1]]
                        board[next_location[0], next_location[1]] = 25
                        inverse_board = np.flipud(board)
                        inverse_move = np.where(inverse_board == 25)
                        self.en_passant_potentials = (inverse_move[0][0], next_location[1])
                        board[next_location[0], next_location[1]] = temp_piece
                    else:
                        self.en_passant_potentials = next_location
                return (True, 0)

        ## Attach move
        if (current_location[1]+1 == next_location[1]) or (current_location[1]-1 == next_location[1]):
            if current_location[0] - next_location[0] == 1:
                if board[next_location[0], next_location[1]] != 0:
                    return (True, 0)
                if self.en_passant_potentials != None:
                    ## En Passant
                    if last_move != None:
                        if ((last_move[1] == self.en_passant_potentials[0]) and (last_move[2] == self.en_passant_potentials[1])):
                            if (current_location[0] == 3) and (next_location[1] == self.en_passant_potentials[1]):
                                if board[current_location[0], next_location[1]] == self.Player_turn *-1:
                                    return (True, 1)

        return (False, 0)

    def is_possible_pawn_helper(self, board, higher_location_index, lower_location_index):
        ## One move forward
        if higher_location_index[0] - lower_location_index[0] == 1:
            if higher_location_index[1] == lower_location_index[1]:
                return (True, 0)

        ## Two moves forward
        elif higher_location_index[0] - lower_location_index[0] == 2:
            if higher_location_index[0] != board.shape[0] - 2:
                return (False, 0)
            else:
                if board[higher_location_index[0] - 1, higher_location_index[1]] == 0:
                    return (True, 1)
        return (False, 0)

class Knight():
    def __init__(self, dim, modified):
        self.dim = dim
        self.Player_turn = 1
        self.modified = modified

    def knight_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn =Player_turn
        if next_location in self.all_move_knight(current_location, next_location):
            if self.Player_turn == 1:
                if board[next_location[0], next_location[1]] <= 0:
                    return 1
            else:
                if board[next_location[0], next_location[1]] >= 0:
                    return 1
        return 0
    ## end_sqaure(8<, self.dim<)
    def all_move_knight(self, start_square, end_square):
        if end_square[1] >= self.dim:
            return []
        return self.all_move_knight_helper(start_square)

    def all_move_knight_helper(self, start_square):
        result = []
        if self.modified == 1:
            jump = 3
        else:
            jump = 2
        if start_square[0] + 1 < 8:
            if start_square[1] + jump < self.dim:
                result.append((start_square[0] + 1, start_square[1] + jump))
            if start_square[1] - jump >= 0:
                result.append((start_square[0] + 1, start_square[1] - jump))
        if start_square[0] - 1 >= 0:
            if start_square[1] + jump < self.dim:
                result.append((start_square[0] - 1, start_square[1] + jump))
            if start_square[1] - jump >= 0:
                result.append((start_square[0] - 1, start_square[1] - jump))
        if start_square[0] + jump < 8:
            if start_square[1] + 1 < self.dim:
                result.append((start_square[0] + jump, start_square[1] + 1))
            if start_square[1] - 1 >= 0:
                result.append((start_square[0] + jump, start_square[1] - 1))
        if start_square[0] - jump >= 0:
            if start_square[1] + 1 < self.dim:
                result.append((start_square[0] - jump, start_square[1] + 1))
            if start_square[1] - 1 >= 0:
                result.append((start_square[0] - jump, start_square[1] - 1))
        return result

class Bishop():
    def __init__(self, dim, modified):
        self.dim = dim
        self.Player_turn = 1
        self.modified = modified

    ## go through
    def bishop_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn = Player_turn
        if next_location in self.diagonal_moves(board, current_location, Player_turn):
            return 1
        return 0

    ## all_move
    def diagonal_moves(self, board, current_location, Player_turn):
        self.Player_turn = Player_turn
        all_moves = []
        forward_col = current_location[1]
        backward_col = current_location[1]
        for i in range(current_location[0]+1, 8):
            forward_col, backward_col = self.diagonal_moves_helper(board, i, forward_col, backward_col, all_moves)

        forward_col = current_location[1]
        backward_col = current_location[1]
        for i in range(current_location[0]-1, -1, -1):
            forward_col, backward_col = self.diagonal_moves_helper(board, i, forward_col, backward_col, all_moves)

        return all_moves

    def diagonal_moves_helper(self, board, i, forward_col, backward_col, all_moves):
        forward_col += 1
        backward_col -= 1
        if forward_col <= self.dim - 1:
            forward_col = self.diagonal_moves_helpers_helper(board, i, forward_col, all_moves, 'forward')

        if not backward_col < 0:
            backward_col = self.diagonal_moves_helpers_helper(board, i, backward_col, all_moves, 'backward')

        return forward_col, backward_col

    def diagonal_moves_helpers_helper(self, board, i, col, all_moves, direction):
        if board[i, col] == 0:
            all_moves.append((i, col))
        elif board[i, col] < 0:
            if self.Player_turn == 1:
                all_moves.append((i, col))
                if self.modified == 1:
                    if direction == 'forward':
                        col = self.dim
                    else:
                        col = 0
            if self.modified !=1:
                ## Intend the below logic to make the bishop jump accross his pieces
                if direction == 'forward':
                    col = self.dim
                else:
                    col = 0
        elif board[i, col] > 0:
            if self.Player_turn == -1:
                all_moves.append((i, col))
                if self.modified == 1:
                    ## Intend the below logic to make the bishop jump accross his pieces
                    if direction == 'forward':
                        col = self.dim
                    else:
                        col = 0

            if self.modified !=1:
                ## Intend the below logic to make the bishop jump accross his pieces
                if direction == 'forward':
                    col = self.dim
                else:
                    col = 0
        else:
            col = self.dim

        return col


class Rook:
    def __init__(self, dim, modified):
        self.dim = dim
        self.Player_turn = 1
        self.modified = modified

    def rook_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn = Player_turn
        if next_location in self.straight_moves(board, current_location, Player_turn):
            if self.modified == 1:
                self.remove_pawns(board, current_location, next_location)
            return 1
        return 0


    def remove_pawns(self, board, current_location, next_location):
        if current_location[0] == next_location[0]:
            if current_location[1] < next_location[1]:
                for i in range(current_location[1]+1, next_location[1]):
                    board[current_location[0], i] = 0
            else:
                for i in range(current_location[1]-1, next_location[1], -1):
                    board[current_location[0], i] = 0

        else:
            if current_location[0] < next_location[0]:
                for i in range(current_location[0]+1, next_location[0]):
                    board[i, current_location[1]] = 0
            else:
                for i in range(current_location[0]-1, next_location[0], -1):
                    board[i, current_location[1]] = 0

        return


    def straight_moves(self, board, current_location, Player_turn):
        self.Player_turn = Player_turn
        all_moves = []
        i = current_location[0]+1
        while 8 > i:
            i = self.straight_moves_col_helper(board, i, current_location, all_moves, 'forward')
        i = current_location[0]-1
        while 0 <= i:
            i = self.straight_moves_col_helper(board, i, current_location, all_moves, 'backward')

        ## Horizontal
        i = current_location[1]+1
        while self.dim > i:
            i = self.straight_moves_horizontal_helper(board, i, current_location, all_moves, 'forward')
        i = current_location[1]-1
        while 0 <= i:
            i = self.straight_moves_horizontal_helper(board, i, current_location, all_moves, 'backward')
        return all_moves

    def straight_moves_col_helper(self, board, i, current_location, all_moves, direction):
        if board[i, current_location[1]] == 0:
            all_moves.append((i, current_location[1]))
        elif board[i, current_location[1]] < 0:
            if self.Player_turn == 1:
                all_moves.append((i, current_location[1]))
                if self.modified == 1:
                    if direction == 'forward':
                        i = 8
                    else:
                        i = 0
            if self.modified != 1:
                if direction == 'forward':
                    i = 8
                else:
                    i = 0
        elif board[i, current_location[1]] > 0:
            if self.Player_turn == -1:
                all_moves.append((i, current_location[1]))
                if self.modified ==1:
                    if direction == 'forward':
                        i = 8
                    else:
                        i = 0
            if self.modified !=1:
                if direction == 'forward':
                    i = 8
                else:
                    i = 0
        else:
            i = 8
        if direction == 'forward':
            i+=1
        else:
            i-=1
        return i

    def straight_moves_horizontal_helper(self, board, i, current_location, all_moves, direction):
        if board[current_location[0], i] == 0:
            all_moves.append((current_location[0], i))
        elif board[current_location[0], i] < 0:
            if self.Player_turn == 1:
                all_moves.append((current_location[0], i))
                if self.modified == 1:
                    if direction == 'forward':
                        i = 8
                    else:
                        i = 0
            if self.modified != 1:
                if direction == 'forward':
                    i = 8
                else:
                    i = 0
        elif board[current_location[0], i] > 0:
            if self.Player_turn == -1:
                all_moves.append((current_location[0], i))
                if self.modified == 1:
                    if direction == 'forward':
                        i = 8
                    else:
                        i = 0
            if self.modified != 1:
                if direction == 'forward':
                    i = 8
                else:
                    i = 0
        else:
            i = 8
        if direction == 'forward':
            i+=1
        else:
            i-=1
        return i

class Queen():
    def __init__(self, dim):
        self.dim = dim
        self.Player_turn = 1
        self.bishop = Bishop(dim,0)
        self.rook = Rook(dim, 0)

    def queen_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn = Player_turn
        all_moves = self.rook.straight_moves(board, current_location, Player_turn) + self.bishop.diagonal_moves(board, current_location, Player_turn)
        if next_location in all_moves:
            return 1
        return 0

class King():
    def __init__(self, dim):
        self.dim = dim
        self.Player_turn = 1

    def king_move_checker(self, board, current_location, next_location, Player_turn):
        self.Player_turn = Player_turn
        if next_location in self.king_moves(board, current_location, Player_turn):
            return 1
        return 0

    def king_moves(self, board, current_location, Player_turn):
        all_move =[]
        row_plus = False
        row_minus = False
        col_plus = False
        col_minus = False

        # row
        if current_location[0] + 1 < 8:
            self.king_moves_helper(board, current_location[0] + 1, current_location[1],Player_turn, all_move)
            row_plus= True
        if current_location[0] - 1 >= 0:
            self.king_moves_helper(board, current_location[0] - 1, current_location[1],Player_turn,  all_move)
            row_minus = True

        # Col
        if current_location[1] + 1 < self.dim:
            self.king_moves_helper(board, current_location[0], current_location[1]+1,Player_turn,  all_move)
            col_plus = True
        if current_location[1] - 1 >= 0:
            self.king_moves_helper(board, current_location[0], current_location[1]-1,Player_turn, all_move)
            col_minus = True

        if (row_plus and col_plus):
            self.king_moves_helper(board, current_location[0] + 1, current_location[1] + 1,Player_turn, all_move)

        if (row_plus and col_minus):
            self.king_moves_helper(board, current_location[0] + 1, current_location[1] - 1,Player_turn, all_move)

        if (row_minus and col_plus):
            self.king_moves_helper(board, current_location[0] - 1, current_location[1] + 1,Player_turn, all_move)

        if (row_minus and col_minus):
            self.king_moves_helper(board, current_location[0] - 1, current_location[1] - 1,Player_turn, all_move)
        return all_move

    def king_moves_helper(self, board, row, col, Player_turn, all_move):
        if Player_turn == 1:
            if board[row, col] <= 0:
                all_move.append((row, col))
        else:
            if board[row, col] >= 0:
                all_move.append((row, col))


class Move():
    def __init__(self, dim, modified):
        # self.king_first_move = False
        # self.rook_first_move = {}
        self.pawn = Pawn(dim)
        self.knight = Knight(dim, modified)
        self.bishop = Bishop(dim, modified)
        self.rook = Rook(dim, modified)
        self.queen = Queen(dim)
        self.king = King(dim)
        self.dim = dim
        self.Player_turn = 1

    def check_piece_and_play(self, board, current_location, next_location, Player_turn, last_move, AI = False):
        self.Player_turn = Player_turn
        if board[current_location[0], current_location[1]] == self.Player_turn * 1:
            ## Flipping the board for black player
            if board[current_location[0], current_location[1]] == -1:
                temp1 = board[current_location[0], current_location[1]]
                board[current_location[0], current_location[1]] = 25
                black_board = np.flipud(board)
                inverse_start = np.where(black_board == 25)
                board[current_location[0], current_location[1]] = temp1

                temp2 = board[next_location[0], next_location[1]]
                board[next_location[0], next_location[1]] = 25
                inverse_end = np.where(black_board == 25)
                board[next_location[0], next_location[1]] = temp2
                return self.pawn.pawn_move_checker_en_passant(black_board, inverse_start, inverse_end, last_move,
                                                              Player_turn, AI)
            else:
                return self.pawn.pawn_move_checker_en_passant(board, current_location, next_location, last_move, Player_turn, AI)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 2:
            return self.bishop.bishop_move_checker(board, current_location, next_location, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 3:
            return self.knight.knight_move_checker(board, current_location, next_location, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 5:
            return self.rook.rook_move_checker(board, current_location, next_location, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 9:
            return self.queen.queen_move_checker(board, current_location, next_location, Player_turn)
        elif board[current_location[0], current_location[1]] == self.Player_turn * 1000:
            return self.king.king_move_checker(board, current_location, next_location, Player_turn)
        else:
            return 0

class HumanPlayer():
    def __init__(self, dim, move):
        self.move = move

    def play(self, board, current_location, next_location, Player_turn, last_move):
        # Checks if the move is valid
        return self.move.check_piece_and_play(board, current_location, next_location, Player_turn, last_move)

''''
Big-O

3 piece modifications: Karan

'''