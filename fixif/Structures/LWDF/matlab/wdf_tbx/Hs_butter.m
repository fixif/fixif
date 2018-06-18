function Hs = Hs_butter(filterOrder,cutOffFrequency)
%HS_BUTTER  Returns H(s) and its roots for a Butterworth lowpass filter
%	Hs = HS_BUTTER(filterOrder) returns a structure Hs describing 
%	the continuous-time transfer function of a normalized 
%	(cutoff frequency = 1) Butterworth approximation of the ideal 
%	lowpass filter. 
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s (for the Butterworth filter, poly_fs = 1.0). 
%	The length of the vector poly_gs equals the filterOrder +1. 
%	By default the cutoff frequency is normalized to equal 1.0 at that 
%	point of the transition slope where the magnitude level equals -3dB.
%
%	Hs = HS_BUTTER(filterOrder,cutOffFrequency) returns the output 
%	parameters for the specified denormalized cutoff frequency.
%
%	See also HS_CHEBY, HS_INVCHEBY, HS_CAUER, HS_CAUER_BIREC, HS_VLACH.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003 ...


if (nargin < 2)
	cutOffFrequency = 1;
end

% reserve space and preset to -1 (value of single real root)
allRoots = -ones( filterOrder, 1 );

% calculate all complex roots
nComplexRoots = 2*floor( filterOrder / 2 );
phi = (1:2:nComplexRoots-1)*pi / (2*filterOrder);
[realPartOfRoots,ix] = sort( sin(phi) );
imagPartOfRoots = cos(phi(ix));
allRoots(1:2:nComplexRoots) = -realPartOfRoots + j*imagPartOfRoots;
allRoots(2:2:nComplexRoots) = -realPartOfRoots - j*imagPartOfRoots;
% in case of an odd filter order the last single root remains -1

% remember the cut-off frequency and normalize so that f(s) = 1
% also, re-order the roots to facilitate their use in lwdf-design
roots_gs = cutOffFrequency * flipud(allRoots);
poly_gs  = real( poly( roots_gs ) ) / (cutOffFrequency ^ filterOrder);

% return the answers in a structure
Hs.poly_fs  = 1.0;
Hs.poly_gs  = poly_gs;
Hs.ident    = [ 'LP PROTOTYPE: ''butter'',' num2str(filterOrder) ',' num2str(cutOffFrequency) ];
Hs.roots_fs = [];
Hs.roots_gs = roots_gs;
