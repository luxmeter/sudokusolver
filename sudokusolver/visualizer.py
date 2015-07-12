import re

from collections import defaultdict


def visualize(candidates):
    matrix = _map_by_label(candidates)
    for row in matrix.keys():
        if row != 0 and row % 3 == 0:
            print('')
        numbers = [str(n) for n in matrix[row].values()]
        for i, number in enumerate(numbers):
            if i != 0 and i % 3 == 0:
                numbers[i] = ' |' + number
        print('|' + '|'.join(numbers) + '|')


def _map_by_label(candidates):
    matrix = defaultdict(dict)
    for candidate in candidates:
        pattern = re.compile(r'R(\d)C(\d)#(\d)')
        matches = pattern.match(candidate)
        row = int(matches.group(1))
        column = int(matches.group(2))
        number = int(matches.group(3))
        matrix[(row - 1)][(column - 1)] = number
    return matrix
