from itertools import chain
from collections import defaultdict


# there is only one number in one cell
def _get_row_column_constraints():
    for row in range(1, 10):
        for column in range(1, 10):
            yield 'R{}C{}'.format(row, column)


def _get_row_number_constraints():
    for row in range(1, 10):
        for number in range(1, 10):
            yield 'R{}#{}'.format(row, number)


def _get_column_number_constraints():
    for column in range(1, 10):
        for number in range(1, 10):
            yield 'C{}#{}'.format(column, number)


def _get_block_number_constraints():
    for block in range(1, 10):
        for number in range(1, 10):
            yield 'B{}#{}'.format(block, number)


def _get_satisfied_row_column_constraint(candidate):
    return candidate[0:-2]


def _get_satisfied_row_number_constraint(candidate):
    return ''.join((candidate[0:2], candidate[4:]))


def _get_satisfied_column_number_constraint(candidate):
    return ''.join((candidate[2:4], candidate[4:]))


def _get_satisfied_block_number_constraint(candidate):
    row_index = int(candidate[1:2]) - 1
    column_index = int(candidate[3:4]) - 1
    block_index = (3 * (row_index // 3)) + (column_index // 3)
    block = block_index + 1
    return 'B{}#{}'.format(block, candidate[5:])


def _get_satisfying_values(predicate, constraint=None):
    satisfied_constraints = defaultdict(list)
    for value in get_all_candidates():
        satisfied_constraint = predicate(value)
        if satisfied_constraint:
            satisfied_constraints[satisfied_constraint].append(value)
    if constraint:
        return satisfied_constraints[constraint]
    return satisfied_constraints


def get_all_candidates():
    for row in range(1, 10):
        for column in range(1, 10):
            for number in range(1, 10):
                yield 'R{}C{}#{}'.format(row, column, number)


def get_all_satisfied_constraints(*candidates):
    res = []
    for p in candidates:
        res += [_get_satisfied_row_column_constraint(p),
                _get_satisfied_row_number_constraint(p),
                _get_satisfied_column_number_constraint(p),
                _get_satisfied_block_number_constraint(p)]
    return res


def get_all_constraints():
    return chain(_get_row_column_constraints(), _get_row_number_constraints(),
        _get_column_number_constraints(), _get_block_number_constraints())