#!/usr/bin/env python
# encoding: utf-8
from collections import namedtuple
import logging as logging

log = logging.getLogger(__name__)


class ConstraintMatrix(object):
    """Matrix to solve an exact cover problem.
    Each node knows his top, left, right and bottom neighbour"""
    def __init__(self):
        self._history = {}
        self._entry = Node('_', '_')
        self._column_head_by_constraint = {}
        self._row_head_by_candidate = {}

    def add(self, candidate=None, covered_constraints=[]):
        for constraint in covered_constraints:
            self.__append(candidate, constraint)

    def get_unsatisfied_constraint_column(self):
        return self._entry.right

    def has_satisfied_all_constraints(self):
        return self._entry.right is None

    def cover(self, row_head):
        # For each column j such that Ar, j = 1,
        #   for each row i such that Ai, j = 1,
        #       delete row i from matrix A;
        #   delete column j from matrix A.

        # provides all constraints the provided candidate is satisfying
        column_heads = self.__get_covered_columns(row_head)

        # provides all candidates that satisfy the same constraints
        row_heads = self.__get_covered_rows(column_heads)

        # remove rows
        removed_row_nodes = []
        for head in row_heads:
            for node in RowIterator(head):
                if node.top:
                    node.top.down = node.down
                if node.down:
                    node.down.top = node.top
                removed_row_nodes.append(node)

        # remove columns
        removed_column_nodes = []
        for head in column_heads:
            for node in ColumnIterator(head):
                if node.left:
                    node.left.right = node.right
                if node.right:
                    node.right.left = node.left
                removed_column_nodes.append(node)

        self._history[row_head] = (removed_row_nodes, removed_column_nodes)

    def uncover(self, row_head):
        removed_row_nodes, removed_column_nodes = self._history[row_head]

        if removed_column_nodes:
            for node in removed_column_nodes:
                if node.left:
                    node.left.right = node
                if node.right:
                    node.right.left = node

        if removed_row_nodes:
            for node in removed_row_nodes:
                if node.top:
                    node.top.down = node
                if node.down:
                    node.down.top = node

        self._history.pop(row_head)

    def __get_covered_rows(self, column_heads):
        return set(node.row_head
                   for column_head in column_heads
                   for node in ColumnIterator(column_head)
                   if node.row_head)

    def __get_covered_columns(self, row):
        return set(node.column_head for node in RowIterator(row)
                   if node.column_head)

    def __append(self, candidate, covered_constraint):
        last_column_node = self.__get_last_column_node(covered_constraint)
        last_row_node = self.__get_last_row_node(candidate)

        if not last_column_node:
            last_column_node = Node('_', covered_constraint)
            if not self._entry.right:
                self._entry.right = last_column_node
                last_column_node.left = self._entry

        if not last_row_node:
            last_row_node = Node(candidate, '_')
            if not self._entry.down:
                self._entry.down = last_row_node
                last_row_node.top = self.entry

        # add node to the column_map if not defined yet
        if not  self._column_head_by_constraint.get(covered_constraint):
            self._column_head_by_constraint[covered_constraint] = last_column_node
            last = self.__get_last_row_node(None, head=self._entry)
            if last is not last_column_node:
                self.__append_row_nodes(last, last_column_node)

        # add node to the row_map if not defined yet
        if not  self._row_head_by_candidate.get(candidate):
            self._row_head_by_candidate[candidate] = last_row_node
            last = self.__get_last_column_node(None, head=self._entry)
            if last is not last_row_node:
                self.__append_column_nodes(last, last_row_node)

        node = Node(candidate, covered_constraint,
                    self._row_head_by_candidate[candidate],
                    self._column_head_by_constraint[covered_constraint])
        self.__append_column_nodes(last_column_node, node)
        self.__append_row_nodes(last_row_node, node)

    def __append_row_nodes(self, last_row_node, node):
        log.debug('setting %s as next row node from %s',
                  node, last_row_node)
        last_row_node.right = node
        node.left = last_row_node

    def __append_column_nodes(self, last_column_node, node):
        log.debug('setting %s as next column node from %s',
                  node, last_column_node)
        last_column_node.down = node
        node.top = last_column_node

    def __get_last_row_node(self, candidate, head=None):
        current = self._row_head_by_candidate.get(candidate)\
            if not head else head
        if current:
            while current.right:
                current = current.right
            return current

        return None

    def __get_last_column_node(self, covered_constraint, head=None):
        current = self._column_head_by_constraint.get(covered_constraint)\
            if not head else head
        if current:
            while current.down:
                current = current.down
            return current

        return None

    @property
    def entry(self):
        return self._entry


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
        return "Node('{}', '{}')".format(self._candidate, self._covered_constraint)

    def __str__(self):
        return repr(self)
    
    def __hash__(self):
        return hash((self._candidate, self._covered_constraint))

    def __eq__(self, other):
        return (self._candidate, self._covered_constraint) == (other._candidate, other._covered_constraint)


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