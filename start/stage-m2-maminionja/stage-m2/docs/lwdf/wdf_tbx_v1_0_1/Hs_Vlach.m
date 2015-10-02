function [Hs,wp] = Hs_vlach(N,rp,wn,ws,nUnitElements,freqNormMode)
%HS_VLACH	Vlach/Sharpe type lowpass filter design, with a free choice of
%			the number (limited by the filter order) and the frequencies
%			of zeros in the stopband and additional Unit Elements.
%
%	Hs = HS_VLACH(filterOrder,passBandRipple_dB)
%	returns a structure Hs describing the continuous-time normalized 
%	(cutoff frequency = 1) Vlach approximation of the ideal lowpass 
%	filter, given the specified parameters. 
%	Note that without stopBandZeros and/or Unit Elements, the Vlach
%	approximation completely equals the Chebyshev apparoximation.
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s.
%
%	[Hs,wp] = HS_VLACH(filterOrder,passBandRipple_dB)
%	additionally returns the frequencies of the peaks in the passband.
%
%	[..] = HS_VLACH(filterOrder,passBandRipple_dB,cutOffFrequency) returns the
%	output parameters for the specified denormalized cutoff frequency.
%
%	[..] = HS_VLACH(filterOrder,passBandRipple_dB, ...
%											cutOffFrequency,stopBandZeros)
%   Here, stopBandZeros is a scalar or a vector giving frequencies of 
%	transmission zeros in the stopband, in which
%	- every stopBandZero frequency is internally treated as two imaginary conjugate 
%	frequency points,
%	- transmission zeros in infinity should be left out.
%
%	[..] = HS_VLACH(filterOrder,passBandRipple_dB,cutOffFrequency, ...
%											stopBandZeros,nUnitElements)
%	adds nUnitElements Unit Elements to the design. Each Unit Element contibutes 
%	to the transfer function, by increasing the order of the approximation of 
%	the passband and increasing the attenuation in the stopband by up to 7.7 dB.
%	With Unit Elements present, poly_fs cannot be written as a common
%	polynomial any more, so	poly_fs and roots_fs are extended to cell arrays: 
%		Hs.poly_fs  ==> { poly_fs  without UEs; number of UEs }.
%		Hs.roots_fs ==> { roots_fs without UEs; number of UEs }.
%
%	[..] = HS_VLACH(filterOrder,passBandRipple_dB,cutOffFrequency, ...
%				 			   stopBandZeros,nUnitElements,freqNormMode) 
%	with freqNormMode 0 returns the same output as in the previous descriptions. 
%	For freqNormMode 1, the cutoff frequency is defined to be at the -3 dB 
%	magnitude level.
%
%	See also HS_BUTTER, HS_CHEBY, HS_INVCHEBY, HS_CAUER, HS_CAUER_BIREC, HS_BPVLACH.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, October 2003 ...
