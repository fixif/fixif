% calcule la norme L2 qd y'a des intervalles (façon gram)

function l = norm2_int( A,B,C,D)


Wc = gram_int(A,B,C,D, 'c');
l = sqrt( trace( C*Wc*C' + D*D') );