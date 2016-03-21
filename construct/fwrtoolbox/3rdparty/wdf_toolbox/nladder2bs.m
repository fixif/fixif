function BsLadder = nladder2bs(NlpLadder,centerFrequency,BandWidth)
%NLADDER2BS	 Transform normalized lowpass ladder circuit into bandstop ladder
%	BsLadder = NLADDER2BS(NlpLadder,centerFrequency,BandWidth)
%	transforms the elements of normalized lowpass ladder circuits to
%	obtain bandstop ladder circuits with bandWidth around centerFrequency.
%	NlpLadder, as well as BsLadder are MATLAB structures:
%		xxLadder.elements		-- a string describing the ladder
%		xxLadder.values      	-- a (set of) column vector(s) with the 
%								   element values
%	The lowpass elements-string may consist of the following elements:
%		'r' for the source resistance, 'R' for the load resistance,
%		'l' for an inductor in a series arm,
%		'C' for a capacitor in a shunt arm, 
%		'p' for a parallel resonator LC-circuit in a series arm, 
%		'S' for a serial resonator LC-circuit in a shunt arm.
%	NOTE: Unit Elements, denoted by a 'U', are NOT ALLOWED here.
%	The bandstop elements-string will contain only 'r','R','p's and 'S's.
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	In case two or more resonator circuits are present in the NlpLadder, say 
%	representing frequencies f1 and f2, xxLadder.values may contain several
%	columns, representing the various permutations of the frequencies 
%	(here column1: f1-f2 and column2: f2-f1).
%
%	See also  NLP_LADDER, NLADDER2LP, NLADDER2HP, NLADDER2BP, 
%             LADDERSYNTHESIS, SHOWLADDER.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004.


lpCodes  = NlpLadder.elements;
lpValues = NlpLadder.values;
if any( lpCodes == 'U' )
	error( 'Transformation not possible for circuits containing Unit Elements ...' );
end
if ~( isempty( find(lpCodes == 's') ) && isempty( find(lpCodes == 'P') ) )
	error( 'Is this really a LOW pass filter ...?' );
end

% transform to bandstop network, knowing that
% lowpass element    bandstop element(s)
%        l   changes into    p
%        C                   S
%        S                 S || S
%        p                 p + p
% Note to use correct sequence when changing codes
bsCodes = lpCodes;
SIndex = find( bsCodes == 'S' );
for i = fliplr(SIndex)
	bsCodes = [ bsCodes(1:i) 'S' bsCodes(i+1:end) ];
end
pIndex = find( bsCodes == 'p' );
for i = fliplr(pIndex)
	bsCodes = [ bsCodes(1:i) 'p' bsCodes(i+1:end) ];
end
bsCodes( bsCodes == 'l' ) = 'p';
bsCodes( bsCodes == 'C' ) = 'S';
BsLadder.elements = bsCodes;

bsValues = zeros( 2*(length(bsCodes)-1), size(lpValues,2) );
% just copy Rsource and Rload
bsValues(  1,:) = lpValues(  1,:);
bsValues(end,:) = lpValues(end,:);
% start from element next to Rsource
lpvalIx = 2;
bsvalIx = 2;

centerFreq2 = centerFrequency ^ 2;
for i = 2:length(lpCodes)-1
	switch( lpCodes(i) )
		case 'l'
			newC = 1 ./ ( BandWidth * lpValues(lpvalIx,:) ); 
			bsValues(bsvalIx  ,:) = 1 ./ ( centerFreq2 * newC );
			bsValues(bsvalIx+1,:) = newC;
			lpvalIx = lpvalIx + 1;
			bsvalIx = bsvalIx + 2;
		case 'C'
			newL = 1 ./ ( BandWidth * lpValues(lpvalIx,:) ); 
			bsValues(bsvalIx  ,:) = newL;
			bsValues(bsvalIx+1,:) = 1 ./ ( centerFreq2 * newL );
			lpvalIx = lpvalIx + 1;
			bsvalIx = bsvalIx + 2;
		case 'S'
			% from Christian & Eisenmann, pg. 9
			a  = centerFrequency / BandWidth;
			c0 = lpValues(lpvalIx+1,:);
			b  = sqrt( 1 + 4*a*a ./ ( lpValues(lpvalIx,:) .* c0 ) );
			k  = 2*a * b ./ c0;
			l1 = k ./ (b + 1);
			l2 = k ./ (b - 1);
			bsValues(bsvalIx  ,:) = l1 / centerFrequency;
			bsValues(bsvalIx+1,:) =  1 ./ (l2 * centerFrequency);
			bsValues(bsvalIx+2,:) = l2 / centerFrequency;
			bsValues(bsvalIx+3,:) =  1 ./ (l1 * centerFrequency);
			lpvalIx = lpvalIx + 2;
			bsvalIx = bsvalIx + 4;
		case 'p'
			% from Christian & Eisenmann, pg. 9
			a  = centerFrequency / BandWidth;
			l0 = lpValues(lpvalIx,:);
			b  = sqrt( 1 + 4*a*a ./ ( l0 .* lpValues(lpvalIx+1,:) ) );
			k  = 2*a * b ./ l0;
			c1 = k ./ (b + 1);
			c2 = k ./ (b - 1);
			bsValues(bsvalIx  ,:) =  1 ./ (c2 * centerFrequency);
			bsValues(bsvalIx+1,:) = c1 / centerFrequency;
			bsValues(bsvalIx+2,:) =  1 ./ (c1 * centerFrequency);
			bsValues(bsvalIx+3,:) = c2 / centerFrequency;
			lpvalIx = lpvalIx + 2;
			bsvalIx = bsvalIx + 4;
	end
end
BsLadder.values = bsValues;
