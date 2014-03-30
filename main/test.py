from main.board import Board

__author__ = 'jeremy'

if __name__ == '__main__':
    game_board = Board()
    game_board.generate_new_tile()
    game_board.generate_new_tile()
    game_board.generate_new_tile()
    game_board.generate_new_tile()
    game_board.generate_new_tile()
    game_board.generate_new_tile()
    print(game_board)
    game_board.move_left()
    print(game_board)
    game_board.move_right()
    print(game_board)
    copy_game_board = game_board.get_tiles()
    print(copy_game_board)