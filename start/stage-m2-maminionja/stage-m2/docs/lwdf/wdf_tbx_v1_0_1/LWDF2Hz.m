function Hz = lwdf2Hz(LWDF)
%LWDF2HZ	Calculate the transfer function H(z) given an LWDF
%	Hz = LWDF2HZ(LWDF) derives the discrete-time transfer function H(z)
%	that belongs to the given Lattice Wave Digital Filter (LWDF).
%	Here LWDF is a structure that should contain the fields
%		LWDF.wdaCodes
%		LWDF.gamma
%	LWDF.wdaCodes is an [2x?] character array, which is
%	described in 'Hs2LWDF.m', as well as in 'showLWDF.m'. 
%	LWDF.gamma contains the coefficients belonging to the wdaCodes.
%	The returned structure Hz contains both the description of the
%	regular output, Hz(1), as well as that of the reflected output, Hz(2).
%	Both Hz(1) and Hz(2) contain
%		Hz(*).poly_fz         -- the coefficients of the numerator function
%		Hz(*).poly_gz         -- the coefficients of the denominator function
%		Hz(*).ident           -- a string, describing the filter
%		Hz(*).roots_fz        -- the roots of the numerator 
%		Hz(*).roots_gz        -- the roots of the denominator
%	( with * 1 or 2 ) where Hz(*).poly_fz and Hz(*).poly_gz are vectors of 
%	coefficients in either descending positive powers of z (N,N-1,...,2,1,0), 
%	or ascending negative powers of z (0,-1,-2,...,-(N-1),-N).
%
%	If the coefficients indicate that we deal with a bireciprocal low/high 
%	pass filter, this property is mentioned in the 'ident' field.
%
%	See also SHOWLWDF, HS2LWDF.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, Febrary 2004

wdaCodes = LWDF.wdaCodes;
gamma	 = LWDF.gamma;

% determine filter order from description in wdaCodes
codes = wdaCodes(:);
order1 = sum( (codes == 't') | (codes == 's') );
order2 = sum( (codes == 'S') | (codes == 'd') );
order4 = sum( (codes == 'D') );
filterOrder = order1 + 2*order2 + 4*order4;
lowPass = ( rem(filterOrder,2) == 1 );

nTopRowSlices    = length( wdaCodes(1,:) );
nBottomRowSlices = sum( wdaCodes(2,:) ~= 'x' );

% -1: s,t,S      p2-p1

numH1z = 1;
numH2z = 1;
for i = 1:nTopRowSlices
	switch wdaCodes(1,i)
		case 't'
			numH1z = -[ 0 -1 ];
		case 's'
			numH1z = conv( numH1z, -[gamma(1,i,1) -1] );
		case 'S'
			numH1z = conv( numH1z, -[gamma(1,i,1) 0 -1] );
		case 'd'
			numH1z = conv( numH1z, [-gamma(1,i,1)  -gamma(2,i,1)*(1-gamma(1,i,1))  1] );
		case 'D'
			numH1z = conv( numH1z, ...
						    [-gamma(1,i,1)  0  -gamma(2,i,1)*(1-gamma(1,i,1))  0   1] );
	end
end
for i = 1:nBottomRowSlices
	switch wdaCodes(2,i)
		case 'S'
			numH2z = conv( numH2z, -[gamma(1,i,2) 0 -1] );
		case 'd'
			numH2z = conv( numH2z, [-gamma(1,i,2)  -gamma(2,i,2)*(1-gamma(1,i,2))  1] );
		case 'D'
			numH2z = conv( numH2z, ...
						    [-gamma(1,i,2)  0  -gamma(2,i,2)*(1-gamma(1,i,2))  0   1] );
		otherwise
			wdaCodes
			beep; 
            error( 'Check LWDF.wdaCodes ...' );

	end
end

denH1z = fliplr(numH1z);
denH2z = fliplr(numH2z);
poly1  = conv(denH2z,numH1z);
poly2  = conv(denH1z,numH2z);
% compute both the regular as well as the complementary outputs
poly_fz_add = (poly1 + poly2) / 2;
poly_fz_sub = (poly2 - poly1) / 2;
if lowPass
	poly_fz1 = poly_fz_add;
	poly_fz2 = poly_fz_sub;
else
	poly_fz1 = poly_fz_sub;
	poly_fz2 = poly_fz_add;
end
poly_gz      = conv(denH1z,denH2z);

% parameters of regular output
Hz1.poly_fz  = poly_fz1;
Hz1.poly_gz  = poly_gz;
Hz1.ident    = 'H(z) reconstructed from LWDF coefficients ...';
Hz1.roots_fz = roots(poly_fz1);
Hz1.roots_gz = roots(poly_gz);

% parameters of complementary output
Hz2.poly_fz  = poly_fz2;
Hz2.poly_gz  = poly_gz;
Hz2.ident    = 'complementary H(z) obtained from LWDF coeffs ...';
Hz2.roots_fz = roots(poly_fz2);
Hz2.roots_gz = roots(poly_gz);

% if the coefficients indicate that we deal with a bireciprocal low/high pass filter,
% signal this through the 'ident' field
if all( abs(gamma(1:2:end)) <= 1e-10  )
	Hz1.ident = [ 'BIRECIPROCAL ' Hz1.ident ];
	Hz2.ident = [ 'BIRECIPROCAL ' Hz2.ident ];
	fprintf( 'results in a Bireciprocal design structure\n\n' );
end

% combine both structures
Hz = [ Hz1 Hz2 ];
