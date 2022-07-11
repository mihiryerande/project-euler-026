# Problem 26:
#     Reciprocal Cycles
#
# Description:
#     A unit fraction contains 1 in the numerator.
#     The decimal representation of the unit fractions with denominators 2 to 10 are given:
#         1/2   =   0.5
#         1/3   =   0.(3)
#         1/4   =   0.25
#         1/5   =   0.2
#         1/6   =   0.1(6)
#         1/7   =   0.(142857)
#         1/8   =   0.125
#         1/9   =   0.(1)
#         1/10  =   0.1
#     Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle.
#     It can be seen that 1/7 has a 6-digit recurring cycle.
#
#     Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

from typing import Tuple


# Idea:
#     First consider the representation of a recurring fraction in decimal.
#     Suppose we have a number cycle `c` repeating in the span of `w` digits after the decimal point.
#     This would look like S = 0.(0...c)*, with zeros padded in front of `c` if len(c) < w.
#
#     Looking at this as an infinite geometric series, and manipulating:
#           S = 0.(0...c)*
#         = (1/10^w) * (Sum(c * 10^(-w*i)) for i in [0, inf])   # Formulating recurring part as a summation
#         = (1/10^w) * (c / (1 - 10^(-w))                       # Substitute in formula for geometric series
#         = c / (10^w * (1 - 10^(-w))                           # Combine fractions
#         = c / (10^w - 1)                                      # Simplify
#
#     Thus any recurring fraction `S` can be written as c/(10^w-1) for some `c` and `w`.
#     Note that the denominator is 99...9, with 9 appearing `w` times.
#     For example, 0.(12345)* = 12345/99999
#
# Extension:
#     The recurring representation can be extended to accommodate fixed prefixes.
#     For example, we might have 0.7(12345)*, so there is a prefix of '7'.
#     We can decompose this with the following:
#       S = 0.7(12345)*
#         = 0.7 + (1/10) * 0.(12345)*
#         = 7/10 + (1/10) * S'
#         = (S'+7)/10
#
#     Here, we know S' is a recurring decimal number, and can be represented as a fraction.
#     S is thus another fraction.

def main(n: int) -> Tuple[int, int]:
    """
    Returns the number `d` (< `n`) for which 1/d contains the
      longest recurring cycle in its decimal fraction part.

    Args:
        n (int): Natural number, greater than 2

    Returns:
        (Tuple[int, int]):
            Tuple of ...
              * `d` (< 'n') for which 1/d has the longest recurring cycle in its decimal fraction part
              * Length of cycle associated with 1/`d`

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 2

    d_best = None
    d_cycle = 0

    for d_orig in range(2, n):
        # Check if some power of 10 would be divisible by d
        d = d_orig
        count_2s = 0
        while d % 2 == 0:
            d //= 2
            count_2s += 1
        count_5s = 0
        while d % 5 == 0:
            d //= 5
            count_5s += 1

        if d != 1:
            if count_2s == 0 and count_5s == 0:
                # 'd_orig' not reducible by 2 or 5, so determine its cycle length
                # Since d and 10 are relatively prime, using some modular math,
                #   there exists some `w`, where 0 < w <= d,
                #   such that 10^w = 1 (mod d)
                #
                # Once we know this `w`, then (10^w - 1) = 0 (mod d), i.e. (10^w-1) is divisible by d.
                # Let c*d = 10^w - 1.
                # Then 1/d = c / (c*d) = c / (10^w-1)
                #
                # From the reasoning above (in 'Idea' section),
                #   this means 1/d turns out to have a recurring decimal cycle of length `w`.
                w = 1
                p = 10 % d
                while p != 1:
                    p = (10*p) % d
                    w += 1

                if w > d_cycle:
                    d_best = d
                    d_cycle = w
            else:
                # `d_orig` reduced to `d`, so would have same cycle length as `d` => Ignore `d_orig`
                continue
        else:
            # 10^max(count_2s,count5s) is divisible by `d_orig` => No cycle
            continue
    return d_best, d_cycle


if __name__ == '__main__':
    num = int(input('Enter a natural number (greater than 2): '))
    denominator, cycle_length = main(num)
    print('Denominator d (≤ {}) having longest recurring decimal cycle:'.format(num))
    print('  d = {} has cycle length of {}'.format(denominator, cycle_length))
