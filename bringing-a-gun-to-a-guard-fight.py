"""
Bringing a Gun to a Guard Fight
===============================

Uh-oh - you've been cornered by one of Commander Lambdas elite guards! Fortunately, you grabbed a beam weapon from an
abandoned guard post while you were running through the station, so you have a chance to fight your way out. But the
beam weapon is potentially dangerous to you as well as to the elite guard: its beams reflect off walls,
meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know
that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits
either you or the guard, it will stop immediately (albeit painfully).

Write a function solution(dimensions, your_position, guard_position, distance) that gives an array of 2 integers of
the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2
integers of the guard's x and y coordinates in the room, and returns an integer of the number of distinct directions
that you can fire to hit the elite guard, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite guard are both positioned
on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim,
0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an
integer 1 < distance <= 10000.

For example, if you and the elite guard were positioned in a room with dimensions [3, 2], your_position [1, 1],
guard_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the
elite guard (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2],
and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1,
the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite guard with a
total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the
elite guard with a total shot distance of sqrt(5).

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9
"""
import math


def solution(dimensions, your_position, guard_position, distance):
    all_positions = {}

    furthest_plane_in_x = int(math.ceil(float(distance) / dimensions[0]))
    furthest_plane_in_y = int(math.ceil(float(distance) / dimensions[1]))

    all_dispositions = {
        (0, 0): [
            your_position,
            guard_position
        ],
        (1, 0): [
            [dimensions[0] - your_position[0], your_position[1]],
            [dimensions[0] - guard_position[0], guard_position[1]]
        ],
        (0, 1): [
            [your_position[0], dimensions[1] - your_position[1]],
            [guard_position[0], dimensions[1] - guard_position[1]]
        ],
        (1, 1): [
            [dimensions[0] - your_position[0], dimensions[1] - your_position[1]],
            [dimensions[0] - guard_position[0], dimensions[1] - guard_position[1]]
        ]
    }

    for x in range(-furthest_plane_in_x, furthest_plane_in_x + 1):
        for y in range(-furthest_plane_in_y, furthest_plane_in_y + 1):
            disposition_for_current_plane = all_dispositions[(x % 2, y % 2)]

            for (index, position) in enumerate(map(
                    lambda original_position: [original_position[0] + (x * dimensions[0]), original_position[1] + (y * dimensions[1])],
                    disposition_for_current_plane
            )):
                delta_x = your_position[0] - position[0]
                delta_y = your_position[1] - position[1]
                distance_from_player = math.sqrt(delta_x**2 + delta_y**2)
                if distance < distance_from_player:
                    shooting_angle = math.atan2(delta_y, delta_x)

                    if shooting_angle not in all_positions or all_positions[shooting_angle]['distance'] > distance_from_player:
                        all_positions[shooting_angle] = {
                            'is_player': not index,
                            'distance': distance_from_player
                        }

    return len(filter(lambda non_duplicate_position: not non_duplicate_position['is_player'], all_positions.values()))
