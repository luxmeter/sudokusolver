"""
Module containing data structures to model an exact cover problem.
"""
from operator import attrgetter


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
    """
    def __init__(self):
        self.__history = []
        self.__entry = Node('_', '_')
        self.__column_head_by_constraint = {}
        self.__column_head_by_candidate = {}
        self.__row_head_by_candidate = {}
        self.__covered_constraint = []

    def add(self, candidate=None, covered_constraints=[]):
        for constraint in covered_constraints:
            self.__append(candidate, constraint)

    def __get_unsatisfied_constraint_column(self):
        constraints = [column_head
                       for column_head in RowIterator(self.__entry.right)]
        return min(constraints, key=attrgetter('size'))

    def has_satisfied_all_constraints(self):
        return self.__entry.right is None

    def candidates_exist(self):
        return self.__entry.down is not None

    def get_next_constraints_candidates(self):
        constraint = self.__get_unsatisfied_constraint_column()
        candidates = [node.row_head
                      for node in ColumnIterator(constraint.down)]
        return candidates

    def cover(self, row_head):
        # For each column j such that Ar, j = 1,
        #   for each row i such that Ai, j = 1,
        #       delete row i from matrix A;
        #   delete column j from matrix A.

        # provides all constraints the provided candidate is satisfying
        column_heads = self.__get_covered_columns(row_head)

        # provides all candidates that satisfy the same constraints
        row_heads = self.__get_covered_rows(column_heads)

        removed_row_nodes = self.__cover_rows(row_heads)  # remove columns
        removed_column_nodes = self.__cover_columns(column_heads)

        self.__history.append((column_heads, removed_row_nodes, removed_column_nodes))
        self.__covered_constraint = self.__covered_constraint + column_heads
        return row_heads, column_heads

    def uncover(self):
        column_heads, removed_row_nodes, removed_column_nodes = self.__history.pop()

        self.__uncover_columns(removed_column_nodes)
        self.__uncover_rows(removed_row_nodes)

        self.__covered_constraint = \
            [c for c in self.__covered_constraint
             if c not in column_heads]

        return removed_row_nodes, removed_column_nodes

    @property
    def entry(self):
        return self.__entry

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
                self.__column_head_by_candidate[node.candidate].size -= 1

        return removed_row_nodes

    def __uncover_rows(self, removed_row_nodes):
        if removed_row_nodes:
            for node in removed_row_nodes:
                if node.top:
                    node.top.down = node
                if node.down:
                    node.down.top = node
                self.__column_head_by_candidate[node.candidate].size += 1

    def __uncover_columns(self, removed_column_nodes):
        if removed_column_nodes:
            for node in removed_column_nodes:
                if node.left:
                    node.left.right = node
                if node.right:
                    node.right.left = node

    def __get_next_constraint(self):
        for c in RowIterator(self.__entry.right):
            if c not in self.__covered_constraint:
                return c
        return None

    def __get_covered_rows(self, column_heads):
        seen = []
        for column_head in column_heads:
            for node in ColumnIterator(column_head):
                if node.row_head and node.row_head not in seen:
                    seen.append(node.row_head)
        return seen

    def __get_covered_columns(self, row):
        return [node.column_head for node in RowIterator(row)
                if node.column_head]

    def __append(self, candidate, covered_constraint):
        last_column_node = self.__get_last_column_node(covered_constraint)
        last_row_node = self.__get_last_row_node(candidate)

        if not last_column_node:
            last_column_node = Header('_', covered_constraint)
            if not self.__entry.right:
                self.__entry.right = last_column_node
                last_column_node.left = self.__entry

        if not last_row_node:
            last_row_node = Header(candidate, '_')
            if not self.__entry.down:
                self.__entry.down = last_row_node
                last_row_node.top = self.__entry

        # add node to the column_map if not defined yet
        if not self.__column_head_by_constraint.get(covered_constraint):
            self.__column_head_by_constraint[covered_constraint] = last_column_node
            last = self.__get_last_row_node(None, head=self.__entry)
            if last is not last_column_node:
                self.__append_row_nodes(last, last_column_node)

        # add node to the row_map if not defined yet
        if not self.__row_head_by_candidate.get(candidate):
            self.__row_head_by_candidate[candidate] = last_row_node
            last = self.__get_last_column_node(None, head=self.__entry)
            if last is not last_row_node:
                self.__append_column_nodes(last, last_row_node)

        node = Node(candidate, covered_constraint,
                    self.__row_head_by_candidate[candidate],
                    self.__column_head_by_constraint[covered_constraint])
        self.__append_column_nodes(last_column_node, node)
        self.__append_row_nodes(last_row_node, node)
        self.__column_head_by_candidate[node.candidate] = node.column_head

        if node.column_head:
            node.column_head.size += 1

    def __append_row_nodes(self, last_row_node, node):
        last_row_node.right = node
        node.left = last_row_node

    def __append_column_nodes(self, last_column_node, node):
        last_column_node.down = node
        node.top = last_column_node

    def __get_last_row_node(self, candidate, head=None):
        current = self.__row_head_by_candidate.get(candidate) \
            if not head else head
        if current:
            while current.right:
                current = current.right
            return current

        return None

    def __get_last_column_node(self, covered_constraint, head=None):
        current = self.__column_head_by_constraint.get(covered_constraint) \
            if not head else head
        if current:
            while current.down:
                current = current.down
            return current

        return None


class Node(object):
    def __init__(self, candidate, covered_constraint,
                 row_head=None, column_head=None):
        self.top = None
        self.down = None
        self.left = None
        self.right = None
        self.candidate = candidate
        self.covered_constraint = covered_constraint
        self.row_head = row_head
        self.column_head = column_head

    def __repr__(self):
        return "Node('{}', '{}')".format(self.candidate,
                                         self.covered_constraint)

    def __str__(self):
        return "Node('{}', '{}')".format(self.candidate,
                                         self.covered_constraint)

    def __hash__(self):
        return hash((self.candidate, self.covered_constraint))

    def __eq__(self, other):
        return (self.candidate, self.covered_constraint) == \
               (other.candidate, other.covered_constraint)


class Header(Node):
    def __init__(self, candidate, covered_constraint,
                 row_head=None, column_head=None):
        super().__init__(candidate, covered_constraint,
                         row_head, column_head)
        self.size = 0


class ColumnIterator(object):
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        return self

    def __next__(self):
        next_node = 'top' if self._reversed else 'down'
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
        next_node = 'left' if self._reversed else 'right'
        if self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            return current
        else:
            raise StopIteration
