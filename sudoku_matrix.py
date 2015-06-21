#!/usr/bin/env python
# encoding: utf-8
import logging as logging

log = logging.getLogger(__name__)


class ConstraintMatrix(object):
    """Matrix to solve an exact cover problem.
    Each node knows his top, left, right and down neighbour"""
    def __init__(self):
        self._entry = Node('_', '_')
        self._column_head_by_constraint = {}
        self._row_head_by_candidate = {}

    def add(self, candidate=None, covered_constraints=[]):
        for constraint in covered_constraints:
            self.__append(candidate, constraint)

    def __append(self, candidate, covered_constraint):
        last_column_node = self.__get_last_column_node(covered_constraint)
        last_row_node = self.__get_last_row_node(candidate)

        if not last_column_node:
            last_column_node = Node('_', covered_constraint)
            if not self._entry.right:
                self._entry.right = last_column_node

        if not last_row_node:
            last_row_node = Node(candidate, '_')
            if not self._entry.down:
                self._entry.down = last_row_node

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

        node = Node(candidate, covered_constraint)
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
    def __init__(self, candidate, covered_constraint):
        self._top = None
        self._down = None
        self._left = None
        self._right = None
        self._candidate = candidate
        self._covered_constraint = covered_constraint

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
    def up(self):
        return self._up

    @up.setter
    def up(self, node):
        self._up = node

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


class ColumnIterator(object):
    def __init__(self, start):
        self._current = start

    def __iter__(self):
        return self

    def __next__(self):
        # in case the linked list is circular
        if self._current:
            current, self._current = \
                self._current, self._current.down
            return current
        else:
            raise StopIteration


class RowIterator(object):
    def __init__(self, start):
        self._current = start

    def __iter__(self):
        return self

    def __next__(self):
        # in case the linked list is circular
        if self._current:
            current, self._current = \
                self._current, self._current.right
            return current
        else:
            raise StopIteration