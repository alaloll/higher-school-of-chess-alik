from copy import deepcopy
from typing import Union, Literal, cast

from board import Board
from game.index_notation import index_to_notation
from game.pieces.king import King
from index_notation import notation_to_index

PieceColor = Union[Literal["white"], Literal["black"]]


class ChessGame:
    def __init__(self, game_time, increment) -> None:
        self.white_timer = game_time
        self.black_timer = game_time
        self.increment = increment
        self.current_player_color: PieceColor = "white"
        self.board_main = Board()
        self.white_king = (7, 4)
        self.black_king = (0, 4)
        self.result = None

    def invert_current_player_color(self) -> None:
        self.current_player_color = "black" if self.current_player_color == "white" else "white"

    def start_game(self) -> None:
        self.board_main.start_board()
        self.board_main.print_board()
        while self.result is None:
            print(f"{self.current_player_color}'s turn")
            args = input().split()
            if len(args) != 2:
                if len(args) == 1 and args[0].lower() == "draw":
                    print("Write 'accept' to accept the draw.")
                    ans_to_draw = input()
                    if ans_to_draw.lower() == "accept":
                        self.result = "draw"
                else:
                    pass
                    # self.help()
            elif args[0].lower() + " " + args[1].lower() == "give up":
                if self.current_player_color == "white":
                    self.result = "black won"
                else:
                    self.result = "white won"
            else:
                from_position, to_position = args
                self.move(from_position, to_position)

    def get_possible_moves(self, from_position: str) -> list[tuple[int, int]]:
        try:
            from_position_index = notation_to_index(from_position)
        except ValueError as ve:
            print(f"Ошибка формата клетки: {ve}")
            return []
        board = deepcopy(self.board_main)
        from_square = board[from_position_index]
        if from_square is None:
            return []
        elif from_square.color != self.current_player_color:
            return []
        else:
            board_sup = deepcopy(board)
            uncut_possible_moves = from_square.show_possible_moves(board_sup.board)
            possible_moves = []
            for move in uncut_possible_moves:
                from_square.move(move, board_sup.board)
                print("BOARD_SUP")
                board_sup.print_board()
                if self.current_player_color == "white":
                    if not cast(King, board_sup[self.white_king]).is_in_check(board_sup.board):
                        possible_moves.append(move)
                elif not cast(King, board_sup[self.black_king]).is_in_check(board_sup.board):
                        possible_moves.append(move)

            return possible_moves


    def move(self, from_position: str, to_position: str) -> None:
        try:
            from_position_index = notation_to_index(from_position)
            to_position_index = notation_to_index(to_position)
        except ValueError as ve:
            print(f"Ошибка формата хода: {ve}")
            self.board_main.print_board()
            return
        from_square = self.board_main[from_position_index]
        if to_position_index not in self.get_possible_moves(from_position):
            print("Impossible move")
            return
        else:
            if from_square.move(to_position_index, self.board_main.board):
                if type(self.board_main[to_position_index]) == King:
                    if self.current_player_color == "white":
                        self.white_king = to_position_index
                    else:
                        self.black_king = to_position_index
                self.invert_current_player_color()
                self.check_game_over()
        self.board_main.print_board()

    def check_game_over(self) -> bool:
        if self.current_player_color == "white":
            i, j = self.white_king
        else:
            i, j = self.black_king
        if self.board_main[i, j].show_possible_moves(self.board_main.board):
            return False
        for k in range(8):
            for t in range(8):
                board_k_t = self.board_main[k, t]
                if board_k_t is not None:
                    if board_k_t.color == self.current_player_color and board_k_t.show_possible_moves(self.board_main.board):
                        return False

        if cast(King, self.board_main[i, j]).is_in_check(self.board_main.board):
            if self.current_player_color == "white":
                self.result = "black won"
            else:
                self.result = "white won"
        else:
            self.result = "draw"
