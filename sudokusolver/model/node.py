class Node(object):
    """
    Simple data structure representing a node within a ConstraintMatrix.
    It know its left, bottom, right and top neighbour.
    In addition, it is also aware of the row and column it belongs to.
    """
    def __init__(self, candidate, covered_constraint,
                 row_ref_node=None, column_ref_node=None):
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.candidate = candidate
        self.covered_constraint = covered_constraint
        self.row_ref_node = row_ref_node
        self.column_ref_node = column_ref_node

    @staticmethod
    def connect(a, b, how: str):
        """Joins the given nodes **vertically** or **horizontally** together."""
        if how.lower() == 'vertically':
            if a:
                a.bottom = b
            if b:
                b.top = a
        if how.lower() == 'horizontally':
            if a:
                a.right = b
            if b:
                b.left = a

    @staticmethod
    def disconnect(node, how: str):
        """Disjoins the given node **vertically** or **horizontally** from its neighbours."""
        if how.lower() == 'vertically':
            if node.left:
                node.left.right = node.right
            if node.right:
                node.right.left = node.left
        if how.lower() == 'horizontally':
            if node.top:
                node.top.bottom = node.bottom
            if node.bottom:
                node.bottom.top = node.top

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


class RowReferenceNode(Node):
    """
    Special kind of node that refers another rode.
    Used by the ConstraintMatrix to address rows and
    iterate through their nodes.
    """
    def __init__(self, candidate):
        super().__init__(candidate, '_', None, None)

    def __iter__(self):
        return iter(RowIterator(self.right))

    def get_last_node(self):
        """Returns the last node of the row represented by this RowReferenceNode."""
        if not self.right:
            return None
        nodes = [node for node in self]
        return nodes.pop()


class ColumnReferenceNode(Node):
    """
    Special kind of node that refers another rode.
    Used by the ConstraintMatrix to address columns and
    iterate through their nodes.
    """
    def __init__(self, covered_constraint):
        super().__init__('_', covered_constraint, None, None)
        self.size = 0

    def __iter__(self):
        return iter(ColumnIterator(self.bottom))

    def get_last_node(self) -> Node:
        """Returns the last node of the column represented by this ColumnReferenceNode."""
        if not self.bottom:
            return None
        nodes = [node for node in self]
        return nodes.pop()


class MatrixHeadReferenceNode(Node):
    """
    Special kind of node that refers to ColumnReferenceNodes and RowReferenceNodes.
    Used by the ConstraintMatrix to itereate through its columns and rows.
    """
    def __init__(self):
        super().__init__('_', '_', None, None)

    def get_last_column_ref_node(self) -> Node:
        """Returns the last ColumnReferenceNode in the matrix otherwise itself"""
        ref_nodes = [ref_node for ref_node in RowIterator(self)]
        return ref_nodes.pop()

    def get_last_row_ref_node(self) -> Node:
        """Returns the last RowReferenceNode in the matrix otherwise itself"""
        ref_nodes = [ref_node for ref_node in ColumnIterator(self)]
        return ref_nodes.pop()

    def get_column_ref_node_iterator(self):
        """Returns iterator iterating through the ColumnRerefernceNodes"""
        return RowIterator(self.right)

    def get_row_ref_node_iterator(self):
        """Returns iterator iterating through the RowReferenceNodes"""
        return ColumnIterator(self.bottom)


class ColumnIterator(object):
    """Iterates through a sequence of vertically connected nodes."""
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        next_node = 'top' if self._reversed else 'bottom'
        while self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            yield current


class RowIterator(object):
    """Iterates through a sequence of horizontally connected nodes."""
    def __init__(self, start, reversed=False):
        self._current = start
        self._reversed = reversed

    def __iter__(self):
        next_node = 'left' if self._reversed else 'right'
        while self._current:
            current, self._current = \
                self._current, vars(self._current)[next_node]
            yield current
