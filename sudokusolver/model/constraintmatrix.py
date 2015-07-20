from collections import defaultdict
from operator import attrgetter
from .node import Node
from .node import ColumnIterator
from .node import RowIterator
from .node import ColumnReferenceNode
from .node import RowReferenceNode
from .node import MatrixHeadReferenceNode


class ConstraintMatrix(object):
    """
    A two dimensional matrix used to solve an exact cover problem.
    The constraints are mapped by the columns and the candidates by the rows.
    Each node in the matrix knows its top, left, bottom and right neighbour.
    A node exists only in case the candidate of the row fulfills the constraint of the column.

    Special nodes, so called ReferenceNodes, point to the first node of a row or a column
    and are used to itereate through their nodes.
    Those ReferenceNodes can be accessed through the MatrixHeadReferenceNode
    which points on its right to the first ColumnReferenceNode
    and on its bottom to the first RowRefereneNode of the matrix.

    Some methods expect candidates and constraint names.
    Those are simple strings obeying following format pattern:

    * candidate: ``R{rowNumber}C{columnNumber}#{number}``
    * constraints: 
        * ``R{rowNumber}#{number}``,
        * ``C{columnNumber}#{number}``,
        * ``B{blockNumber}#{number}``,
        * ``R{rowNumber}C{columnNumber}``
    """
    def __init__(self):
        self.__history = []
        self.__entry = MatrixHeadReferenceNode()
        # accessible by candidate and constraint
        self.__col_ref_nodes = defaultdict(None)
        self.__row_ref_nodes = defaultdict(None)
        self.__covered_constraint = []

    def add(self, candidate=None, covered_constraints=[]):
        """
        creates and adds a new node to the matrix labeled with
        the provided candidate and constraints.

        Args:
            candidate (str): candidate name to be attached to the Node
            covered_constraints (list): constraint names to be attached to the Node
        """
        for constraint in covered_constraints:
            self.__append(candidate, constraint)

    def __get_unsatisfied_constraint_column(self):
        constraints = [column_ref_node
                       for column_ref_node in self.__entry.get_column_ref_node_iterator()]
        return min(constraints, key=attrgetter('size'))

    def has_satisfied_all_constraints(self) -> bool:
        """Returns True of all contraints has been satisfied, otherwise False"""
        return self.__entry.right is None

    def candidates_exist(self) -> bool:
        """Returs True if any candidate is left, otherwise False"""
        return self.__entry.bottom is not None

    def get_next_constraints_candidates(self) -> list:
        """
        Returns a sequence of RowReferenceNodes(candidates) fulfilling
        the next automatically chosen ColumnReferenceNode(constraint)

        Returns:
            list of RowReferenceNodes
        """
        constraint = self.__get_unsatisfied_constraint_column()
        candidates = [node.row_ref_node for node in constraint]
        return candidates

    def cover(self, row_ref_node):
        """Covers the candidate itself and all satisfiying constraints
        as well as the other candidates that would satisfy those.

        Removes complete rows and columns according the Algorithm-X::

            For each column j such that Ar, j = 1
              for each row i such that Ai, j = 1
                  delete row i from matrix A
              delete column j from matrix A

        Use uncover to undo the changes made by this operation.
        """
        # provides all constraints the provided candidate is satisfying
        column_ref_nodes = self.__get_covered_columns(row_ref_node)

        # provides all candidates that satisfy the same constraints
        row_ref_nodes = self.__get_covered_rows(column_ref_nodes)

        # disconnects also reference nodes from their neighbours
        removed_row_nodes = self.__cover_rows(row_ref_nodes)  # remove columns
        removed_column_nodes = self.__cover_columns(column_ref_nodes)

        self.__history.append((column_ref_nodes, removed_row_nodes, removed_column_nodes))
        self.__covered_constraint = self.__covered_constraint + column_ref_nodes
        return row_ref_nodes, column_ref_nodes

    def uncover(self):
        """Reverts all changes done by cover operation"""
        column_ref_nodes, removed_row_nodes, removed_column_nodes = self.__history.pop()

        self.__uncover_columns(removed_column_nodes)
        self.__uncover_rows(removed_row_nodes)

        self.__covered_constraint = \
            [c for c in self.__covered_constraint
             if c not in column_ref_nodes]

        return removed_row_nodes, removed_column_nodes

    @property
    def head_ref_node(self) -> MatrixHeadReferenceNode:
        """Returns the MatrixHeadReferenceNode.
        Can be used to iterate through the RowReferenceNodes and ColumnReferenceNodes"""
        return self.__entry

    @staticmethod
    def __cover_columns(column_ref_nodes):
        removed_column_nodes = []
        for ref_node in column_ref_nodes:
            for node in ColumnIterator(ref_node):
                Node.disconnect(node, how='vertically')
                removed_column_nodes.append(node)

        return removed_column_nodes

    def __cover_rows(self, row_ref_nodes):
        removed_row_nodes = []
        for ref_node in row_ref_nodes:
            for node in RowIterator(ref_node):
                Node.disconnect(node, how='horizontally')
                removed_row_nodes.append(node)
                self.__col_ref_nodes[node.candidate].size -= 1

        return removed_row_nodes

    def __uncover_rows(self, removed_row_nodes):
        if removed_row_nodes:
            for node in removed_row_nodes:
                Node.connect(node.top, node, how='vertically')
                Node.connect(node, node.bottom, how='vertically')
                self.__col_ref_nodes[node.candidate].size += 1

    @staticmethod
    def __uncover_columns(removed_column_nodes):
        if removed_column_nodes:
            for node in removed_column_nodes:
                Node.connect(node.left, node, how='horizontally')
                Node.connect(node, node.right, how='horizontally')

    def __get_next_constraint(self):
        for c in self.__entry.get_column_ref_node_iterator():
            if c not in self.__covered_constraint:
                return c
        return None

    @staticmethod
    def __get_covered_rows(column_ref_nodes):
        seen = []
        for column_ref_node in column_ref_nodes:
            for node in column_ref_node:
                if node.row_ref_node not in seen:
                    seen.append(node.row_ref_node)
        return seen

    @staticmethod
    def __get_covered_columns(row_ref_node):
        return [node.column_ref_node for node in row_ref_node]

    def __append(self, candidate, covered_constraint):
        col_ref_node = self.__col_ref_nodes.get(covered_constraint)
        row_ref_node = self.__row_ref_nodes.get(candidate)

        last_column_node = ColumnReferenceNode(covered_constraint) \
            if not col_ref_node else col_ref_node.get_last_node()

        last_row_node = RowReferenceNode(candidate) \
            if not row_ref_node else row_ref_node.get_last_node()

        # add node to the column_map if not defined yet
        if not col_ref_node:
            self.__col_ref_nodes[covered_constraint] = last_column_node
            last = self.__entry.get_last_column_ref_node()
            if last is not last_column_node:
                Node.connect(last, last_column_node, how='horizontally')

        # add node to the row_map if not defined yet
        if not row_ref_node:
            self.__row_ref_nodes[candidate] = last_row_node
            last = self.__entry.get_last_row_ref_node()
            if last is not last_row_node:
                Node.connect(last, last_row_node, how='vertically')

        node = Node(candidate, covered_constraint,
                    self.__row_ref_nodes[candidate],
                    self.__col_ref_nodes[covered_constraint])
        Node.connect(last_column_node, node, how='vertically')
        Node.connect(last_row_node, node, how='horizontally')
        self.__col_ref_nodes[node.candidate] = node.column_ref_node

        if node.column_ref_node:
            node.column_ref_node.size += 1
