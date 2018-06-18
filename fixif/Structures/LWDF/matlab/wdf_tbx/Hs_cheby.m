function Hs = Hs_cheby(filterOrder,passBandRipple_dB,cutOffFrequency,freqNormMode)
%HS_CHEBY   Chebyshev lowpass filter design.
%	Hs = HS_CHEBY(filterOrder,passBandRipple_dB) returns a structure Hs 
%	describing the continuous-time transfer function of a normalized 
%	(cutoff frequency = 1) Chebyshev approximation of the ideal lowpass filter. 
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s (for the Chebyshev approximation, poly_fs = 1.0). 
%   The length of the vector poly_gs equals the filterOrder +1. 
%	By default the cutoff frequency is normalized to equal 1.0 at that point 
%	of the transition slope where the magnitude equals the minima in the 
%	pass band ripple.
%
%	Hs = HS_CHEBY(filterOrder,passBandRipple_dB,cutOffFrequency) returns the
%	output parameters for the specified denormalized cutoff frequency.
%
%	Hs = HS_CHEBY(filterOrder,passBandRipple_dB,cutOffFrequency,freqNormMode)
%	with freqNormMode 0 returns the same output as in the previous description. 
%	For freqNormMode 1, the cutoff frequency is defined to be at the -3 dB 
%	magnitude level.
%
%	See also HS_BUTTER, HS_INVCHEBY, HS_CAUER, HS_CAUER_BIREC, HS_VLACH.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003 ...


if (nargin == 2)
	cutOffFrequency = 1;
	freqNormMode    = 0;
elseif (nargin == 3)
	freqNormMode    = 0;
end

e = sqrt( 10 ^ (passBandRipple_dB/10) -1 );
a = asinh(1/e) / filterOrder;
oddFilterOrder = ( mod(filterOrder,2) == 1 );

% reserve space and preset to 0
allRoots = zeros( filterOrder, 1 );

% calculate all complex roots
nComplexRoots = 2*floor( filterOrder / 2 );
phi = (1:2:nComplexRoots-1)*pi / (2*filterOrder);
sinha = sinh( a );
[realPartOfRoots,ix] = sort( sinha * sin(phi) );
imagPartOfRoots = cosh( a ) * cos(phi(ix));
allRoots(1:2:nComplexRoots) = -realPartOfRoots + j*imagPartOfRoots;
allRoots(2:2:nComplexRoots) = -realPartOfRoots - j*imagPartOfRoots;
if oddFilterOrder
	allRoots(end) = -sinha;
end

% remember the cut-off frequency and the frequency normalization mode 
% and normalize so that f(s) = 1
if ( freqNormMode == 0 )
	Kw = cutOffFrequency;
else
	Kw = cutOffFrequency / cosh( acosh(1/e)/filterOrder );
end
% also, re-order the roots to facilitate their use in lwdf-design
roots_gs =  Kw * flipud(allRoots);
% to keep f(s) = 1, we have to adjust g(s)
fs1 = real( prod(-roots_gs) );
if ~oddFilterOrder
	fs1 = fs1 / ( 10 ^ (passBandRipple_dB/20) );
end
poly_gs = real( poly(roots_gs) );

% return the answers in a structure
Hs.poly_fs  = fs1;
Hs.poly_gs  = poly_gs;
Hs.ident    = [ 'LP PROTOTYPE: ''cheby'',' num2str(filterOrder) ',' num2str(passBandRipple_dB) ...
							',' num2str(cutOffFrequency) ',' num2str(freqNormMode) ];
Hs.roots_fs = [];
Hs.roots_gs = roots_gs;
