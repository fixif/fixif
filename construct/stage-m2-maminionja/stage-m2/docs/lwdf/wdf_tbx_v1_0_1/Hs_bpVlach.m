function Hs = Hs_bpVlach(N,rp,wLwH,ws,nUnitElements,freqNormMode)
%HS_BPVLACH		Vlach type bandpass filter design, with a free choice of
%				zeros frequencies in the stopbands (limited by filterOrder)
%				and additional Unit Elements.
%
%	Hs = HS_BPVLACH(filterOrder,passBandRipple_dB,cutOffFrequencies, ...
%																stopBandZeros)
%	returns a structure Hs describing the continuous-time Vlach approximation 
%	of an ideal bandpass filter, given the specified parameters. 
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s.
%	cutOffFrequencies is expected to be a two element vector, defining resp.
%	the lower and the upper cut-off frequency.
%	With stopBandZeros, transmission zeros outside the passband can be defined.
%	Here, every non-zero frequency value is treated as two conjugated imaginary
%	transmission zeros. Zero values each mean a single transmission zero at 
%	zero frequency. The total number of transmission zeros should be less than
% 	the (EVEN) cutOffFrequency (stopBandZeros can be an empty vector).
%
%	Hs = HS_BPVLACH(filterOrder,passBandRipple_dB,cutOffFrequencies, ...
%													stopBandZeros,nUnitElements)
%	adds nUnitElements Unit Elements to the design. Each Unit Element contributes 
%	to the transfer function, by increasing the order of the approximation of 
%	the passband and increasing the attenuation in the stopband by up to 7.7 dB.
%	With Unit Elements present, poly_gs cannot be written as a common
%	polynomial any more, so	poly_fs and roots_fs are extended to cell arrays: 
%		Hs.poly_fs  ==> { poly_fs  without UEs; number of UEs }.
%		Hs.roots_fs ==> { roots_fs without UEs; number of UEs }.
%	The sum of filterOrder and nUnitElements should be EVEN, and less than the
%	total number of transmission zeros.
%
%	Hs = HS_BPVLACH(filterOrder,passBandRipple_dB,cutOffFrequencies, ...
%										stopBandZeros,nUnitElements,freqNormMode)
%	with freqNormMode 0 returns the same output as in the previous descriptions. 
%	For freqNormMode 1, the cutoff frequencies are defined to be at the -3 dB 
%	magnitude level.
%
%	Example:
%		Hs = Hs_bpVlach(6,1,fz2fs([0.13 0.17]),fz2fs([0 0.1 0.2]),0,0);
%		plotHz( LWDF2Hz(Hs2LWDF(Hs)) ,1,2 );
%
%	See also HS_BUTTER, HS_CHEBY, HS_INVCHEBY, HS_CAUER, HS_CAUER_BIREC, HS_VLACH,
%			 NLP2BP, NLADDER2BP.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, October 2003 ...
