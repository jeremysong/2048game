from main.board import Board, Direction

__author__ = 'jeremy'


class Game:
    def __init__(self):
        self.__board = Board()
        self.__movement = {
            Direction.up: self.__board.move_up,
            Direction.down: self.__board.move_down,
            Direction.left: self.__board.move_left,
            Direction.right: self.__board.move_right
        }

    def restart(self):
        self.__board = Board()

    def get_tiles(self):
        """
        Defensive copy
        """
        return self.__board.get_tiles()

    def print_tiles(self):
        print(self.__board)

    def attempt_movement(self):
        movement_list = list()
        for direction in [Direction.left, Direction.down, Direction.right, Direction.up]:
            movable, tiles = self.__board.try_move(direction)
            if movable:
                movement_list.append((direction, tiles))

        return movement_list if len(movement_list) != 0 else None

    def move(self, direction):
        self.__movement[direction]()
        if self.__board.is_win():
            return True
        self.__board.generate_new_tile()