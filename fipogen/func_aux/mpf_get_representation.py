import mpmath

def mpf_get_representation(a):
	"""
	Given a MP floating-point number of type mpmath.mpf
	this function returns a tuple (y, n) of python long integers
	such that
	    a = y * 2**n
	exactly.

	If the number is +Inf, -Inf or NaN

	WARNING: we get into the internal structure of MPF class.
	a._mpf_ yeilds a tuple of four variables:
		_mpf_[0] - sign
		_mpf_[1] - mantissa
		_mpf_[2] - exponent
		_mpf_[3] - size of mantissa with which the number was created

	Parameters
	----------
	a - MP number

	Returns
	-------
	y - long
	n - int or long
	"""
	if not isinstance(a, mpmath.mpf):
		raise ValueError('Expected mpmath.mpf but got %s' % type(a))

	if not mpmath.isnormal(a):
		raise ValueError('Cannot get a representation of a not normal number')

	t = a._mpf_
	if len(t) != 4:
		raise ValueError('Something is wrong, could not get mpf number structure')

	n = t[2]
	y = -t[1] if t[0] else t[1]

	return y, n

