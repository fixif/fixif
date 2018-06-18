function BpLadder = nladder2bp(NlpLadder,centerFrequency,BandWidth)
%NLADDER2BP	 Transform normalized lowpass ladder circuit into bandpass ladder
%	BpLadder = NLADDER2BP(NlpLadder,centerFrequency,BandWidth)
%	transforms the elements of normalized lowpass ladder circuits to
%	obtain bandpass ladder circuits with bandWidth around centerFrequency.
%	NlpLadder, as well as BpLadder are MATLAB structures:
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
%	The bandpass elements-string adds the elements:
%		'P' for a parallel resonator LC-circuit in a shunt arm, 
%		's' for a serial resonator LC-circuit in a series arm.
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	In case two or more resonator circuits are present in the NlpLadder, say 
%	representing frequencies f1 and f2, xxLadder.values may contain several
%	columns, representing the various permutations of the frequencies 
%	(here column1: f1-f2 and column2: f2-f1).
%
%	See also  NLP_LADDER, NLADDER2LP, NLADDER2HP, NLADDER2BS, 
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

% transform to bandpass network, knowing that
% lowpass element    bandpass element(s)
%        l   changes into    s
%        C                   P
%        S                 S || S
%        p                 p + p
bpCodes = lpCodes;
bpCodes( bpCodes == 'l' ) = 's';
bpCodes( bpCodes == 'C' ) = 'P';
SIndex = find( bpCodes == 'S' );
for i = fliplr(SIndex)
	bpCodes = [ bpCodes(1:i) 'S' bpCodes(i+1:end) ];
end
pIndex = find( bpCodes == 'p' );
for i = fliplr(pIndex)
	bpCodes = [ bpCodes(1:i) 'p' bpCodes(i+1:end) ];
end
BpLadder.elements = bpCodes;

bpValues = zeros( 2*(length(bpCodes)-1), size(lpValues,2) );
% leave Rsource and Rload unchanged
bpValues(  1,:) = lpValues(  1,:);
bpValues(end,:) = lpValues(end,:);
% start from element next to Rsource
lpvalIx = 2;
bpvalIx = 2;

centerFreq2 = centerFrequency ^ 2;
for i = 2:length(lpCodes)-1
	switch( lpCodes(i) )
		case 'l'
			newL = lpValues(lpvalIx,:) / BandWidth;
			bpValues(bpvalIx  ,:) = newL;
			bpValues(bpvalIx+1,:) = 1 ./ (centerFreq2 * newL );
			lpvalIx = lpvalIx + 1;
			bpvalIx = bpvalIx + 2;
		case 'C'
			newC = lpValues(lpvalIx,:) / BandWidth;
			bpValues(bpvalIx  ,:) = 1 ./ (centerFreq2 * newC );
			bpValues(bpvalIx+1,:) = newC;
			lpvalIx = lpvalIx + 1;
			bpvalIx = bpvalIx + 2;
		case 'S'
			% from Christian & Eisenmann, pg. 9
			a  = centerFrequency / BandWidth;
			l0 = lpValues(lpvalIx,:);
			b  = sqrt( 1 + 4*a*a* l0 .* lpValues(lpvalIx+1,:) );
			k  = 2*a * l0 .* b;
			l1 = k ./ (b + 1);
			l2 = k ./ (b - 1);
			bpValues(bpvalIx  ,:) = l1 / centerFrequency;
			bpValues(bpvalIx+1,:) =  1 ./ (l2 * centerFrequency);
			bpValues(bpvalIx+2,:) = l2 / centerFrequency;
			bpValues(bpvalIx+3,:) =  1 ./ (l1 * centerFrequency);
			lpvalIx = lpvalIx + 2;
			bpvalIx = bpvalIx + 4;
		case 'p'
			% from Christian & Eisenmann, pg. 9
			a  = centerFrequency / BandWidth;
			c0 = lpValues(lpvalIx+1,:);
			b  = sqrt( 1 + 4*a*a* lpValues(lpvalIx,:) .* c0 );
			k  = 2*a * c0 .* b;
			c1 = k ./ (b + 1);
			c2 = k ./ (b - 1);
			bpValues(bpvalIx  ,:) =  1 ./ (c2 * centerFrequency);
			bpValues(bpvalIx+1,:) = c1 / centerFrequency;
			bpValues(bpvalIx+2,:) =  1 ./ (c1 * centerFrequency);
			bpValues(bpvalIx+3,:) = c2 / centerFrequency;
			lpvalIx = lpvalIx + 2;
			bpvalIx = bpvalIx + 4;
	end
end
BpLadder.values = bpValues;
