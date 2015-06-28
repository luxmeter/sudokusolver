from collections import defaultdict
import re

import rules


def visualize(candidates):
    candidates = [_map_to_coordinate(c) for c in candidates]
    candidate_map = defaultdict(dict)
    for r in range(0, 9):
        for c in range(0, 9):
            candidate_map[r][c] = 0

    for row, column, number in candidates:
        candidate_map[(row - 1)][(column - 1)] = number

    for row in candidate_map.keys():
        if row != 0 and row % 3 == 0:
            print('')
        numbers = [str(n) for n in candidate_map[row].values()]
        for i, number in enumerate(numbers):
            if i != 0 and i % 3 == 0:
                numbers[i] = ' |' + number
        print('|' + '|'.join(numbers) + '|')


def _get_row_map(candidates):
    row_map = defaultdict(list)
    for c in candidates:
        row_map[c[0]].append((c[1], c[2]))
    return row_map


def _map_to_coordinate(candidate):
    p = re.compile(r'R(\d)C(\d)#(\d)')
    m = p.match(candidate)
    row = int(m.group(1))
    column = int(m.group(2))
    number = int(m.group(3))
    return row, column, number


if __name__ == '__main__':
    visualize(rules.get_all_candidates())
