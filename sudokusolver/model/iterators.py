"""Provides iterators to iterate through
the nodes of the rows and columns of the ConstraintMatrix"""


class ColumnIterator(object):
    """Iterates through a sequence of vertically connected nodes."""
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        next_node = 'top' if self._reversed else 'bottom'
        while self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            yield current


class RowIterator(object):
    """Iterates through a sequence of horizontally connected nodes."""
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        next_node = 'left' if self._reversed else 'right'
        while self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            yield current
