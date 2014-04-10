import copy
import random

from enum import Enum


__author__ = 'jeremy'


class Direction(Enum):
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'


class Board:
    """
    Game board, where all 16 tiles are placed on.
    """
    def __init__(self):
        """
        Creates a 4*4 board and generates a new tile randomly.
        """
        self.__tiles = list()
        for i in range(0, 4):
            self.__tiles.append([0, 0, 0, 0])

        self.generate_new_tile()

    def get_empty_tile(self):
        """
        Gets current empty tiles.
        """
        empty_tiles = list()
        for i in range(0, 4):
            for j in range(0, 4):
                if self.__tiles[i][j] == 0:
                    empty_tiles.append((i, j))
        return empty_tiles

    def generate_new_tile(self):
        """
        Randomly generates a new tile from empty tiles.
        """
        empty_tiles = self.get_empty_tile()
        tile_tuple = random.choice(empty_tiles)
        random_int = random.choice(range(0, 10))
        if random_int == 9:
            self.__tiles[tile_tuple[0]][tile_tuple[1]] = 4
        else:
            self.__tiles[tile_tuple[0]][tile_tuple[1]] = 2

    def try_move(self, direction):
        """
        Tries to move towards a specific direction. Tiles will be restored after this movement.

        Returns a boolean indicating if this direction is available and new tiles
        """
        old_tiles = copy.deepcopy(self.__tiles)
        movements = {
            Direction.up: self.move_up,
            Direction.down: self.move_down,
            Direction.left: self.move_left,
            Direction.right: self.move_right
        }
        movements[direction]()
        movable = does_tile_change(self.__tiles, old_tiles)
        new_tiles = copy.deepcopy(self.__tiles)
        self.__tiles = old_tiles
        return movable, new_tiles

    def move_up(self):
        """
        Moves all tiles up.
        """
        for j in range(0, 4):
            j_column = list()
            for i in range(0, 4):
                j_column.append(self.__tiles[i][j])

            j_column_merge = merge_list(j_column)

            for i in range(0, 4):
                self.__tiles[i][j] = j_column_merge[i] if i < len(j_column_merge) else 0

    def move_down(self):
        """
        Moves all tiles down.
        """
        for j in range(0, 4):
            j_column = list()
            for i in range(3, -1, -1):
                j_column.append(self.__tiles[i][j])

            j_column_merge = merge_list(j_column)
            for i in range(3, -1, -1):
                self.__tiles[i][j] = j_column_merge[3 - i] if 3 - i < len(j_column_merge) else 0

    def move_left(self):
        """
        Moves all tiles left.
        """
        for i in range(0, 4):
            i_row = list()
            for j in range(0, 4):
                i_row.append(self.__tiles[i][j])

            i_row_merge = merge_list(i_row)
            for j in range(0, 4):
                self.__tiles[i][j] = i_row_merge[j] if j < len(i_row_merge) else 0

    def move_right(self):
        """
        Moves all tiles right.
        """
        for i in range(0, 4):
            i_row = list()
            for j in range(3, -1, -1):
                i_row.append(self.__tiles[i][j])

            i_row_merge = merge_list(i_row)
            for j in range(3, -1, -1):
                self.__tiles[i][j] = i_row_merge[3 - j] if 3 - j < len(i_row_merge) else 0

    def is_win(self):
        """
        Returns True if 2048 presents in tiles. Otherwise, False.
        """
        tiles = list()
        [tiles.extend(row) for row in self.__tiles]
        # return 2048 in tiles
        return False

    def is_lose(self):
        """
        Returns True if no empty tiles. Otherwise, False.
        """
        return len(self.get_empty_tile()) == 0

    def get_tiles(self):
        """
        Defensive copy of all tiles.
        """
        return copy.deepcopy(self.__tiles)

    def __str__(self):
        """
        String representation.
        """
        represent = ''
        for i in range(0, 4):
            represent += '\t'.join(map(lambda element: str(element) if element != 0 else 'x', self.__tiles[i]))
            represent += '\n'
        return represent


def merge_list(old_list):
    """
    Merges same tiles.
    """
    # Remove 0s from list
    list_value = filter(lambda t: t != 0, old_list)
    list_merge = list()

    index = 0
    while index < len(list_value):
        if index < len(list_value) - 1 and list_value[index] == list_value[index + 1]:
            list_merge.append(list_value[index] * 2)
            index += 2
        else:
            list_merge.append(list_value[index])
            index += 1

    return list_merge


def does_tile_change(new_tiles, old_tiles):
    """
    Returns True if new board is different from the old one. Otherwise, False.
    """
    new_tiles_list = list()
    old_tiles_list = list()
    [new_tiles_list.extend(row) for row in new_tiles]
    [old_tiles_list.extend(row) for row in old_tiles]

    for i in range(0, 16):
        if new_tiles_list[i] != old_tiles_list[i]:
            return True

    return False