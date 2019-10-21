"""
    Expanding Nebula
    ================

    You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies.
    But - oh no! - one of the escape pods has flown into a nearby nebula, causing you to lose track of it. You start
    monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. However, you do find
    that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine
    the previous state of the gas and narrow down where you might find the pod.

    From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can
    model it as a 2D grid. You find that the current existence of gas in a cell of the grid is determined exactly by its
    4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the
    cell below and to the right of it. If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas,
    then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

    For example, let's say the previous state of the grid (p) was:
    .O..
    ..O.
    ...O
    O...

    To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of
    cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which
    means this 2x2 block would become cell c[0][0] with gas in the next time step:
    .O -> O
    ..

    Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the
    containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:
    O. -> .
    .O

    Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
    O.O
    .O.
    O.O

    Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

    Write a function answer(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.  The answer will always be less than one billion (10^9).

    Languages
    =========

    To provide a Python solution, edit solution.py
    To provide a Java solution, edit solution.java

    Test cases
    ==========

    Inputs:
        (boolean) g = [
                        [true, false, true],
                        [false, true, false],
                        [true, false, true]
                      ]
    Output:
        (int) 4

    Inputs:
        (boolean) g = [
                        [true, false, true, false, false, true, true, true],
                        [true, false, true, false, false, false, true, false],
                        [true, true, true, false, false, false, true, false],
                        [true, false, true, false, false, false, true, false],
                        [true, false, true, false, false, true, true, true]
                      ]
    Output:
        (int) 254

    Inputs:
        (boolean) g = [
                        [true, true, false, true, false, true, false, true, true, false],
                        [true, true, false, false, false, false, true, true, true, false],
                        [true, true, false, false, false, false, false, false, false, true],
                        [false, true, false, false, false, false, true, true, false, false]
                      ]
    Output:
        (int) 11567

"""
import unittest

from collections import defaultdict


def find_overlap(column1, column2, column_size):
    c1brs = column1 & ~(1 << column_size)  # Column 1 bottom right side
    c1urs = column1 >> 1  # Column 1 upper right side
    c2brs = column2 & ~(1 << column_size)  # Column 2 bottom right side
    c2urs = column2 >> 1  # Column 2 upper right side

    return (c1brs & ~c2brs & ~c1urs & ~c2urs) | (~c1brs & c2brs & ~c1urs & ~c2urs) | (~c1brs & ~c2brs & c1urs & ~c2urs) | (~c1brs & ~c2brs & ~c1urs & c2urs)


def get_binary_number_from_row(row):
    return sum([(1 << key) * value for key, value in enumerate(row)])


def answer(g):
    if len(g[0]) > len(g):
        g = list(zip(*g))  # Make sure we always have shorter column

    column_count = len(g[0])

    columns_as_binary_numbers = [get_binary_number_from_row(row) for row in g]
    columns_as_binary_numbers_set = set(columns_as_binary_numbers)

    previous_column_states = {previous_state: 1 for previous_state in range(1 << (column_count+1))}

    overlapping_column_states_cache = defaultdict(set)

    for previous_state in range(1 << (column_count + 1)):
        for next_state in range(1 << (column_count + 1)):
            overlap = find_overlap(previous_state, next_state, column_count)

            if overlap in columns_as_binary_numbers_set:
                overlapping_column_states_cache[(overlap, previous_state)].add(next_state)

    for column_value in columns_as_binary_numbers:
        next_column = defaultdict(int)
        for previous_column_state in previous_column_states:
            for overlapping_column_state in overlapping_column_states_cache[(column_value, previous_column_state)]:
                next_column[overlapping_column_state] += previous_column_states[previous_column_state]

        previous_column_states = next_column

    return sum(previous_column_states.values())


class TestExpandingNebula(unittest.TestCase):
    def test1(self):
        test_input = [
                        [True, True, False, True, False, True, False, True, True, False],
                        [True, True, False, False, False, False, True, True, True, False],
                        [True, True, False, False, False, False, False, False, False, True],
                        [False, True, False, False, False, False, True, True, False, False]
                      ]
        self.assertEqual(answer(test_input), 11567)

    def test2(self):
        test_input = [
                        [True, False, True, False, False, True, True, True],
                        [True, False, True, False, False, False, True, False],
                        [True, True, True, False, False, False, True, False],
                        [True, False, True, False, False, False, True, False],
                        [True, False, True, False, False, True, True, True]
                      ]
        self.assertEqual(answer(test_input), 254)

    def test3(self):
        test_input = [
                        [False, False, False, False]
                      ]
        self.assertEqual(answer(test_input), 380)
