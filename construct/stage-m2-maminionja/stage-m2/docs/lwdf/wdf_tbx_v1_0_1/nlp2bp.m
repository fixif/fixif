function HsBP = nlp2bp(Hs,centerFrequency,bandWidth)
%NLP2BP	  Normalized lowpass to bandpass transformation
%	Hsbp = NLP2BP(Hs,centerFrequency,bandWidth) transforms the description of 
%	the (normalized) lowpass transfer function Hs to the bandpass transfer 
%	function HsBP with centerFrequency and bandWidth, where
%	bandWidth = f2-f1  and  centerFrequency = sqrt(f1*f2).
%	The transformation formula used is:
%
%	                  /  2     2 \
%   	          1  |  s  + Fc   |
%	   S_nlp => ----.| ---------- |   with Fc = centerFrequency, BW = bandWidth
%   	         BW   \    s     /
%
%	See also NLP2LP, NLP2HP, NLP2BS.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004


if iscell( Hs.poly_fs )		% poly_fs contains Unit Elements info
	error( 'Transformation not possible for designs containing Unit Elements ...' );
end

poly_fs = Hs.poly_fs;
poly_gs = Hs.poly_gs;
centerFrequency2 = centerFrequency ^ 2;
halfBandWidth    = bandWidth / 2;

% do the lowpass to bandpass transformation
roots_fsBP = lfLp2Bp( Hs.roots_fs, centerFrequency2, halfBandWidth );
degreeDiff = length(poly_gs) - length(poly_fs);
convPoly   = [ (bandWidth^degreeDiff)/(poly_gs(1)/poly_fs(1))  zeros(1,degreeDiff) ];
poly_fsBP  = conv( convPoly, poly(roots_fsBP) );
roots_fsBP = cplxpair( [ roots_fsBP; zeros(degreeDiff,1) ] );

roots_gsBP = lfLp2Bp( Hs.roots_gs, centerFrequency2, halfBandWidth );

HsBP.poly_fs  = poly_fsBP;
HsBP.poly_gs  = poly(roots_gsBP);
HsBP.ident    = Hs.ident;
HsBP.roots_fs = roots_fsBP;
HsBP.roots_gs = cplxpair( roots_gsBP );


%====================================================================================
%======  Local functions  ===========================================================
%====================================================================================

function bpRoots = lfLp2Bp(lpRoots,w02,BWd2)
  tmp = BWd2 * lpRoots;
  bpRoots = [ tmp + j*sqrt(w02 - tmp.^2); tmp - j*sqrt(w02 - tmp.^2) ];
