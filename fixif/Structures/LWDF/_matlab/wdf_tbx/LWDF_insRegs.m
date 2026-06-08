function [LWDF,Hz] = LWDF_insRegs(LWDF,regsVec)
%LWDF_INSREGS	Insert pipeline registers between the slices of an LWDF.
%	LWDF = LWDF_INSREGS(LWDF,regsVec) is used to insert pipeline registers
%	between the slices of a previously calculated LWDF structure.
%	At input, LWDF should be a structure that contains the fields
%		LWDF.wdaCodes
%		LWDF.gamma,
%	while the output LWDF will be extended with the field LWDF.insRegs.
%	This field is a copy of the regsVec input, which should be a vector of 
%	ones and zeros which specify where to insert the registers: a one means
%	that a registers should be inserted at the appropriate place, both in 
%	the top and bottom rows.
%
%	[LWDF,Hz] = LWDF_INSREGS(LWDF,regsVec) additionally returns the resulting
%	discrete-time magnitude transfer function Hz.
%
%	See also HS2LWDF, SHOWLWDF.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, October 2005

wdaCodes    = LWDF.wdaCodes;
nSlices     = size(wdaCodes,2);
maxRegPairs = nSlices -1;
nRegPairs   = length(regsVec);
if ( nRegPairs > maxRegPairs )
	wdaCodes
	error( 'Only %d register-pairs may be inserted ...', maxRegPairs );
elseif ( nRegPairs < maxRegPairs )
	regsVec = [ regsVec zeros(maxRegPairs-nRegPairs) ];
end

LWDF.insRegs = regsVec;
if ( nargout == 2 )
	nRegs = sum( regsVec == 1 );
	Hz = lwdf2Hz(LWDF);
	Hz(1).poly_fz = [ zeros(1,nRegs) Hz(1).poly_fz ];
	Hz(2).poly_fz = [ zeros(1,nRegs) Hz(2).poly_fz ];
end
