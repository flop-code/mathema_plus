from math import isqrt


def is_square(n: float) -> bool:
    if not n.is_integer():
        return False
    
    i = abs(int(n))
    k = isqrt(i)
    return i == k * k
