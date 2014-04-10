import operator

import numpy as np

from main.game import Game


__author__ = 'jeremy'


def decision_function(movements, old_tiles, merge_param, monotonic_param, dup_param, occupation_param):
    """
    Calculates based on the decision function.

    Returns the best(largest decision function output) movement.
    """
    direction_dict = dict()
    old_tiles_list = list()
    [old_tiles_list.extend(filter(lambda t: t != 0, row)) for row in old_tiles]
    # Maximize merge
    for (direction, tiles) in movements:
        tiles_list = list()
        [tiles_list.extend(filter(lambda t: t != 0, row)) for row in tiles]
        for element in old_tiles_list:
            try:
                tiles_list.remove(element)
            except ValueError:
                continue
        direction_dict[direction] = sum(tiles_list) * merge_param

    # Rewards monotonic, duplicates and occupation
    for (direction, tiles) in movements:
        monitonic_value = 0
        dup_value = 0
        occupation_value = 0
        for i in range(0, 4):
            prev = tiles[i][0]
            for j in range(1, 4):
                if prev != 0:
                    occupation_value += i + j
                if prev > tiles[i][j]:
                    monitonic_value += prev - tiles[i][j]
                    # monotonic_value += 1
                if prev == tiles[i][j] and prev != 0:
                    dup_value += prev * 2
                prev = tiles[i][j]

        for j in range(0, 4):
            prev = tiles[j][0]
            for i in range(1, 4):
                if prev != 0:
                    occupation_value += i + j
                if prev > tiles[i][j]:
                    monitonic_value += prev - tiles[i][j]
                    # monotonic_value += 1
                if prev == tiles[i][j] and prev != 0:
                    dup_value += prev * 2
                prev = tiles[i][j]

        direction_dict[direction] += monitonic_value * -monotonic_param + dup_value * dup_param + \
                                     occupation_value * occupation_param

    # print(direction_dict)

    return max(direction_dict.iteritems(), key=operator.itemgetter(1))[0]


def simulate(merge_param, monotonic_param, dup_param, occupation_param, vobose=False):
    """
    Simulates 2048 game.

    Returns True if win; otherwise, returns False.
    """
    game = Game()

    while True:
        movements = game.attempt_movement()
        if movements is None:
            # print("Lose")
            game.print_max_tile()
            if vobose:
                game.print_tiles()
            return False
        if vobose:
            game.print_tiles()
        max_direction = decision_function(movements, game.get_tiles(), merge_param, monotonic_param, dup_param,
                                      occupation_param)
        if game.move(max_direction):
            if vobose:
                game.print_tiles()
            return True


if __name__ == '__main__':
    # merge_param_list = np.arange(0.5, 5.5, 0.5)
    # monotonic_param_list = np.arange(0.5, 5.5, 0.5)
    # dup_param_list = np.arange(0.5, 5.5, 0.5)
    # occupation_param_list = np.arange(0.5, 5.5, 0.5)

    merge_param_list = [5.0]
    monotonic_param_list = [4.5]
    dup_param_list = [4.5]
    occupation_param_list = [1.5]

    for merge_param in merge_param_list:
        for monotonic_param in monotonic_param_list:
            for dup_param in dup_param_list:
                for occupation_param in occupation_param_list:
                    win = 0
                    for count in range(0, 5000):
                        if simulate(merge_param, monotonic_param, dup_param, occupation_param, vobose=False):
                            win += 1

                    if win > 0:
                        print(
                            "merge_param: {0}, monotonic param: {1}, dup_param: {2}, occupation_param: {3}, win: {4}/100".format(
                                merge_param, monotonic_param, dup_param, occupation_param, win))
