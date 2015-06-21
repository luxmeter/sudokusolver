#!/usr/bin/env python
# encoding: utf-8
import unittest
from sudoku_matrix import ConstraintMatrix
from sudoku_matrix import ColumnIterator
from sudoku_matrix import RowIterator

# logging.basicConfig(level=logging.DEBUG)

class ConstraintMatrixTest(unittest.TestCase):
    def setUp(self):
        self.m = ConstraintMatrix()

    def test_append(self):
        self.m.add('r1', ['c1', 'c2'])
        # iterator will iterate downwards through the rows
        nodes = [(node.candidate, node._covered_constraint)
                     for node in ColumnIterator(self.m.entry)]
        self.assertEqual(2, len(nodes))
        self.assertCountEqual([('_', '_'), ('r1', '_')],
                              nodes)

        nodes = [(node.candidate, node._covered_constraint)
                     for node in RowIterator(self.m.entry)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', '_'), ('_', 'c1'), ('_', 'c2')],
                              nodes)

    def test_linked_list_integrity(self):
        self.__setup_matrix()
        self.__check_integrity()

    def __check_integrity(self):
        # row checks
        nodes = [(node.candidate, node._covered_constraint)
                 for node in RowIterator(self.m.entry.down)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('r1', '_'), ('r1', 'c1'), ('r1', 'c2')],
                              nodes)
        nodes = [(node.candidate, node._covered_constraint)
                 for node in RowIterator(self.m.entry.down.down)]
        self.assertEqual(2, len(nodes))
        self.assertCountEqual([('r2', '_'), ('r2', 'c2')], nodes)
        # column checks
        nodes = [(node.candidate, node._covered_constraint)
                 for node in ColumnIterator(self.m.entry.right)]
        self.assertEqual(2, len(nodes))
        self.assertCountEqual([('_', 'c1'), ('r1', 'c1')],
                              nodes)
        nodes = [(node.candidate, node._covered_constraint)
                 for node in ColumnIterator(self.m.entry.right.right)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', 'c2'), ('r1', 'c2'), ('r2', 'c2')],
                              nodes)
        # try to iterate backwards on column headers
        # iterate through column headers
        nodes = [(node.candidate, node._covered_constraint)
                 for node in RowIterator(self.m.entry.right.right, reversed=True)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', '_'), ('_', 'c1'), ('_', 'c2')], nodes)
        # iterate through c2 column
        nodes = [(node.candidate, node._covered_constraint)
                 for node in ColumnIterator(self.m.entry.right.right.down.down, reversed=True)]
        self.assertEqual(3, len(nodes))
        self.assertCountEqual([('_', 'c2'), ('r1', 'c2'), ('r2', 'c2')],
                              nodes)

    def test_constraint_covering(self):
        self.__setup_matrix()

        column_head = self.m.get_unsatisfied_constraint_column()
        self.assertIsNotNone(column_head)
        self.assertFalse(self.m.has_satisfied_all_constraints())

        self.m.cover(column_head.down.row_head)
        self.assertIsNone(self.m.get_unsatisfied_constraint_column())
        self.assertTrue(self.m.has_satisfied_all_constraints())


    def test_constraint_covering(self):
        self.__setup_matrix()

        row_head = self.m.get_unsatisfied_constraint_column().down.row_head
        self.m.cover(row_head)
        self.assertIsNone(self.m.get_unsatisfied_constraint_column())
        self.assertTrue(self.m.has_satisfied_all_constraints())
        self.assertIsNone(self.m.entry.down)

        self.m.uncover(row_head)
        self.assertIsNotNone(self.m.get_unsatisfied_constraint_column())
        self.assertFalse(self.m.has_satisfied_all_constraints())
        self.assertIsNotNone(self.m.entry.down)
        self.__check_integrity()

    def __setup_matrix(self):
        self.m.add('r1', ['c1', 'c2'])
        self.m.add('r2', ['c2'])


if __name__ == '__main__':
    unittest.main()