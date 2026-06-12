"""Unit tests for arb_mat utility functions."""

import numpy as np
import pytest
from flint import arb_mat

from fixif.func_aux.arb_mtx_helper import (
    arb2numpy,
    block,
    eye,
    hstack,
    numpy2arb,
    vstack,
    zeros,
)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def assert_arb_close(m: arb_mat, expected: np.ndarray, tol: float = 1e-12) -> None:
    """Assert that an arb_mat is close to a numpy array (midpoints)."""
    result = arb2numpy(m)
    np.testing.assert_allclose(result, expected, atol=tol)


# ──────────────────────────────────────────────
# numpy2arb
# ──────────────────────────────────────────────
def test_2d_array():
    m = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = numpy2arb(m)
    assert result.nrows() == 2
    assert result.ncols() == 2
    assert_arb_close(result, m)

def test_1d_array_becomes_row():
    v = np.array([1.0, 2.0, 3.0])
    result = numpy2arb(v)
    assert result.nrows() == 1
    assert result.ncols() == 3

def test_python_list():
    m = [[1.0, 0.0], [0.0, 1.0]]
    result = numpy2arb(m)
    assert_arb_close(result, np.eye(2))

def test_numpy_matrix():
    m = np.matrix([[1.0, 2.0], [3.0, 4.0]])  # noqa: E501
    result = numpy2arb(m)
    assert_arb_close(result, np.array([[1.0, 2.0], [3.0, 4.0]]))


# ──────────────────────────────────────────────
# arb2numpy
# ──────────────────────────────────────────────


def test_roundtrip():
    m = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert_arb_close(numpy2arb(m), m)

def test_arbshape():
    m = arb_mat([[1, 2, 3], [4, 5, 6]])
    result = arb2numpy(m)
    assert result.shape == (2, 3)

def test_dtype_is_float():
    m = arb_mat([[1, 2], [3, 4]])
    result = arb2numpy(m)
    assert result.dtype == float



# ──────────────────────────────────────────────
# zeros
# ──────────────────────────────────────────────

def test_values_are_zero():
    m = zeros(3, 4)
    assert_arb_close(m, np.zeros((3, 4)))




# ──────────────────────────────────────────────
# eye
# ──────────────────────────────────────────────

@pytest.mark.parametrize("n", [1,2,3,12,20,37])
def test_nxn(n):
    assert_arb_close(eye(n), np.eye(n))



# ──────────────────────────────────────────────
# hstack
# ──────────────────────────────────────────────

def test_vtwo_matrices():
    A = numpy2arb(np.array([[1.0, 2.0], [3.0, 4.0]]))
    B = numpy2arb(np.array([[5.0], [6.0]]))
    result = hstack(A, B)
    expected = np.array([[1.0, 2.0, 5.0], [3.0, 4.0, 6.0]])
    assert_arb_close(result, expected)

def test_vthree_matrices():
    A = numpy2arb(np.ones((2, 1)))
    B = numpy2arb(np.ones((2, 2)))
    C = numpy2arb(np.ones((2, 3)))
    result = hstack(A, B, C)
    assert result.nrows() == 2
    assert result.ncols() == 6

def test_hshape():
    A = numpy2arb(np.zeros((3, 2)))
    B = numpy2arb(np.zeros((3, 4)))
    result = hstack(A, B)
    assert result.nrows() == 3
    assert result.ncols() == 6

def test_incompatible_rows_raises():
    A = numpy2arb(np.zeros((2, 2)))
    B = numpy2arb(np.zeros((3, 2)))
    with pytest.raises(ValueError):
        hstack(A, B)

def test_with_zeros():
    A = numpy2arb(np.eye(2))
    Z = zeros(2, 2)
    result = hstack(A, Z)
    expected = np.array([[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0]])
    assert_arb_close(result, expected)


# ──────────────────────────────────────────────
# vstack
# ──────────────────────────────────────────────

def test_htwo_matrices():
    A = numpy2arb(np.array([[1.0, 2.0]]))
    B = numpy2arb(np.array([[3.0, 4.0]]))
    result = vstack(A, B)
    expected = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert_arb_close(result, expected)

def test_hthree_matrices():
    A = numpy2arb(np.ones((1, 3)))
    B = numpy2arb(np.ones((2, 3)))
    C = numpy2arb(np.ones((3, 3)))
    result = vstack(A, B, C)
    assert result.nrows() == 6
    assert result.ncols() == 3

def test_vshape():
    A = numpy2arb(np.zeros((2, 4)))
    B = numpy2arb(np.zeros((3, 4)))
    result = vstack(A, B)
    assert result.nrows() == 5
    assert result.ncols() == 4

def test_incompatible_cols_raises():
    A = numpy2arb(np.zeros((2, 2)))
    B = numpy2arb(np.zeros((2, 3)))
    with pytest.raises(ValueError):
        vstack(A, B)

def test_with_eye():
    I2 = eye(2)
    Z = zeros(2, 2)
    result = vstack(I2, Z)
    expected = np.array([[1.0, 0.0],
                          [0.0, 1.0],
                          [0.0, 0.0],
                          [0.0, 0.0]])
    assert_arb_close(result, expected)


# ──────────────────────────────────────────────
# block
# ──────────────────────────────────────────────


def test_2x2_blocks():
    A = numpy2arb(np.array([[1.0, 2.0], [3.0, 4.0]]))
    Z = zeros(2, 2)
    result = block([[A, Z], [Z, A]])
    expected = np.block([[np.array([[1.0, 2.0], [3.0, 4.0]]),
                           np.zeros((2, 2))],
                          [np.zeros((2, 2)),
                           np.array([[1.0, 2.0], [3.0, 4.0]])]])
    assert_arb_close(result, expected)

def test_series_connection_block():
    """Block structure used in dSS.__mul__."""
    n1, n2 = 2, 3
    A1 = numpy2arb(np.eye(n1))
    A2 = numpy2arb(np.eye(n2))
    B2C1 = numpy2arb(np.ones((n2, n1)))
    result = block([
        [A1,     zeros(n1, n2)],
        [B2C1,   A2               ],
    ])
    assert result.nrows() == n1 + n2
    assert result.ncols() == n1 + n2

def test_shape():
    A = numpy2arb(np.ones((2, 3)))
    B = numpy2arb(np.ones((2, 4)))
    C = numpy2arb(np.ones((5, 3)))
    D = numpy2arb(np.ones((5, 4)))
    result = block([[A, B], [C, D]])
    assert result.nrows() == 7
    assert result.ncols() == 7

def test_single_block():
    A = numpy2arb(np.eye(3))
    result = block([[A]])
    assert_arb_close(result, np.eye(3))