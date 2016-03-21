function Hs = Hs_invcheby(filterOrder,stopBandRipple_dB,cutOffFrequency,freqNormMode)
%HS_INVCHEBY  Inverse Chebyshev lowpass filter design.
%	Hs = HS_INVCHEBY(filterOrder,stopBandRipple_dB) returns a 
%	structure Hs describing the continuous-time transfer function of a
%	normalized (cutoff frequency = 1) Inverse Chebyshev approximation 
%	of the ideal lowpass filter. 
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s.  The length of the vector poly_gs equals the filterOrder +1,
%	while the length of g(s) equals filterOrder for odd filterOrders, and 
%	filterOrder+1 for even orders.  
%	By default the cutoff frequency is normalized to equal 1.0 at that point 
%	of the transition slope where the magnitude equals the maxima of the 
%	stopband ripple.
%
%	Hs = HS_INVCHEBY(filterOrder,stopBandRipple_dB,cutOffFrequency) 
%	returns the	output parameters for the denormalized cutOffFrequency.
%
%	Hs = HS_INVCHEBY(filterOrder,stopBandRipple_dB,cutOffFrequency, ...
%																 freqNormMode) 
%	with freqNormMode 0 returns the same output as the previous description. 
%	For freqNormMode 1, the cutoff frequency is defined to be at the -3 dB 
%	magnitude level.
%
%	See also HS_BUTTER, HS_CHEBY, HS_CAUER, HS_CAUER_BIREC, HS_VLACH.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003 ...


if (nargin == 2)
	cutOffFrequency = 1;
	freqNormMode    = 0;
elseif (nargin == 3)
	freqNormMode    = 0;
end

d = sqrt( 10 ^ (stopBandRipple_dB/10) -1 );
a = asinh(d) / filterOrder;
oddFilterOrder = ( mod(filterOrder,2) == 1 );

nComplexRoots = 2*floor( filterOrder / 2 );
phi = (1:2:nComplexRoots-1)*pi / (2*filterOrder);

% calculate the roots of the numerator f(s)
roots_fs = zeros(nComplexRoots,1);
imagPartOfRoots = j ./ cos(phi);
roots_fs(1:2:end) = -imagPartOfRoots;
roots_fs(2:2:end) =  imagPartOfRoots;
% remember the cut-off frequency

% calculate the roots of the denominator g(s)
sinha = sinh( a );
[realPartOfRoots,ix] = sort( sinha * sin(phi) );
imagPartOfRoots = cosh( a ) * cos(phi(ix));
% reserve space and preset to 0
allRoots = zeros(filterOrder,1);
allRoots(1:2:nComplexRoots) = -realPartOfRoots + j*imagPartOfRoots;
allRoots(2:2:nComplexRoots) = -realPartOfRoots - j*imagPartOfRoots;
if oddFilterOrder
	allRoots(end) = -sinha;
end
roots_gs = 1 ./ allRoots;

% remember the stop band frequency and the frequency normalization mode
if ( freqNormMode == 0 )
	Kw = cutOffFrequency;
else
	Kw = cutOffFrequency * cosh( acosh(d)/filterOrder );
end
roots_fs = Kw * roots_fs;
% re-order the roots of g(s) to facilitate their use in lwdf-design
roots_gs = Kw * flipud(roots_gs);

% construct the output polynomials and return the results in a structure Hs
K0 = real( prod( -roots_gs ) / prod( roots_fs ) );
Hs.poly_fs  = K0 * poly( roots_fs );
Hs.poly_gs  = real( poly( roots_gs ) );
Hs.ident    = [ 'LP PROTOTYPE: ''invcheby'',' num2str(filterOrder) ',' num2str(stopBandRipple_dB) ...
							',' num2str(cutOffFrequency) ',' num2str(freqNormMode) ];
Hs.roots_fs = roots_fs;
Hs.roots_gs = roots_gs;
