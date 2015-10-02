function [magn_dB,freq] = ladder2Magn(Ladder,freqInfo,figNo)
%LADDER2MAGN   Reconstruct the magnitude plot for a given ladder filter 
%	magn_dB = LADDER2MAGN(Ladder) computes the	magnitude transfer function
%	from the ladder structure described in Ladder, where Ladder should
%	contain the fields  
%		Ladder.elements		-- a string describing the ladder
%		Ladder.values      	-- a (set of) column vector(s) with the 
%								   element values
%	The elements-string may consist of the following elements:
%		'r' for the source resistance, 'R' for the load resistance,
%		'l' or 'L' for an inductor, 'c' or 'C' for a capacitor, 
%		's' or 'S' for a serial resonator LC-circuit and 
%		'p' or 'P' for a parallel resonance LC-circuit.
%	The lowercase notation is used to identify elements in series arms,
%	while the uppercase is used for elements in shunt arms.
%	Moreover, also Unit Elements can be present, denoted by a 'U'.
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	NOTE: if multiple columns are present in Ladder.values, the FIRST ONE ONLY 
%		  is selected to compute the magnitude transfer function.
%
%	[magn_dB,freq] = LADDER2MAGN(Ladder) also returns a vector freq 
%	respresenting the frequency points for which the transfer function 
%	has been evaluated. Default is 1000 points in the range 1e-10 to 5. 
%
%	... = LADDER2MAGN(Ladder,freqInfo) uses the parameters freqInfo to 
%	judge what to do: if freqInfo is a scalar, it just specifies the number 
%	of frequency point to be used, given the same frequency range as above.
%	If freqInfo is a vector, this data is interpreted as the frequencies
%	to be used for the evaluation.
%
%	... = LADDER2MAGN(Ladder,freqInfo,figNo)
% 	If figNo is 0, no plot will be made. If figNo is 1 or is left out, a plot
%	will be made in figure(1), otherwise figure(figNo) will be drawn.
%
%	See also NLP_LADDER, NLADDER2LP, NLADDER2HP, NLADDER2BP, NLADDER2BS.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, November 2003.
%                                     December 2003, also handle Unit Elements.
% NOTE: this program uses more code than strictly necessary to lower 
%		the execution time needed.

elCodes  = Ladder.elements;
elValues = Ladder.values(:,1);		% only first configuration
if any( elValues <= 0 )
	error( 'Negative element values present. No reconstruction ...' );
end

if ( nargin < 3 ),  figNo = 1;       end
if ( nargin >= 2 )
	if ( length(freqInfo) == 1 )
		nFreqPoints = freqInfo;
	else
		omega       = freqInfo;
		nFreqPoints = length( omega );
	end
else
	nFreqPoints = 1000;
end
if ~exist( 'omega','var' )
	omega = linspace(1e-10,5,nFreqPoints);
end


filterOrder = length(elCodes) -2;     % minus Rsource and Rload
Rsource     = elValues(1);
Rload       = elValues(end);
% first determine the number of nodes in the circuit
% elCodes >= 'a'  means lowercase selected (== series arms)
nNodes  = sum( elCodes(2:end) >= 'a' ) + sum( elCodes == 'U' ) + 1;
j_omega = j*omega;
% initialize the I and V vectors
Vvec = zeros(nNodes,nFreqPoints);
Ivec = [ 1; zeros(nNodes-1,1) ];
% compute the voltage on all nodes by calculating 
% V = inv(Y)*I for each frequency point
for n = 1:nFreqPoints

	jw   = j_omega(n);
	Ymat = zeros(nNodes);
	% start with Rsource = 1
	Ymat(1,1) = 1/Rsource;
	% fill the Ymatrix for this frequency		
	ix    = 2;
	iNode = 1;
	for i = 1:filterOrder
		switch elCodes(i+1)
			case 'l'
				Yl = 1/(jw*elValues(ix));
				iNode2 = iNode +1;
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + Yl;
				Ymat(iNode2,iNode2) =  Yl;
				Ymat(iNode, iNode2) = -Yl;
				Ymat(iNode2,iNode ) = -Yl;
				iNode = iNode2;
			case 'L'
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + 1/(jw*elValues(ix));
			case 'c'
				Yc = jw*elValues(ix);
				iNode2 = iNode +1;
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + Yc;
				Ymat(iNode2,iNode2) =  Yc;
				Ymat(iNode, iNode2) = -Yc;
				Ymat(iNode2,iNode ) = -Yc;
				iNode = iNode2;
			case 'C'
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + jw*elValues(ix);
			case 's'
				w  = omega(n);
				Ys = jw*elValues(ix+1) / ( 1 - w*w*elValues(ix)*elValues(ix+1) );
				iNode2 = iNode +1;
				Ymat(iNode, iNode ) = Ymat(iNode,iNode)   + Ys;
				Ymat(iNode2,iNode2) =  Ys;
				Ymat(iNode, iNode2) = -Ys;
				Ymat(iNode2,iNode ) = -Ys;
				iNode = iNode2;
				ix    = ix +1;
			case 'S'
				w  = omega(n);
				YS = jw*elValues(ix+1) / ( 1 - w*w*elValues(ix)*elValues(ix+1) );
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + YS;
				ix = ix +1;
			case 'p'
				Yp = 1/(jw*elValues(ix)) + jw*elValues(ix+1);
				iNode2 = iNode +1;
				Ymat(iNode, iNode ) = Ymat(iNode,iNode)   + Yp;
				Ymat(iNode2,iNode2) =  Yp;
				Ymat(iNode, iNode2) = -Yp;
				Ymat(iNode2,iNode ) = -Yp;
				iNode = iNode2;
				ix    = ix +1;
			case 'P'
				YP = 1/(jw*elValues(ix)) + jw*elValues(ix+1);
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + YP;
				ix = ix +1;
			case 'U'
				YU = 1/(jw*elValues(ix));
				iNode2 = iNode +1;
				Ymat(iNode, iNode ) = Ymat(iNode, iNode ) + YU;
				Ymat(iNode2,iNode2) = YU;
				w = omega(n);
				YUmutual = -sqrt(w*w + 1) * YU; 
				Ymat(iNode, iNode2) = YUmutual;
				Ymat(iNode2,iNode ) = YUmutual;
				iNode = iNode2;
		end
		ix = ix +1;
	end	% for i = ...	
	% always treat last node seperately
	Ymat(iNode,iNode) = Ymat(iNode,iNode) + 1/Rload;
	% compute the V vector
	Vvec(:,n) = inv(Ymat) * Ivec;

end  % n, nFreqPoints

if ( rem(filterOrder,2) == 1 )	% odd filterOrder
	refLvl = 20*log10( (1+Rload)/Rload );
else
	refLvl = 10*log10(4/Rload);
end
magn = refLvl + 20*log10( abs( Vvec(end,:) ) );

% check to see whether a plot is wanted
if ( figNo ~= 0 )
	figure( figNo )
	plot( omega,magn, 'linewidth',2);
	axis( [xlim -80 10 ]);
	grid on  
	title( 'Transfer function reconstructed from ladder topology' );
	xlabel( 'Frequency' );
	ylabel( 'Magnitude in dB' );
end
% return the correct number of parameters
if ( nargout == 1 )
	magn_dB = magn;
else
	magn_dB = magn;
	freq    = omega;
end

