function LpLadder = nladder2lp(NlpLadder,cutOffFrequency)
%NLADDER2LP	Normalized lowpass ladder circuit to denormalized lowpass ladder
%	LpLadder = NLADDER2LP(NlpLadder,cutOffFrequency)
%	recalculates the element values of normalized lowpass ladder circuits
%	to obtain ladder circuits with cutoff frequency cutOffFrequency.
%	NlpLadder, as well as LpLadder are MATLAB structures:
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
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	In case two or more resonators are present, say representing frequencies
%	f1 and f2, xxLadder.values may contain more columns, representing the
%	various permutations of the frequencies (here column1: f1-f2 and 
%	column2: f2-f1).
%
%	See also  NLP_LADDER, NLADDER2HP, NLADDER2BP, NLADDER2BS, 
%             LADDERSYNTHESIS, SHOWLADDER.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004.


elements = NlpLadder.elements;
if any( elements == 'U' )
	error( 'Transformation not possible for circuits containing Unit Elements ...' );
end
if ~( isempty( find(elements == 's') ) && isempty( find(elements == 'P') ) )
	error( 'Is this really a LOW pass filter ...?' );
end
% the circuit toplology doesn't change with this transformation
LpLadder.elements = elements;

elValues = NlpLadder.values;
% assume columns with Rsource as first and Rload as last row
% don't alter Rsource or Rload
elValues(2:end-1,:) = elValues(2:end-1,:) / cutOffFrequency;
LpLadder.values = elValues;