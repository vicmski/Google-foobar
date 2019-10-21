"""
Oh no! You've managed to escape Commander Lambdas collapsing space station in an escape pod with the rescued bunny
prisoners - but Commander Lambda isnt about to let you get away that easily.
She's sent her elite fighter pilot squadron after you - and they've opened fire!

Fortunately, you know something important about the ships trying to shoot you down. Back when you were still
Commander Lambdas assistant, she asked you to help program the aiming mechanisms for the starfighters.
They undergo rigorous testing procedures, but you were still able to slip in a subtle bug.
The software works as a time step simulation: if it is tracking a target that is accelerating away at 45 degrees,
the software will consider the targets acceleration to be equal to the square root of 2, adding the calculated result
to the targets end velocity at each timestep. However, thanks to your bug, instead of storing the result with proper
precision, it will be truncated to an integer before adding the new velocity to your current position.
This means that instead of having your correct position, the targeting software will erringly report your
position as sum(i=1..n, floor(i*sqrt(2))) - not far enough off to fail Commander Lambdas testing, but enough that it
might just save your life.

If you can quickly calculate the target of the starfighters' laser beams to know how far off they'll be,
you can trick them into shooting an asteroid, releasing dust, and concealing the rest of your escape.
Write a function solution(str_n) which, given the string representation of an integer n,
returns the sum of (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string.
That is, for every number i in the range 1 to n, it adds up all of the integer portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".

str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be very large (up to 101 digits!),
using just sqrt(2) and a loop won't work. Sometimes, it's easier to take a step back and concentrate not on what you
have in front of you, but on what you don't.


"""

import math
import decimal

irrational_number = decimal.Decimal('1.41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157273')
complement = decimal.Decimal('3.41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157273501')


decimal.getcontext().prec = 100

def sumOfBeattySeq(current_irrational_number, n):
    if n > 0:
        if current_irrational_number > 2:
            return sumOfBeattySeq(irrational_number, n) + (n * (n + 1))
        else:
            m = long(decimal.Decimal(current_irrational_number - 1) * n)


            return (n + m) * (n + m + 1) / 2 - sumOfBeattySeq(complement, m)

    return 0


def solution(n):
    return str(long(sumOfBeattySeq(irrational_number, long(n))))
