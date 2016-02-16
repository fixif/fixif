function HsBS = nlp2bs(Hs,centerFrequency,bandWidth)
%NLP2BS	  Normalized lowpass to bandstop transformation
%	HsBS = NLP2BS(Hs,centerFrequency,bandWidth) transforms the description of 
%	the (normalized) lowpass transfer function Hs to the bandstop transfer 
%	function HsBS with centerFrequency and bandWidth, where
%	bandWidth = f2-f1  and  centerFrequency = sqrt(f1*f2).
%	The transformation formula used is:
%
%	                 /          \
%   	            |     s      |
%	   S_nlp =>  BW | ---------- |   with Fc = centerFrequency, BW = bandWidth
%	                |   2     2  |
%   	             \ s  + Fc  /
%
%	See also NLP2LP, NLP2HP, NLP2BP.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004


if iscell( Hs.poly_fs )		% poly_fs contains Unit Elements info
	error( 'Transformation not possible for designs containing Unit Elements ...' );
end

poly_fs = Hs.poly_fs;
poly_gs = Hs.poly_gs;
centerFrequency2 = centerFrequency ^ 2;
halfBandWidth    = bandWidth / 2;

% do the lowpass to bandstop transformation
degreeFs   = length(poly_fs) -1;
degreeGs   = length(poly_gs) -1;
roots_fsBS = lfLp2Bs( Hs.roots_fs, centerFrequency2, halfBandWidth );
degreeDiff = degreeGs - degreeFs;
% terms (s^2 + fc^2) ^(n-m)
mulFacs    = centerFrequency .^ (0:2:2*degreeDiff);
coeffs     = mulFacs .* diag( fliplr( pascal(degreeDiff+1) ) )';
convPoly   = zeros( 1,2*length(coeffs)-1 );
convPoly(1:2:end) = coeffs;
% Hs.poly_fs(end)/Hs.poly_gs(end) gives us the attenuation at zero frequency 
poly_fsBS  = poly_fs(end)/poly_gs(end) * conv( convPoly, poly(roots_fsBS) );

roots_gsBS = lfLp2Bs( Hs.roots_gs, centerFrequency2, halfBandWidth );
poly_gsBS  = poly(roots_gsBS);

HsBS.poly_fs  = poly_fsBS;
HsBS.poly_gs  = poly_gsBS;
HsBS.ident    = Hs.ident;
HsBS.roots_fs = cplxpair( roots(poly_fsBS) );
HsBS.roots_gs = cplxpair( roots_gsBS );


%====================================================================================
%======  Local functions  ===========================================================
%====================================================================================

function bsRoots = lfLp2Bs(lpRoots,w02,BWd2)
  tmp = BWd2 ./ lpRoots;
  % NOTE: for certain combinations of w02 and BWd2 the sqrt-argument can
  % become negative, so the 'imaginary'-part becomes real: in that case 
  % we can't work with conjugated complex values, so we need the next code
  bsRoots = [ tmp + j*sqrt(w02 - tmp.^2);  tmp - j*sqrt(w02 - tmp.^2) ];
  