function HsHP = nlp2hp(Hs,cutOffFrequency)
%NLP2HP	  Normalized lowpass to highpass transformation
%	HsHP = NLP2HP(Hs,cutOffFrequency) transforms the description of 
%	the (normalized) lowpass transfer function Hs to the highpass transfer 
%	function HsHP with cutoff frequency cutOffFrequency.
%	The transformation formula used is:
%
%   	          Fc
%		S_nlp => ----   with Fc = cutOffFrequency
%   	          s
%
%	See also NLP2LP, NLP2BP, NLP2BS.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004


if iscell( Hs.poly_fs )		% poly_fs contains Unit Elements info
	error( 'Transformation not possible for designs containing Unit Elements ...' );
end

poly_fs     = Hs.poly_fs;
poly_gs     = Hs.poly_gs;
degreeFs = length(poly_fs) -1;
degreeGs = length(poly_gs) -1;
if ( degreeFs > degreeGs )
	error( 'Degrees Hs.poly_fs and Hs.poly_gs not realistic ...' );
end
mulFacs = cutOffFrequency .^ (0:degreeGs);
poly_fs = [ fliplr(poly_fs) zeros(1,degreeGs-degreeFs) ] .* mulFacs;
poly_gs = fliplr(poly_gs) .* mulFacs;

HsHP.poly_fs  = poly_fs / poly_gs(1);
HsHP.poly_gs  = poly_gs / poly_gs(1);
HsHP.ident    = Hs.ident;
HsHP.roots_fs = sort( roots( poly_fs ) );
HsHP.roots_gs = sort( roots( poly_gs ) );