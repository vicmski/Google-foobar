"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as
raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may
be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state
of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions
it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each
time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).
You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms
that the ore can become, but you haven't seen all of them.

Write a function answer(m) that takes an array of array of non-negative ints representing how many times that state
has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each
terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in
simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a
path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The
ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the
fraction is simplified regularly.

For example, consider the matrix m:
[
    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
    [0,0,0,0,0,0],  # s3 is terminal
    [0,0,0,0,0,0],  # s4 is terminal
    [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) m = [
               [0, 2, 1, 0, 0],
               [0, 0, 0, 3, 4],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]
           ]
Output:
    (int list) [7, 6, 8, 21]

Inputs:
    (int) m = [
               [0, 1, 0, 0, 0, 1],
               [4, 0, 0, 3, 2, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]
           ]
Output:
    (int list) [0, 3, 2, 9, 14]
"""


import unittest
from fractions import gcd


def lcm(a, b):
    result = a * b / gcd(a, b)

    return result


def lcm_for_arrays(*args):
    array_length = len(args)
    if array_length <= 2:
        return lcm(*args)

    initial = lcm(args[0], args[1])
    i = 2
    while i < array_length:
        initial = lcm(initial, args[i])
        i += 1
    return initial


def return_terminal_states(row_sum):
    return [index for index, item in enumerate(row_sum) if item == 0]


def change_denominator(array, final_denominator):
    current_denominator = array[len(array) - 1]
    multiply_array = lcm(current_denominator, final_denominator)/current_denominator
    return map(lambda x: x * multiply_array, array)


def answer(m):
    row_sum = [sum(item) for item in m]

    terminal_states = return_terminal_states(row_sum)

    result = [0]*(len(terminal_states) + 1)

    last_result_item = len(result) - 1

    result[last_result_item] = row_sum[0]

    if row_sum[0] == 0:
        result[0] = 1
        result[last_result_item] = 1
        return result

    for stateIndex, value in enumerate(m[0]):
        if stateIndex in terminal_states:
            result[terminal_states.index(stateIndex)] += value * (result[last_result_item] / row_sum[0])
        else:
            result = change_denominator(result, row_sum[stateIndex])
            if stateIndex != 0:
                for state_key, state_chance in enumerate(m[stateIndex]):
                    if state_key in terminal_states:
                        result[terminal_states.index(state_key)] += state_chance * value

    return result


class TestAnswer(unittest.TestCase):
    def test1(self):
        test_input = [
            [0, 2, 1, 0, 0],
            [0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.assertEqual(answer(test_input),
                         [7, 6, 8, 21])

    def test2(self):
        test_input = [
            [0, 1, 0, 0, 0, 1],
            [4, 0, 0, 3, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.assertEqual(answer(test_input), [0, 3, 2, 9, 14])
