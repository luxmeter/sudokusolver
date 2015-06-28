from collections import defaultdict
import re

import rules


def visualize(candidates):
    candidates = [_map_to_coordinate(c) for c in candidates]
    candidates = sorted(candidates)
    row_map = _get_row_map(candidates)
    for row, fields in row_map.items():
        sum_fields = []
        max_range = len(fields) if len(fields) >= 9 else 9
        for c in range(0, max_range):
            f = fields[c] if c < len(fields) else None
            if f:
                sum_fields.append('%s' % f[1])
            else:
                sum_fields.append('%s' % (c, '_'))
        print('R#%s: %s' % (row, sum_fields))


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
