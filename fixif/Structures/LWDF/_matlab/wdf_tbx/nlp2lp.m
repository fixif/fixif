function HsLP = nlp2lp(Hs,cutOffFrequency)
%NLP2LP	  Normalized lowpass to lowpass transformation
%	HsLP = NLP2LP(Hs,cutOffFrequency) transforms the description of 
%	the (normalized) lowpass transfer function Hs to the lowpass transfer 
%	function HsLP with cutoff frequency cutOffFrequency.
%	The transformation formula used is:
%
%   	           s
%		S_nlp => ----   with Fc = cutOffFrequency
%   	          Fc
%
%	See also NLP2HP, NLP2BP, NLP2BS.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004


if iscell( Hs.poly_fs )		% poly_fs contains Unit Elements info
	error( 'Transformation not possible for designs containing Unit Elements ...' );
end

poly_fs  = Hs.poly_fs;
poly_gs  = Hs.poly_gs;
poly_fs  = ( cutOffFrequency .^ -(length(poly_fs)-1:-1:0) ) .* (poly_fs(:))';
poly_gs  = ( cutOffFrequency .^ -(length(poly_gs)-1:-1:0) ) .* (poly_gs(:))';

HsLP.poly_fs  = poly_fs / poly_gs(1);
HsLP.poly_gs  = poly_gs / poly_gs(1);
HsLP.ident    = Hs.ident;
HsLP.roots_fs = cutOffFrequency * Hs.roots_fs;
HsLP.roots_gs = cutOffFrequency * Hs.roots_gs;
