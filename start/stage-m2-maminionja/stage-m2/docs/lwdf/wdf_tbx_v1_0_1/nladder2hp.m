function HpLadder = nladder2hp(NlpLadder,cutOffFrequency)
%NLADDER2HP	 Transform normalized lowpass ladder circuit into highpass ladder
%	HpLadder = NLADDER2HP(NlpLadder,cutOffFrequency)
%	transforms the elements of normalized lowpass ladder circuits to
%	obtain high pass ladder circuits with cutoff frequency cutOffFrequency.
%	NlpLadder, as well as HpLadder are MATLAB structures:
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
%	The highpass elements-string adds the elements:
%		'L' for an inductor in a shunt arm,
%		'c' for a capacitor in a series arm. 
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	In case two or more resonators are present, say representing frequencies
%	f1 and f2, xxLadder.values may contain more columns, representing the
%	various permutations of the frequencies (here column1: f1-f2 and 
%	column2: f2-f1).
%
%	See also  NLP_LADDER, NLADDER2LP, NLADDER2BP, NLADDER2BS, 
%             LADDERSYNTHESIS, SHOWLADDER.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004.


elCodes = NlpLadder.elements;
if any( elCodes == 'U' )
	error( 'Transformation not possible for circuits containing Unit Elements ...' );
end
if ~( isempty( find(elCodes == 's') ) && isempty( find(elCodes == 'P') ) )
	error( 'Is this really a LOW pass filter ...?' );
end
% all capacitors change into inductors and all inductors change into capacitors
% only single elements do change place, resonators remain in place
elCodes( elCodes == 'l' ) = 'c';
elCodes( elCodes == 'C' ) = 'L';
HpLadder.elements = elCodes;

elValues = NlpLadder.values;
% assume columns with Rsource as first and Rload as last row
% don't alter Rsource or Rload
elValues(2:end-1,:) = 1 ./ ( elValues(2:end-1,:) * cutOffFrequency );
% So, capacitors change into inductors and vice versa
% but with resonators, we had the rule that first the inductor value was
% listed and the capacitor value thereafter, so we have to do a little switching
switchStr = upper( elCodes );
iSwitch   = find( (switchStr == 'S') | (switchStr == 'P' ) );
if ~isempty( iSwitch )
	iSwitch   = iSwitch + (0:length(iSwitch)-1);
	% switch indices found
	tmpValues             = elValues(iSwitch,:);
	elValues(iSwitch,: )  = elValues(iSwitch+1,:);
	elValues(iSwitch+1,:) = tmpValues;
end
HpLadder.values = elValues;