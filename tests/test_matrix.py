#!/usr/bin/env python3
# encoding: utf-8
import unittest

from sudokusolver.model.constraintmatrix import ConstraintMatrix
from sudokusolver.model.iterators import ColumnIterator
from sudokusolver.model.iterators import RowIterator
from sudokusolver.rules import get_all_candidates, get_all_satisfied_constraints

# logging.basicConfig(level=logging.DEBUG)
MAX_CANDIDATES = 729
MAX_CONSTRAINTS = 324


class ConstraintMatrixTest(unittest.TestCase):
    def setUp(self):
        self.m = ConstraintMatrix()

    def test_append(self):
        self.m.add('r1', ['c1', 'c2'])
        # iterator will iterate downwards through the rows
        nodes = [(node.candidate, node.covered_constraint)
                 for node in ColumnIterator(self.m.head_ref_node)]
        self.assertEqual(2, len(nodes))
        self.assertCountEqual([('_', '_'), ('r1', '_')],
                              nodes)

        nodes = [(node.candidate, node.covered_constraint)
                 for node in RowIterator(self.m.head_ref_node)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', '_'), ('_', 'c1'), ('_', 'c2')],
                              nodes)

    def test_linked_list_integrity(self):
        self.m.add('r1', ['c1', 'c2'])
        self.m.add('r2', ['c2'])
        self.__check_integrity()

    def test_cover_and_uncover(self):
        matrix = self.__create_matrix()
        candidate = matrix.head_ref_node.bottom

        matrix.cover(candidate)

        covered_constraints = get_all_satisfied_constraints(candidate.candidate)
        count_covered_constraints = len(covered_constraints)
        count_covered_candidates = 29

        count_candidates, count_constraints = self.__calc_size(matrix)
        self.assertEqual(MAX_CONSTRAINTS - count_covered_constraints,
                         count_constraints)
        self.assertEqual(MAX_CANDIDATES - count_covered_candidates,
                         count_candidates)

        matrix.uncover()

        count_candidates, count_constraints = self.__calc_size(matrix)
        self.__check_size(count_candidates, count_constraints)

    def test_matrix_full_size(self):
        matrix = self.__create_matrix()
        count_candidates, count_constraints = self.__calc_size(matrix)
        self.__check_size(count_candidates, count_constraints)

    def __create_matrix(self):
        matrix = ConstraintMatrix()
        for candidate in get_all_candidates():
            satisfied_constraints = get_all_satisfied_constraints(candidate)
            matrix.add(candidate, satisfied_constraints)
        return matrix

    def __check_integrity(self):
        # row checks
        nodes = [(node.candidate, node.covered_constraint)
                 for node in RowIterator(self.m.head_ref_node.bottom)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('r1', '_'), ('r1', 'c1'), ('r1', 'c2')],
                              nodes)
        nodes = [(node.candidate, node.covered_constraint)
                 for node in RowIterator(self.m.head_ref_node.bottom.bottom)]
        self.assertEqual(2, len(nodes))
        self.assertCountEqual([('r2', '_'), ('r2', 'c2')], nodes)
        # column checks
        nodes = [(node.candidate, node.covered_constraint)
                 for node in ColumnIterator(self.m.head_ref_node.right)]
        self.assertEqual(2, len(nodes))
        self.assertCountEqual([('_', 'c1'), ('r1', 'c1')],
                              nodes)
        nodes = [(node.candidate, node.covered_constraint)
                 for node in ColumnIterator(self.m.head_ref_node.right.right)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', 'c2'), ('r1', 'c2'), ('r2', 'c2')],
                              nodes)
        # try to iterate backwards on column headers
        # iterate through column headers
        nodes = [(node.candidate, node.covered_constraint)
                 for node in
                 RowIterator(self.m.head_ref_node.right.right, reversed=True)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', '_'), ('_', 'c1'), ('_', 'c2')], nodes)
        # iterate through c2 column
        nodes = [(node.candidate, node.covered_constraint)
                 for node in ColumnIterator(self.m.head_ref_node.right.right.bottom.bottom,
                                            reversed=True)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', 'c2'), ('r1', 'c2'), ('r2', 'c2')],
                              nodes)

    def __check_size(self, count_candidates, count_constraints):
        self.assertEqual(MAX_CONSTRAINTS, count_constraints)
        self.assertEqual(MAX_CANDIDATES, count_candidates)

    def __calc_size(self, matrix):
        count_constraints = sum([1 for n in RowIterator(matrix.head_ref_node)
                                 if n is not matrix.head_ref_node])
        count_candidates = sum([1 for n in ColumnIterator(matrix.head_ref_node)
                                if n is not matrix.head_ref_node])
        return count_candidates, count_constraints


if __name__ == '__main__':
    unittest.main()
