#!/usr/bin/env python
# encoding: utf-8

class ConstraintMatrix(object):
    """Matrix to solve an exact cover problem.
    Each node knows his top, left, right and bottom neighbour"""

    def __init__(self):
        self._history = []
        self._entry = Node('_', '_')
        self._column_head_by_constraint = {}
        self._row_head_by_candidate = {}
        self._covered_constraints = []

    def add(self, candidate=None, covered_constraints=[]):
        for constraint in covered_constraints:
            self.__append(candidate, constraint)

    def get_unsatisfied_constraint_column(self):
        return self._entry.right

    def has_satisfied_all_constraints(self):
        return self._entry.right is None

    def exists_candidates(self):
        return self._entry.down is not None

    def get_next_candidate(self):
        constraint = self.__get_next_constraint()
        if constraint:
            for node in ColumnIterator(constraint.down):
                yield node.row_head

    def cover(self, row_head):
        # For each column j such that Ar, j = 1,
        #   for each row i such that Ai, j = 1,
        #       delete row i from matrix A;
        #   delete column j from matrix A.

        # provides all constraints the provided candidate is satisfying
        column_heads = self.__get_covered_columns(row_head)

        # provides all candidates that satisfy the same constraints
        row_heads = self.__get_covered_rows(column_heads)

        removed_row_nodes = self.__cover_rows(row_heads)# remove columns
        removed_column_nodes = self.__cover_columns(column_heads)

        self._history.append((row_head, column_heads, removed_row_nodes, removed_column_nodes))
        self._covered_constraints = self._covered_constraints + column_heads
        return row_heads, column_heads

    def uncover(self):
        row_head, column_heads, removed_row_nodes, removed_column_nodes = self._history.pop()
        self.__uncover_columns(removed_column_nodes)
        self.__uncover_rows(removed_row_nodes)

        self._covered_constraints = \
            [c for c in self._covered_constraints
             if c not in column_heads]

        return removed_row_nodes, removed_column_nodes

    @property
    def entry(self):
        return self._entry

    def __cover_columns(self, column_heads):
        removed_column_nodes = []
        for head in column_heads:
            for node in ColumnIterator(head):
                if node.left:
                    node.left.right = node.right
                if node.right:
                    node.right.left = node.left
                removed_column_nodes.append(node)
        return removed_column_nodes

    def __cover_rows(self, row_heads):
        removed_row_nodes = []
        for head in row_heads:
            for node in RowIterator(head):
                if node.top:
                    node.top.down = node.down
                if node.down:
                    node.down.top = node.top
                removed_row_nodes.append(node)
                if node.column_head:
                    node.column_head.size -= 1
        return removed_row_nodes

    def __uncover_rows(self, removed_row_nodes):
        if removed_row_nodes:
            for node in removed_row_nodes:
                if node.top:
                    node.top.down = node
                if node.down:
                    node.down.top = node
                if node.column_head:
                    node.column_head.size += 1

    def __uncover_columns(self, removed_column_nodes):
        if removed_column_nodes:
            for node in removed_column_nodes:
                if node.left:
                    node.left.right = node
                if node.right:
                    node.right.left = node

    def __get_next_constraint(self):
        for c in RowIterator(self._entry.right):
            if c not in self._covered_constraints:
                return c
        return None

    def __get_covered_rows(self, column_heads):
        seen = []
        for column_head in column_heads:
            for node in ColumnIterator(column_head):
                if node.row_head and \
                                node.row_head not in seen:
                    seen.append(node.row_head)
        return seen

    def __get_covered_columns(self, row):
        return [node.column_head for node in RowIterator(row)
                if node.column_head]

    def __append(self, candidate, covered_constraint):
        last_column_node = self.__get_last_column_node(covered_constraint)
        last_row_node = self.__get_last_row_node(candidate)

        if not last_column_node:
            last_column_node = ColumnHeader('_', covered_constraint)
            if not self._entry.right:
                self._entry.right = last_column_node
                last_column_node.left = self._entry

        if not last_row_node:
            last_row_node = Node(candidate, '_')
            if not self._entry.down:
                self._entry.down = last_row_node
                last_row_node.top = self._entry

        # add node to the column_map if not defined yet
        if not self._column_head_by_constraint.get(covered_constraint):
            self._column_head_by_constraint[covered_constraint] = last_column_node
            last = self.__get_last_row_node(None, head=self._entry)
            if last is not last_column_node:
                self.__append_row_nodes(last, last_column_node)

        # add node to the row_map if not defined yet
        if not self._row_head_by_candidate.get(candidate):
            self._row_head_by_candidate[candidate] = last_row_node
            last = self.__get_last_column_node(None, head=self._entry)
            if last is not last_row_node:
                self.__append_column_nodes(last, last_row_node)

        node = Node(candidate, covered_constraint,
                    self._row_head_by_candidate[candidate],
                    self._column_head_by_constraint[covered_constraint])
        self.__append_column_nodes(last_column_node, node)
        self.__append_row_nodes(last_row_node, node)
        if node.column_head:
            node.column_head.size += 1

    def __append_row_nodes(self, last_row_node, node):
        last_row_node.right = node
        node.left = last_row_node

    def __append_column_nodes(self, last_column_node, node):
        last_column_node.down = node
        node.top = last_column_node

    def __get_last_row_node(self, candidate, head=None):
        current = self._row_head_by_candidate.get(candidate) \
            if not head else head
        if current:
            while current.right:
                current = current.right
            return current

        return None

    def __get_last_column_node(self, covered_constraint, head=None):
        current = self._column_head_by_constraint.get(covered_constraint) \
            if not head else head
        if current:
            while current.down:
                current = current.down
            return current

        return None


class Node(object):
    def __init__(self, candidate, covered_constraint,
                 row_head=None, column_head=None):
        self._top = None
        self._down = None
        self._left = None
        self._right = None
        self._candidate = candidate
        self._covered_constraint = covered_constraint
        self._row_head = row_head
        self._column_head = column_head

    @property
    def row_head(self):
        return self._row_head

    @property
    def column_head(self):
        return self._column_head

    @property
    def covered_constraint(self):
        return self._covered_constraint

    @covered_constraint.setter
    def covered_constraint(self, covered_constraint):
        self._covered_constraint = covered_constraint

    @property
    def candidate(self):
        return self._candidate

    @candidate.setter
    def candidate(self, candidate):
        self._candidate = candidate

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, node):
        self._top = node

    @property
    def down(self):
        return self._down

    @down.setter
    def down(self, node):
        self._down = node

    def __repr__(self):
        return "Node('{}', '{}')".format(self._candidate,
                                         self._covered_constraint)

    def __str__(self):
        return "Node('{}', '{}')".format(self._candidate,
                                         self._covered_constraint)

    def __hash__(self):
        return hash((self._candidate, self._covered_constraint))

    def __eq__(self, other):
        return (self._candidate, self._covered_constraint) == \
               (other._candidate, other._covered_constraint)

class ColumnHeader(Node):
    def __init__(self, candidate, covered_constraint,
                 row_head=None, column_head=None):
        super().__init__(candidate, covered_constraint,
                         row_head, column_head)
        self._size = 0

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size


class ColumnIterator(object):
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        return self

    def __next__(self):
        next_node = '_top' if self._reversed else '_down'
        if self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            return current
        else:
            raise StopIteration


class RowIterator(object):
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        return self

    def __next__(self):
        next_node = '_left' if self._reversed else '_right'
        if self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            return current
        else:
            raise StopIteration
