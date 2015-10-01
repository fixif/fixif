int sum_c( int i)
	{
	return (((i>>1) & 1) + ( i & 1)) & 1;
	}
