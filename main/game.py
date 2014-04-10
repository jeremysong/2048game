from main.board import Board, Direction

__author__ = 'jeremy'


class Game:
    def __init__(self):
        """
        Constructor. Create new game board.
        """
        self.__board = Board()
        self.__movement = {
            Direction.up: self.__board.move_up,
            Direction.down: self.__board.move_down,
            Direction.left: self.__board.move_left,
            Direction.right: self.__board.move_right
        }

    def restart(self):
        """
        Restarts game board.
        """
        self.__board = Board()

    def get_tiles(self):
        """
        Defensive copy of current board tiles.
        """
        return self.__board.get_tiles()

    def print_tiles(self):
        print(self.__board)

    def print_max_tile(self):
        print(max([tile for sublist in self.get_tiles() for tile in sublist]))

    def attempt_movement(self):
        """
        Tries all possible movements. Returns a list of (direction, tiles after movement) tuples.
        """
        movement_list = list()
        for direction in [Direction.left, Direction.down, Direction.right, Direction.up]:
            movable, tiles = self.__board.try_move(direction)
            if movable:
                movement_list.append((direction, tiles))

        return movement_list if len(movement_list) != 0 else None

    def move(self, direction):
        """
        Move tiles towards a specific redirection.

        Returns True if win. Otherwise, returns None.
        """
        self.__movement[direction]()
        if self.__board.is_win():
            return True
        self.__board.generate_new_tile()