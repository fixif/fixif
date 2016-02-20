% calcule un grammien qd y'a des intervalles (façon gram)

function W = gram_int( A,B,C,D, ch)


if isintval(A)==1
	if ch=='c'
		W = vermatreqn( A, A', -eye(size(A)), eye(size(A)),  -B*B');
	else
		W = vermatreqn( A', A, -eye(size(A)), eye(size(A)), -C'*C);
	end
else
	S = ss(A,B,C,D,-1)
	W = gram(S,ch)
end