"""
A collection of functions to deal with arb_mat objects (matrices with ball interval at arbitrary precision)
"""

import numpy as np
from flint import arb_mat


class matrix(arb_mat):
    """arbitrary precision ball matrices based on arb_mat
    `plus some extra methods to help its use (like numpy conversion, slices, etc.)"""
    
    def __init__(self, *args):
        if len(args)==1 and isinstance(args[0], np.ndarray):
            M = np.atleast_2d(np.array(args[0], dtype=float))
            # copy the data
            arb_mat.__init__(self, *M.shape)
            for i, j in np.ndindex(M.shape):
                self[i, j] = M[i, j]

        elif  len(args)==1 and isinstance(args[0], (int,float)):
            arb_mat.__init__(self, [[args[0]]])
        elif  len(args)==1 and isinstance(args[0], list) and all(isinstance(i, (int, float)) for i in args[0]):
            arb_mat.__init__(self, [args[0]])
        else:
            # otherwise call arb_mat super
            arb_mat.__init__(self, *args)
    

    def tonumpy(self) -> np.ndarray:
        """Convert an arb_mat to a 2D numpy array (midpoints only).
            ⚠️ Only the midpoint of each ball is extracted;

        Returns:
            A 2D numpy array of float64.

        Example::

            >>> matrix([[1, 2], [3, 4]]).tonumpy()
            array([[1., 2.],
                   [3., 4.]])
        """
        A = np.zeros(self.shape, dtype=float)
        for i, j in np.ndindex(A.shape):
                A[i, j] = float(self[i, j].mid())
        return A


    @property
    def shape(self) -> tuple:
        """Return the shape of the matrix, as in numpy array."""
        return self.nrows(), self.ncols()

    def __add__(self, other):
        result = super().__add__(other)
        return matrix(result)

    def __sub__(self, other):
        result = super().__sub__(other)
        return matrix(result)

    def __neg__(self):
        result = super().__neg__()
        return matrix(result)

    def __mul__(self, other):
        result = super().__mul__(other)
        return matrix(result)

    def transpose(self):
        return matrix(super().transpose())


    def __getitem__(self, key):
        # scalar m[i, j]
        if isinstance(key, tuple) and len(key) == 2:
            row_key, col_key = key

            # for integer, ask arb_mat
            if isinstance(row_key, int) and isinstance(col_key, int):
                return super().__getitem__(key)

            # for slices
            rows = self._resolve(row_key, self.nrows())
            cols = self._resolve(col_key, self.ncols())

            result = matrix(len(rows), len(cols))
            for i, r in enumerate(rows):
                for j, c in enumerate(cols):
                    result[i, j] = super().__getitem__((r, c))
            return result

        # m[i] or m[i:k] -> rows
        if isinstance(key, (int, slice)):
            rows = self._resolve(key, self.nrows())
            ncols = self.ncols()
            result = matrix(len(rows), ncols)
            for i, r in enumerate(rows):
                for j in range(ncols):
                    result[i, j] = super().__getitem__((r, j))
            return result

        raise TypeError(f"unsupported index type: {type(key)}")

    def _resolve(self, key: int | slice, size: int) -> list[int]:
        """Convert an int or slice to a list of indices.

        Args:
            key:  An integer index or a slice object.
            size: The dimension size (nrows or ncols).

        Returns:
            List of integer indices.

        Raises:
            IndexError: If an integer index is out of range.
        """
        if isinstance(key, int):
            if key < -size or key >= size:
                raise IndexError(f"index {key} out of range for size {size}")
            return [key % size]
        if isinstance(key, slice):
            return list(range(*key.indices(size)))
        raise TypeError(f"unsupported index type: {type(key)}")


# ──────────────────────────────────────────────
# Construction
# ──────────────────────────────────────────────

def zeros(nrows: int, ncols: int) -> matrix:
    """Return a zero :class:`arb_mat` of shape (nrows, ncols).

    Equivalent to :func:`numpy.zeros`.

    Args:
        nrows: Number of rows.
        ncols: Number of columns.

    Returns:
        Zero matrix of shape ``(nrows, ncols)``.
    """
    return matrix(nrows, ncols)


def eye(n: int) -> matrix:
    """Return the n-by-n identity :class:`arb_mat`.

    Equivalent to :func:`numpy.eye`.

    Args:
        n: Matrix dimension.

    Returns:
        Identity matrix of shape ``(n, n)``.
    """
    result = matrix(n, n)
    for i in range(n):
        result[i, i] = 1
    return result


# ──────────────────────────────────────────────
# Stacking / concatenation
# ──────────────────────────────────────────────

def hstack(*matrices: matrix) -> matrix:
    """Concatenate :class:`arb_mat` matrices horizontally.

    Equivalent to :func:`numpy.concatenate` along axis=1,
    or ``numpy.c_[...]``.

    Args:
        *matrices: Matrices with the same number of rows.

    Returns:
        Horizontally concatenated matrix.

    Raises:
        ValueError: If matrices do not have the same number of rows.
    """
    nrows = matrices[0].nrows()
    if any(m.nrows() != nrows for m in matrices):
        raise ValueError("All matrices must have the same number of rows")
    ncols = sum(m.ncols() for m in matrices)
    result = matrix(nrows, ncols)
    col_offset = 0
    for m in matrices:
        for i,j in np.ndindex(m.shape):
             result[i, col_offset + j] = m[i, j]
        col_offset += m.ncols()
    return result


def vstack(*matrices: matrix) -> matrix:
    """Concatenate :class:`arb_mat` matrices vertically.

    Equivalent to :func:`numpy.concatenate` along axis=0,
    or ``numpy.r_[...]``.

    Args:
        *matrices: Matrices with the same number of columns.

    Returns:
        Vertically concatenated matrix.

    Raises:
        ValueError: If matrices do not have the same number of columns.
    """
    ncols = matrices[0].ncols()
    if any(m.ncols() != ncols for m in matrices):
        raise ValueError("All matrices must have the same number of columns")
    nrows = sum(m.nrows() for m in matrices)
    result = matrix(nrows, ncols)
    row_offset = 0
    for m in matrices:
        for i,j in np.ndindex(m.shape):
            result[row_offset + i, j] = m[i, j]
        row_offset += m.nrows()
    return result



def block(blocks: list[list[matrix]]) -> matrix:
    """Assemble an :class:`arb_mat` from nested lists of blocks.

    Equivalent to :func:`numpy.block`.

    Args:
        blocks: A 2D list of :class:`arb_mat` where ``blocks[i][j]``
            is the block at row *i*, column *j*. All blocks in the same
            row must have the same number of rows; all blocks in the same
            column must have the same number of columns.

    Returns:
        Block matrix assembled from the given blocks.

    Example::


        .. math::

            M = \\begin{pmatrix} A & 0 \\\\ B C & D \\end{pmatrix}

        is built as::

            arb_block([[A, arb_zeros(n1, n2)],
                       [B @ C, D]])
    """

    rows = [hstack(*row) for row in blocks]
    return vstack(*rows)