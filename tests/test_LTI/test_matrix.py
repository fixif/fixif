"""Unit tests for arb_mat utility functions."""

import numpy as np
import pytest

from fixif.func_aux.matrix import matrix, block, eye, hstack, vstack, zeros



def assert_matrix(m,n):
    #assert m.shape == n.shape
    for i,j in np.ndindex(m.shape):
        np.testing.assert_approx_equal(m[i, j], n[i, j])

# ──────────────────────────────────────────────
# construct
# ──────────────────────────────────────────────
@pytest.mark.parametrize("m", [
    np.array([[1.0, 2.0], [3.0, 4.0]]),
    np.array([1.0, 2.0, 3.0]),
    [[1.0, 0.0], [0.0, 1.0]],
    np.matrix([[1.0, 2.0], [3.0, 4.0]])
])
def test_construct(m):
    result = matrix(m)
    m = np.atleast_2d(np.array(m, dtype=float))
    assert_matrix(result, m)

# ──────────────────────────────────────────────
# to numpy
# ──────────────────────────────────────────────

@pytest.mark.parametrize("m", [
    [[1.0, 2.0], [3.0, 4.0]],
    [1.0, 2.0, 3.0],
    [[0.1, 0.0], [0.0, 1.0]],
    [[1.0, 2.0], [3.0, 4.0]]
])
def test_roundtrip(m):
    A = matrix(m).tonumpy()
    B = np.atleast_2d(np.array(m, dtype=float))
    assert_matrix(A, B)
    assert A.shape == B.shape
    assert A.dtype == float



# ──────────────────────────────────────────────
# zeros
# ──────────────────────────────────────────────

def test_values_are_zero():
    m = zeros(3, 4)
    assert_matrix(m, np.zeros((3, 4)))


# ──────────────────────────────────────────────
# eye
# ──────────────────────────────────────────────

@pytest.mark.parametrize("n", [1,2,3,12,20,37])
def test_nxn(n):
    assert_matrix(eye(n), np.eye(n))


@pytest.mark.parametrize("key", [
    pytest.param((0, slice(None)),              id="m[0, :]"),
    pytest.param((slice(None), 1),              id="m[:, 1]"),
    pytest.param((slice(0, 2), slice(None)),    id="m[0:2, :]"),
    pytest.param((slice(None), slice(1, 3)),    id="m[:, 1:3]"),
    pytest.param((slice(0, 2), slice(1, 3)),    id="m[0:2, 1:3]"),
    pytest.param((-1, slice(None)),             id="m[-1, :]"),
    pytest.param(1,                             id="m[1]"),
])
def test_slicing(key):
    m = matrix([[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])
    n = m.tonumpy()
    # tweak the key, in order to transform [:,1] in [:,[1]], otherwise numpy array are not 2d...
    if isinstance(key, tuple):
        key2 = tuple(k if isinstance(k, slice) else [k] for k in key)
    else:
        key2 = [key]
    assert_matrix(m[key], n[key2])






# ──────────────────────────────────────────────
# hstack
# ──────────────────────────────────────────────

def test_vtwo_matrices():
    A = matrix(np.array([[1.0, 2.0], [3.0, 4.0]]))
    B = matrix(np.array([[5.0], [6.0]]))
    result = hstack(A, B)
    expected = np.array([[1.0, 2.0, 5.0], [3.0, 4.0, 6.0]])
    assert_matrix(result, expected)

def test_vthree_matrices():
    A = matrix(np.ones((2, 1)))
    B = matrix(np.ones((2, 2)))
    C = matrix(np.ones((2, 3)))
    result = hstack(A, B, C)
    assert result.nrows() == 2
    assert result.ncols() == 6

def test_hshape():
    A = matrix(np.zeros((3, 2)))
    B = matrix(np.zeros((3, 4)))
    result = hstack(A, B)
    assert result.shape == (3,6)

def test_incompatible_rows_raises():
    A = matrix(np.zeros((2, 2)))
    B = matrix(np.zeros((3, 2)))
    with pytest.raises(ValueError):
        hstack(A, B)

def test_with_zeros():
    A = matrix(np.eye(2))
    Z = zeros(2, 2)
    result = hstack(A, Z)
    expected = np.array([[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0]])
    assert_matrix(result, expected)


# ──────────────────────────────────────────────
# vstack
# ──────────────────────────────────────────────

def test_htwo_matrices():
    A = matrix(np.array([[1.0, 2.0]]))
    B = matrix(np.array([[3.0, 4.0]]))
    result = vstack(A, B)
    expected = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert_matrix(result, expected)

def test_hthree_matrices():
    A = matrix(np.ones((1, 3)))
    B = matrix(np.ones((2, 3)))
    C = matrix(np.ones((3, 3)))
    result = vstack(A, B, C)
    assert result.shape == (6,3)


def test_vshape():
    A = matrix(np.zeros((2, 4)))
    B = matrix(np.zeros((3, 4)))
    result = vstack(A, B)
    assert result.shape == (5,4)
    

def test_incompatible_cols_raises():
    A = matrix(np.zeros((2, 2)))
    B = matrix(np.zeros((2, 3)))
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
    assert_matrix(result, expected)


# ──────────────────────────────────────────────
# block
# ──────────────────────────────────────────────


def test_2x2_blocks():
    A = matrix(np.array([[1.0, 2.0], [3.0, 4.0]]))
    Z = zeros(2, 2)
    result = block([[A, Z], [Z, A]])
    expected = np.block([[np.array([[1.0, 2.0], [3.0, 4.0]]),
                           np.zeros((2, 2))],
                          [np.zeros((2, 2)),
                           np.array([[1.0, 2.0], [3.0, 4.0]])]])
    assert_matrix(result, expected)

def test_series_connection_block():
    """Block structure used in dSS.__mul__."""
    n1, n2 = 2, 3
    A1 = matrix(np.eye(n1))
    A2 = matrix(np.eye(n2))
    B2C1 = matrix(np.ones((n2, n1)))
    result = block([
        [A1,     zeros(n1, n2)],
        [B2C1,   A2               ],
    ])
    assert result.nrows() == n1 + n2
    assert result.ncols() == n1 + n2

def test_shape():
    A = matrix(np.ones((2, 3)))
    B = matrix(np.ones((2, 4)))
    C = matrix(np.ones((5, 3)))
    D = matrix(np.ones((5, 4)))
    result = block([[A, B], [C, D]])
    assert result.shape == (7,7)

def test_single_block():
    A = matrix(np.eye(3))
    result = block([[A]])
    assert_matrix(result, np.eye(3))