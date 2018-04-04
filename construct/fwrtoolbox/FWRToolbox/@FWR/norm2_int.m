% calcule la norme L2 qd y'a des intervalles (façon gram)

function l = norm2_int( R)

% sup de la trace !!
l = sqrt( sup(trace( R.CZ*R.Wc*R.CZ' + R.DZ*R.DZ')) );