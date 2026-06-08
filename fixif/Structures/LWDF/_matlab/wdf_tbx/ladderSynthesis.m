function [elValues,result] = ladderSynthesis(InputYZ,Topology,stopBandZeroFrequencies)
%LADDERSYNTHESIS	Compute ladder element values given the input reactance function
%	elValues = LADDERSYNTHESIS(InputYZ,Topology) calculates the element values for
%	the given InputYZ and Topology, which has to describe a lowpass ladder filter. 
%	The input parameters are both structures, which should contain the fields
%		InputYZ.num, InputYZ.den
%	and
%		Topology.elTypeStr, Topology.ZorYStr.
%	InputYZ.num and InputYZ.den are polynomial descriptions of respectively the
%	numerator and the denominator of the input reactance function, which can be 
%	treated as either an impedance or an admittance function, depending on the 
%	first character of Topology.ZorYStr.
%	The polynomial descriptions list the coefficients of the polynomials in 
%	descending powers of s.
% 	Topology.elTypeStr and Topology.ZorYStr describe the element types of the 
%	ladder circuit and their interconnections. Recognized element types of
%	Topology.elTypeStr are:
%		'x'		-- an inductor or a capacitor,
%		'W'		-- a series or parallel resonance LC-circuit,
%		'U'		-- a Unit Element.
%	the last element should be an 'R' for the load resistance.
%	For each 'W'-type element (if present), a resonance frequency should be 
%	specified in the 3rd input argument (see below).
% 	The source resistance is always expected to be 1.0 Ohm.
%	Topology.ZorYStr is a string of 'Z' and 'Y' characters, with the same length 
%	as Topology.elTypeStr.
%	The returned elValues give the calculated values for the elements, preceded
%	by a 1.0 for the source resistance. 'W' types result in two elements, which
%	are listed in the sequence: [ ...; inductance; capacitance; ... ]
%	If the circuit turns out to be not realizable, all NaNs are returned.
%  	
%	[elValues,result] = LADDERSYNTHESIS(InputYZ,Topology) also returns
%	a result-flag, which is 1 in case the synthesis executed without errors,
%	or a 0 in case the circuit turns out to be not realizable.
%
%	[...] = LADDERSYNTHESIS(InputYZ,Topology,stopBandZeroFrequencies) uses
%	a third input parameter to specify the resonance freqencies of the 'W'-type
%	elements in Topology.elTypeStr (these are always located in the stopband).
%	
% 	See also  NLP_LADDER.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, February 2004.

% 	The choice which element actually results is determined by both
%	Topology.elTypeStr and Topology.ZorYStr, e.g.
%		'x', combined with 'Z' --> an inductor in a series arm,
%		'x', combined with 'Y' --> a capacitor in a shunt arm,
%		'W', combined with 'Z' --> a parallel resonator in a series arm,
%		'W', combined with 'Y' --> a series resonator in a shunt arm.
