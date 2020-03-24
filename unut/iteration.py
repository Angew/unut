import collections
import itertools


def sliding_window_iter(iterable, size):
    """Iterate through iterable using a sliding window of several elements.
    
    Creates an iterable where each element is a tuple of `size`
    consecutive elements from `iterable`, advancing by 1 element each
    time. For example:
    
    >>> list(sliding_window_iter([1, 2, 3, 4], 2))
    [(1, 2), (2, 3), (3, 4)]
    """
    iterable = iter(iterable)
    window = collections.deque(
        itertools.islice(iterable, size-1),
        maxlen=size
    )
    for item in iterable:
        window.append(item)
        yield tuple(window)
