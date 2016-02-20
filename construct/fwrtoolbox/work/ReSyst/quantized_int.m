% quantification de X sur n bits
% renvoie un interval... sur n 

function rep = quantized_int(X, n)

	if X==0
		rep = infsup(0,0)
	else
		gammaX = n - 2 -floor(log2( abs(X) ) );
		rep = infsup( floor( X*2^gammaX ) * 2^-gammaX, ceil( X*2^gammaX ) * 2^-gammaX );
	
end