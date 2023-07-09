import hashlib
import os
from collections.abc import Callable, Iterable
from typing import Any, Optional
import random
import string


def human_num(num):
    """Converts a number to a human-readable string.
    Adapted from: https://stackoverflow.com/a/45846841
    Distributed under: CC BY-SA 3.0"""
    if num == 1:
        return 'operation'
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def round_elements(
        iterable: Iterable,
        round_to: int = 2,
        reduce: Callable[[Iterable], Any] | None = None,
) -> Iterable:
    """Takes any iterable of arbitrary elements and rounds all floating point numbers.

    By default, the return value is a list, but this can be changed by passing a different reduce function.
    If the reduce function is None, the return value is a list.

    Args:
        :param iterable: the iterable to round
        :param round_to: the number of decimal places to round to (default: 2)
        :param reduce: the reduce function to use to reduce the map object (default: list)
    """
    rounded = map(lambda elem: round(elem, round_to) if isinstance(elem, float) else elem, iterable)
    if reduce is None:
        return list(rounded)
    return reduce(rounded)


def generate_random_string(n: int) -> str:
    """Generates a random string of n uppercase letters and numbers.

    Args:
        n: The length of the string to generate.

    Returns:
        A random string of n letters and numbers.
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(n))


def strip_whitespace(s: str) -> str:
    """Takes a string and removes double spaces, tabs, and newlines."""
    return ' '.join(s.split())


def md5_hash(s: str) -> str:
    """Returns the md5 hash of a string."""
    return hashlib.md5(s.encode()).hexdigest()


def user_path(s: str) -> str | None:
    """Returns the path with user home directory expanded."""
    if s is None:
        return None
    if s.startswith('~'):
        return os.path.expanduser(s)
    return s


# if __name__ == '__main__':
#     test_str = "\nSELECT\n    entry.entryId\nFROM\n    entry\nWHERE (\n    1=1\n)\n"
#     print(strip_whitespace(test_str))

