
function M = DFT(n)

n

if n==2
	M = [1 1; 1 -1];
elseif fix(log2(n))~=log2(n)
	error('n is not a power of 2')
else
	if mod( log2(n),2 )==0
		k = sqrt(n);
		Mk = DFT(k);
		M = kron( Mk,eye(k) ) * Trn(k,n) * kron( eye(k),Mk ) * Lrn(k,n);
	else
		k = 2^floor(log2(n)/2);
		Mk = DFT(k);
		M2k = kron( [1 1; 1 -1],eye(k) ) * Trn(k,2*k) * kron( eye(2),Mk ) * Lrn(2,2*k);
		M = kron( Mk,eye(2*k) ) * Trn(2*k,n) * kron( eye(k),M2k ) * Lrn(k,n);
	end
		
	%M = kron( DFT(r), eye(s) ) * Trn(s,n) * kron( eye(r), DFT(s) ) * Lrn(r,n);
end