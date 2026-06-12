"""
A collection of functions to deal with arb_mat objects (matrices with ball interval at arbitrary precision)
"""

import numpy as np
from flint import arb_mat


# ──────────────────────────────────────────────
# Conversions
# ──────────────────────────────────────────────

def something2arb(M) -> arb_mat:
    if isinstance(M, np.ndarray):
        return numpy2arb(M)
    elif isinstance(M, int) or isinstance(M, float):
        return arb_mat([[M]])
    else:
        return arb_mat(M)

def numpy2arb(M: np.ndarray) -> arb_mat:
    """Convert a 2D numpy array to an arb_mat.

    Args:
        M: A 2D numpy array (or matrix).

    Returns:
        The corresponding :class:`arb_mat`.

    Example::

        >>> np_to_arb(np.eye(2))
        [1, 0]
        [0, 1]
    """
    M = np.atleast_2d(np.array(M, dtype=float))
    # copy the data
    A = arb_mat(*M.shape)
    for i, j in np.ndindex(M.shape):
        A[i, j] = M[i, j]
    return A


def arb2numpy(M: arb_mat) -> np.ndarray:
    """Convert an arb_mat to a 2D numpy array (midpoints only).

    Note:
        Only the midpoint of each ball is extracted;

    Args:
        M: An :class:`arb_mat`.

    Returns:
        A 2D numpy array of float64.

    Example::

        >>> arb_to_np(arb_mat([[1, 2], [3, 4]]))
        array([[1., 2.],
               [3., 4.]])
    """
    nrows, ncols = M.nrows(), M.ncols()
    A = np.zeros((nrows, ncols), dtype=float)
    for i, j in np.ndindex(A.shape):
            A[i, j] = float(M[i, j].mid())
    return A


# ──────────────────────────────────────────────
# Construction
# ──────────────────────────────────────────────

def zeros(nrows: int, ncols: int) -> arb_mat:
    """Return a zero :class:`arb_mat` of shape (nrows, ncols).

    Equivalent to :func:`numpy.zeros`.

    Args:
        nrows: Number of rows.
        ncols: Number of columns.

    Returns:
        Zero matrix of shape ``(nrows, ncols)``.
    """
    return arb_mat(nrows, ncols)


def eye(n: int) -> arb_mat:
    """Return the n-by-n identity :class:`arb_mat`.

    Equivalent to :func:`numpy.eye`.

    Args:
        n: Matrix dimension.

    Returns:
        Identity matrix of shape ``(n, n)``.
    """
    result = arb_mat(n, n)
    for i in range(n):
        result[i, i] = 1
    return result


# ──────────────────────────────────────────────
# Stacking / concatenation
# ──────────────────────────────────────────────

def hstack(*matrices: arb_mat) -> arb_mat:
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
    result = arb_mat(nrows, ncols)
    col_offset = 0
    for m in matrices:
        for i,j in np.ndindex((nrows, m.ncols())):
             result[i, col_offset + j] = m[i, j]
        col_offset += m.ncols()
    return result


def vstack(*matrices: arb_mat) -> arb_mat:
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
    result = arb_mat(nrows, ncols)
    row_offset = 0
    for m in matrices:
        for i,j in np.ndindex((m.nrows(), ncols)):
            result[row_offset + i, j] = m[i, j]
        row_offset += m.nrows()
    return result



def block(blocks: list[list[arb_mat]]) -> arb_mat:
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