function [WDF,fwdB,revB,allB] = ladder2WDF(Ladder,wdfType,impulseResponseLength,figNo)
%LADDER2WDF	  	Translate a ladder filter into a Wave Digital Filter structure.
%	WDF = LADDER2WDF(Ladder) translates the LC-ladder network Ladder into
%	an equivalent time-discrete Wave Digital Filter WDF containing only
%	three-port adaptors. 
%	The structure Ladder should contain the fields  
%		Ladder.elements		-- a string describing the ladder
%		Ladder.values      	-- a (set of) column vector(s) with the 
%								   element values
%	The elements-string may consist of the following elements:
%		'r' for the source resistance, 'R' for the load resistance,
%		'l' or 'L' for an inductor, 
%		'c' or 'C' for a capacitor, 
%		's' or 'S' for a serial resonator LC-circuit and 
%		'p' or 'P' for a parallel resonance LC-circuit.
%	The lowercase notation is used to identify elements in series arms,
%	while the uppercase is used for elements in shunt arms.
%	The values-vector should contain the values of the elements in the same 
%	sequence as given in the elements-string. A resonator circuit needs two 
%	values, where always the first one denotes the inductor value and the 
%	second one the capacitor value (See also NLP_LADDER).
%	NOTE: if multiple columns are present in Ladder.values, the FIRST ONE ONLY 
%		  is selected to compute the magnitude transfer function.
%	The returned WDF will be a structure containing the fields
%		WDF.wdaStruct
%		WDF.wdaNo
%		WDF.mulFacs 
% 	In here, WDFS.wdaStruct, described the WDF block diagram:
%	A WDF block diagram is represented with 2 strings, one describing the
%	adaptors in the signal path (bottom row), the second one (top row) 
%	describing the elements or adaptors connected to the serial or parallel 
%	ports of the first mentioned adaptors.
%	So, the bottom row can only consist of the following codes 
%		's' 	-- for a reflection free 3-port serial adaptor,
%		'p'		-- a reflection free 3-port parallel adaptor,
%		'S'		-- a 3-port serial adaptor with two coefficients,
%		'P'		-- a 3-port parallel adaptor with two coefficients,
%		'm'		-- an output invertor or scaling factor, if needed.
%	For all these adaptors, port 1 is the input, port 3 the output (to be 
%	reflection free, adapted to port 1 of the next in line adaptor), and 
%	port 2 the interface to the top row elements.
%	For all adaptors, port 2 is the interface to the top row elements.
%	Each element in the top row string is connected to port 2 of the
%	adaptor in the same position in the bottom row string. Possible
%	codes are:
%		'+'		-- a single delay element (translation of a capacitance),
%		'-'		-- a delay element in series with an inverter (inductance),
%		's' 	-- a reflection free serial adaptor (series LC resonator), 
%		'p'		-- a reflection free parallel adaptor (parallel LC resonator),
%		'x'		-- for an empty slot.
%	In case of the 's' and 'p' adaptors, their port 1 is connected to a single  
%	delay element (translation of the capacitance), port 2 to a delay element in 
%	series with an inverter (the inductance), while the reflection free port 3 
%	is connected to port 2 of the corresponding bottom row adaptor.  
%	WDF.wdaNo defines the numbering of the individual adaptors,
%	WDF.mulFacs lists the multiplication coefficients of the adaptors, starting
%	from adaptor 1. The very last adaptor, which is not reflection free, needs
%	two coefficients, while, if the bottom row string ends with an 'm', the last
%	value will be the scaling coefficient.   
%	Finally, the coefficients will be listed together with -unless deliberately
%	suppressed- a block diagram of the WDF-structure. 
%	Also the magnitude transfer functions for forward and reverse outputs are 
%	recalculated from the WDF-structure and the scattering matrices as has 
%	been found. Both transfer functions are showed in the top window of a 
%	two-figures plot. The bottom window shows the peak levels of the magnitude
%	transfer functions of each B-output port as bar diagrams.	
%
%	WDF = LADDER2WDF(Ladder,wdfType) can be used to choose among different
%	filter structures. wdfType can be:
%		'3p'	 : use only three-port adaptors (default, see above).
%		'2p'	 : use two-port adaptors for resonators in the top row.
%				   Top row codes are extended with
%					'S' -- a 2-port translation of a serial LC resonance circuit,
%					'P'	-- a 2-port translation of a parallel LC resonance circuit.
%		'3p_sym' : in case of an odd order of bottom-row adaptors and if the
%				   ladders shows a topological symmetry, a symmetric WDF structure
%                  using only three-ports will be constructed.
%				   For all these adaptors except the middle one, port 1 is the 
%				   input, port 3 the output (to be reflection free, adapted to 
%				   port 1 of the adaptor to its right if left from the middle, 
%				   or to port 1 of the adaptor at its left if right from the middle).
%				   The adaptor in the middle has port 1 connected to port 3 of its 
%				   left	neighbor and port 3 connected to port 3 of its right 
%				   neighbor.
%				   For all adaptors, port 2 is connected to the top row elements.
%		'2p_sym' : as '3p-sym', except for two-port adaptors for resonators in 
%				   the top row.
%
%	[WDF,fwdB] = LADDER2WDF(Ladder,wdfType) additionally returns the impulse   
%	response of the forward output.
%
%	[WDF,fwdB,revB] = LADDER2WDF(Ladder,wdfType) also returns the impulse  
%	response of the reflection or reverse output.
%
%	[WDF,fwdB,revB,allB] = LADDER2WDF(Ladder,wdfType) also returns all B-outputs
%	in a 3 column by 'numbers of adaptors' matrix form.
%
%	[...] = LADDER2WDF(Ladder,wdfType,impulseResponseLength) allows the user 
%	to specify the length of the impulse reponse that is used for calculating 
%	the frequency transfer function and the optionally returned response vectors. 
%	Default value is 512, but this value may be too low for narrowband 
%	bandpass/stop filters.
%
%	[...] = LADDER2WDF(Ladder,wdfType,impulseResponseLength,figNo) can be used 
%	to control the output plot. Use figNo = 0 if no output is wanted. 
%	When no figNo is specified, figure(1) will be used for plotting, 
%	otherwise figure(figNo). 
%
%	See also NLP_LADDER, SHOWWDF.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, October 2004,2005


elCodes  = Ladder.elements;
if ( any(elCodes == 'U') )
	error( 'Really not much sense to input a circuit containing Unit Elements ...' );
end
% if elValues happens to be an array, use the first column
elValues = Ladder.values(:,1);

if ~exist('wdfType','var')
	wdfType = '3p';
	fprintf( 'wdfType not specified : ''3p'' assumed ...\n' );
end	
switch wdfType
	case '2p'
		pref3p  = 0;
		prefSym = 0;
	case '3p'
		pref3p  = 1;
		prefSym = 0;
	case '2p_sym'
		pref3p  = 0;
		prefSym = 1;
	case '3p_sym'
		pref3p  = 1;
		prefSym = 1;
	otherwise
		error( 'Unknown wdfType ...' );
end

if ( prefSym == 1 )
	% test Ladder for being TOPOLOGICALLY symmetric
	if ( rem(length(elCodes),2) ~= 1 )
		error( 'There should be an odd number of arms for our definition of symmetry ...' );
	end
	symTestStr = elCodes(2:end-1);
	if ( length(symTestStr) < 3)
		error( 'Ladder should have at least 3 arms to be symmetrical ...' );
	end
	if ~strcmp(symTestStr,fliplr(symTestStr)) 
		error( 'Ladder is not topologically symmetrical ...' );
	end
end

if ( nargin < 4 )
	figNo = 1;
end
if ( ~exist('impulseResponseLength','var') || isempty(impulseResponseLength) )
	xnLength  = 512;
	fftLength = 4*xnLength;
else
	xnLength  = impulseResponseLength;
	fftLength = 2 ^ (ceil( log2(xnLength) ));
end

% translate topology
% first, seperate Rsource and Rload
Rsource   = elValues(1);
Rload     = elValues(end);
elValues  = elValues(2:end-1);
elCodes   = elCodes(2:end-1);
nSlices   = length(elCodes);
nWdas     = nSlices + sum( (lower(elCodes) == 's') | (lower(elCodes) == 'p') );
wdaStruct = char( '+' * ones(2,nSlices) );
lowerElCodes = lower(elCodes);
wdaStruct(1, ( lowerElCodes == 'l') ) = '-';
if ( pref3p == 1 )
	wdaStruct(1, ( lowerElCodes == 's') ) = 's';
	wdaStruct(1, ( lowerElCodes == 'p') ) = 'p';
else
	wdaStruct(1, ( lowerElCodes == 's') ) = 'S';	
	wdaStruct(1, ( lowerElCodes == 'p') ) = 'P';
end
%==============================================
wdaStruct(2, ( elCodes >= 'a' ) ) = 's';		% lower case, series arm
wdaStruct(2, ( elCodes < 'a'  ) ) = 'p';		% UPPER CASE, shunt arm
if ( prefSym == 1 )
	midSliceNo = (nSlices+1)/2;
	wdaStruct(2,midSliceNo) = upper( wdaStruct(2,midSliceNo) );
else
	wdaStruct(2,end) = upper( wdaStruct(2,end) );
end

% wdaStruct describes the topology as needed here
% we now have to find the correct numbering sequence
tmpStr = wdaStruct(:);
tmpIx  = find( ~( (tmpStr == '-') | (tmpStr == '+') ) );
wdaNo  = zeros(2*nSlices,1);
wdaNo(tmpIx) = 1:nWdas;
wdaNo  = reshape(wdaNo,2,nSlices);

% for output info; for calculation in fact only R2 bottom row needed
Rmat = zeros(3,nWdas);
Smat = zeros(3,3,nWdas);
aMat = NaN*ones(2,nWdas);
% determine parameters for the adaptors in the upper row
% Delay elements for inductors and capacitors in series arms
% are also considered to belong to the upper row.
% Besides the delay, translations of inductors also need an inversion.
% These can be found in combination with simple serial adaptors (port 2)
% (signB2 reflects them) 
%    ..........................
% 'resonance' adaptors (hard coded in simulation code).
signB2 = ones(1,nSlices);
signB2( wdaStruct(1,:) == '-' ) = -1;
elNo     = 1;
for i = 1:nSlices
	switch wdaStruct(1,i)
		case '-'			% inductor
			Rmat(2,wdaNo(2,i)) = elValues(elNo);
			elNo = elNo + 1;
		case '+'			% capacitor
			Rmat(2,wdaNo(2,i)) = 1 / elValues(elNo);
			elNo = elNo + 1;
		case 's'			% 3 port serial adaptor
			n     = wdaNo(1,i);
			R1    = 1 / elValues(elNo+1);
			R2    = elValues(elNo);
			R3    = R1 + R2;
			alpha = R1 / R3;
			%
			Rmat(:,n) = [ R1; R2; R3 ];
			aMat(1,n) = alpha;
			%
			Smat(:,:,n) = lfCreateSmat_3ps1m(alpha);
			Rmat(2,wdaNo(2,i)) = R3;
			elNo = elNo + 2;
		case 'p'			% 3 port parallel adaptor
			n     = wdaNo(1,i);
			R1    = 1 / elValues(elNo+1);
			R2    = elValues(elNo);
			R3    = R1*R2 / (R1 + R2);
			alpha = R2 / (R1 + R2);
			%
			Rmat(:,n) = [ R1; R2; R3 ];
			aMat(1,n) = alpha;
			%
			Smat(:,:,n) = lfCreateSmat_3pp1m(alpha);
			Rmat(2,wdaNo(2,i)) = R3;
			elNo = elNo + 2;
		case 'S'			% 2 port adaptor as a series resonator
			n     = wdaNo(1,i);
			LC    = elValues(elNo) * elValues(elNo+1);
			R1    = (1 + LC) / elValues(elNo+1);
			R2    = R1 / LC;
			%==========================================================================
			alpha = 2 / (elValues(elNo+1) * R1);	% this "alpha" is Nouta's "alpha1"
			%==========================================================================
			%
			Rmat(:,n) = [ R1; R2; NaN ];
			aMat(1,n) = alpha;
			%
			Smat(1:2,1:2,n) = lfCreateSmat_2p(alpha);
			Rmat(2,wdaNo(2,i)) = R1;
			elNo = elNo + 2;
		case 'P'			% 2 port adaptor as a parallel resonator
			n     = wdaNo(1,i);
			LC    = elValues(elNo) * elValues(elNo+1);
			R1    = elValues(elNo) / (1 + LC);
			R2    = LC * R1;
			%==========================================================================
			alpha = 2 * elValues(elNo+1) * R1;		% this "alpha" is Nouta's "alpha1"
			%==========================================================================
			%
			Rmat(:,n) = [ R1; R2; NaN ];
			aMat(1,n) = alpha;
			%
			Smat(1:2,1:2,n) = lfCreateSmat_2p(alpha);
			Rmat(2,wdaNo(2,i)) = R1;
			elNo = elNo + 2;
	end
end

% now handle the bottom row of adaptors
if ( prefSym == 1 )
	% first from input to middle adaptor ...
	% RELEASE 14  USE NESTED FUNCTION
	R1_midSlice = nfComputeWDF(Rsource,(1:midSliceNo-1));
	% ... then from output to middle adaptor ...
	R3_midSlice = nfComputeWDF(Rload  ,(nSlices:-1:midSliceNo+1));


	% ... finally the adaptor in the middle
	R1 = R1_midSlice;
	n  = wdaNo(2,midSliceNo);
	R2 = Rmat(2,n);
	R3 = R3_midSlice;
	switch wdaStruct(2,midSliceNo)
		case 'S'
			sumR  = R1 + R2 + R3;
			alpha = 2/sumR * [R1; R3];
			Smat(:,:,n) = lfCreateSmat_3ps2m(alpha(1),alpha(2));
		case 'P'
			mixR  = R1 + R3 + R1*R3/R2;
			alpha = 2/mixR * [R3; R1];
			Smat(:,:,n) = lfCreateSmat_3pp2m(alpha(1),alpha(2));
	end
	aMat(:,n) = alpha;
	Rmat(:,n) = [ R1; R2; R3 ];
else
	% not symmetrical: from left to right
	prevR3 = Rsource;
	for i = 1:nSlices
		n  = wdaNo(2,i);
		R1 = prevR3;
		R2 = Rmat(2,n);
		switch wdaStruct(2,i)
			case 's'
				R3    = R1 + R2;
				alpha = R1 / R3;
				aMat(1,n) = alpha;
				Smat(:,:,n) = lfCreateSmat_3ps1m(alpha);
			case 'S'
				R3    = Rload;
				sumR  = R1 + R2 + R3;
				alpha = 2/sumR * [R1; R3];
				aMat(:,n) = alpha;
				Smat(:,:,n) = lfCreateSmat_3ps2m(alpha(1),alpha(2));
			case 'p'
				R3    = R1*R2 / (R1 + R2);
				alpha = R2 / (R1 + R2);
				aMat(1,n) = alpha;
				Smat(:,:,n) = lfCreateSmat_3pp1m(alpha);
			case 'P'
				R3    = Rload;
				mixR  = R1 + R3 + R1*R3/R2;
				alpha = 2/mixR * [R3; R1];
				aMat(:,n) = alpha;
				Smat(:,:,n) = lfCreateSmat_3pp2m(alpha(1),alpha(2));
		end
		Rmat(:,n) = [ R1; R2; R3 ];
		prevR3 = R3;
	end
end


		%================================================================
		% This is the Release 14 and up recognizable "nested function"
		% which can access all variables in this scope
		% nested function
		function R3 = nfComputeWDF(prevR3,iRange)
			for i = iRange
				n  = wdaNo(2,i);
				R1 = prevR3;
				R2 = Rmat(2,n);
				switch wdaStruct(2,i)
					case 's'
						R3       = R1 + R2;
						alpha    = R1 / R3;
						thisSmat = lfCreateSmat_3ps1m(alpha);
					case 'p'
		  				R3       = R1*R2 / (R1 + R2);
		  				alpha    = R2 / (R1 + R2);
			  			thisSmat = lfCreateSmat_3pp1m(alpha);
  				end
				aMat(1,n)   = alpha;
				Smat(:,:,n) = thisSmat;
				Rmat(:,n)   = [ R1; R2; R3 ];
				prevR3      = R3;
	  		end
		end		% of nested function
		%================================================================



% handle Rload values differing from 1.0, and
% correct for port match inversions due to serial adaptors:
% change sign at forward output if odd number of serial adaptors in lower chain,
%             at reflection output if the structure starts with a parallel adaptor.
mulFacB3 = 1;
if ( abs(Rload - 1.0) > 1e-7 )
	mulFacB3 = 1 / sqrt(Rload);
end
if ( rem( sum(lower(wdaStruct(2,:)) == 's'),2 ) == 1 )  
	mulFacB3 = -mulFacB3;   % GIVEN THE SIGN CONVENTIONS IN OUR 3-PORT DEFINITIONS
end
mulFacs = aMat(~isnan(aMat))';		% row vector of all valid a's
if ( mulFacB3 ~= 1.0 )
	wdaStruct = [ wdaStruct ['x';'m'] ];
	wdaNo     = [ wdaNo [0;0] ];
	mulFacs   = [ mulFacs  mulFacB3 ];
end
WDF.wdaStruct = wdaStruct;
WDF.wdaNo	  = wdaNo;
WDF.mulFacs   = mulFacs(:);
%==========================================================================
% NOTE:  for 2-ports: mulFacs(x) is Nouta's "alpha1"   NOTE  NOTE  NOTE !!
%==========================================================================


%======  SIMULATION / CHECK  ======================================================
topRow2p = zeros(1,nSlices);
topRow3p = zeros(1,nSlices);
topRow2p( (wdaStruct(1,:) == 'S') | (wdaStruct(1,:) == 'P') ) = 1;
topRow3p( (wdaStruct(1,:) == 's') | (wdaStruct(1,:) == 'p') ) = 1;
xn       = [ 1 zeros(1,xnLength-1) ];
fwdB     = zeros(1,xnLength);
B        = zeros(3,nWdas);
allB     = zeros(3,nWdas,xnLength);
inputWda = wdaNo(2,1);

for t = 1:length(xn)
	% forward pass, top row
	for i = 1:nSlices
		if ( topRow2p(i) == 1 )
			B(2,wdaNo(2,i)) = B(1,wdaNo(1,i));
		elseif ( topRow3p(i) == 1 )
			n = wdaNo(1,i);
			B(3,n) = Smat(3,1:2,n) * [ B(1,n); -B(2,n) ];  % Note: invertor before B2
			B(2,wdaNo(2,i)) = B(3,n);
		end
	end
	% forward pass, bottom row
	if ( prefSym == 1 )
		% left side of midSlice
		B(3,inputWda) = Smat(3,1:2,inputWda) * [ xn(t); B(2,inputWda)*signB2(1) ];
		for i = 2:midSliceNo-1
			n = wdaNo(2,i);
			B(3,n) = Smat(3,1:2,n) * [ B(3,wdaNo(2,i-1)); B(2,n)*signB2(i) ];
		end
		% right side of midSlice
		B(3,nWdas) = Smat(3,1:2,nWdas) * [ 0; B(2,nWdas)*signB2(nSlices) ];
		for i = nSlices-1:-1:midSliceNo+1
			n = wdaNo(2,i);
			B(3,n) = Smat(3,1:2,n) * [ B(3,wdaNo(2,i+1)); B(2,n)*signB2(i) ];
		end
		% middle adaptor
		m = wdaNo(2,midSliceNo);
		B(:,m) = Smat(:,:,m) * [ B(3,wdaNo(2,midSliceNo-1)); ...
							B(2,m)*signB2(midSliceNo); B(3,wdaNo(2,midSliceNo+1)) ];
		% backward pass, bottom row
		% left side of midSlice
		for i = midSliceNo-1:-1:2
			n = wdaNo(2,i);
			B(1:2,n) = Smat(1:2,:,n) * ...
						[ B(3,wdaNo(2,i-1)); B(2,n)*signB2(i); B(1,wdaNo(2,i+1)) ];
		end
		B(1:2,inputWda) = Smat(1:2,:,inputWda) * ...
							   [ xn(t); B(2,inputWda)*signB2(1); B(1,wdaNo(2,2)) ];
		% right side of midSlice
		for i = midSliceNo+1:nSlices
			n = wdaNo(2,i);
			if ( i == nSlices )
				A1 = 0;
			else
				A1 = B(3,wdaNo(2,i+1));
			end
			if ( i == midSliceNo+1 )
				A3 = B(3,wdaNo(2,midSliceNo));
			else
				A3 = B(1,wdaNo(2,i-1));
			end
			B(1:2,n) = Smat(1:2,:,n) * [ A1; B(2,n)*signB2(i); A3 ];
 	 	end
	else	% not symmetric
		if ( nSlices > 1 )
			B(3,inputWda) = Smat(3,1:2,inputWda) * [ xn(t); B(2,inputWda)*signB2(1) ];
			for i = 2:nSlices-1
				n = wdaNo(2,i);
				B(3,n) = Smat(3,1:2,n) * [ B(3,wdaNo(2,i-1)); B(2,n)*signB2(i) ];
			end
			% final adaptor
			B(:,nWdas) = Smat(:,:,nWdas) * ...
							[ B(3,wdaNo(2,nSlices-1)); B(2,nWdas)*signB2(nSlices); 0 ];
			% backward pass, bottom row
			for i = nSlices-1:-1:2
				n = wdaNo(2,i);
				B(1:2,n) = Smat(1:2,:,n) * ...
							[ B(3,wdaNo(2,i-1)); B(2,n)*signB2(i); B(1,wdaNo(2,i+1)) ];
			end
			B(1:2,inputWda) = Smat(1:2,:,inputWda) * ...
								   [ xn(t); B(2,inputWda)*signB2(1); B(1,wdaNo(2,2)) ];
		else	% only one bottom adaptor
			B(:,nWdas) = Smat(:,:,nWdas) * [ xn(t); B(2,nWdas)*signB2(nSlices); 0 ];
		end
	end
	% update top row
	for i = 1:nSlices
		if ( topRow2p(i) == 1 )
			if ( wdaStruct(1,i) == 'S' )
				n = wdaNo(1,i);
				B(1:2,n) = Smat(1:2,1:2,n) * [ B(2,wdaNo(2,i)); B(2,n) ]; 
			elseif ( wdaStruct(1,i) == 'P' )
				n = wdaNo(1,i);
				% Note: invertor before own B2 (parallel)
				B(1:2,n) = Smat(1:2,1:2,n) * [ B(2,wdaNo(2,i)); -B(2,n) ]; 
			end
		elseif ( topRow3p(i) == 1 )
			n = wdaNo(1,i);  
			% Note: invertor before B2
			B(1:2,n) = Smat(1:2,:,n) * [ B(1,n); -B(2,n); B(2,wdaNo(2,i)) ];
		end
	end
		
	allB(:,:,t) = B;
end   % t-loop

if ( prefSym == 1 )
	fwdB = squeeze( allB(1,nWdas,:) );
else
	fwdB = squeeze( allB(3,nWdas,:) );
end
if ( mulFacB3 ~= 1.0 )
	fwdB = mulFacB3 * fwdB;
end	
revB = squeeze(  allB(1,inputWda,:) );
if ( lower(wdaStruct(2,1)) == 'p' )
	revB = -revB;
end


if ( figNo ~= 0 ) 
	showWDF(WDF,'L',figNo);
	figHandle = figure( figNo +1 ); 
	figPos    = get( figHandle, 'Position' );
	% change height of figure
	set( figHandle, 'Position', [ figPos(1) figPos(3)/4  figPos(3) figPos(3)/0.7 ] );

	% compute and plot the forward and reverse transmission functions
	fwdH = abs( fft( fwdB,fftLength ) );
	fwdH = fwdH( 1:fftLength/2 );
	w   = (0:length(fwdH)-1) / fftLength;
	revH = abs( fft( revB,fftLength ) );
	revH = revH( 1:fftLength/2 );

	sub1Handle = subplot(2,1, 1);
	set( sub1Handle, 'Position', [ 0.13 0.50 0.775 0.43 ] );
	warning off
	plot( w, 20*log10(fwdH), w,20*log10(revH),'r', 'linewidth',2 );	
	warning on
	axis( [xlim -80 +10] );
	grid on;
	if ( pref3p == 1 )
		title( 'Reconstructed from the adaptor (all three-ports) structure ...' );
	else
		title( 'Reconstructed from the adaptor (two- and three-ports) structure ...' );
	end
	xlabel( 'Frequency / Sample Frequency' );
	ylabel( 'Magnitude in dB' );
	legend( ' forward B_{fwd}', ' reverse B_{rev}' );

	% also compute and plot the frequency transfer functions from input 
	% to all B-outputs
	allH = abs( fft( reshape( allB,3*nWdas,xnLength ),fftLength,2 ) );
	allH = allH( :,1:fftLength/2 );
	sub2Handle = subplot(2,1, 2);
	set( sub2Handle, 'Position', [ 0.13 0.11 0.775 0.25 ] );
	bar( reshape(max(allH,[],2),3,nWdas)', 1.2 );
	grid on;
	xlabel( 'Adaptor Number ( resp. B1,B2[,B3] )' );
	ylabel( 'Maximum Signal Level in Frequency range' );
end


%==================================================================================
%==========  LOCAL NESTED FUNCTIONS  ==== originally release 13 style =============
%==================================================================================

%==========================================================================
% a1 is Nouta's "alpha1"
%==========================================================================
function Smat = lfCreateSmat_2p(a1)
  p1ma1 = 1.0 - a1;
  Smat  = [ -p1ma1  2.0-a1;  a1  p1ma1 ];
end

function Smat = lfCreateSmat_3ps1m(a1)
  a1m1 = a1 - 1.0;
  Smat = [ -a1m1  -a1  -a1;  a1m1  a1  a1m1;  -1.0  -1.0  0 ];
end

function Smat = lfCreateSmat_3pp1m(a1)
  a1m1 = a1 - 1.0;
  Smat = [ a1m1  -a1m1  1.0;  a1  -a1  1.0;  a1  -a1m1  0 ];
end

function Smat = lfCreateSmat_3ps2m(a1,a3)
  a1a3m2 = a1 + a3 - 2.0;
  Smat   = [ 1.0-a1  -a1  -a1; a1a3m2  a1a3m2+1.0  a1a3m2;  -a3  -a3  1.0-a3 ];
end
  
function Smat = lfCreateSmat_3pp2m(a1,a3)
  ma1a3m2 = -a1 - a3 + 2.0;
  Smat    = [ a1-1.0  ma1a3m2  a3;  a1  ma1a3m2-1.0  a3;  a1  ma1a3m2  a3-1.0 ];
end


end  % of overall function "ladder2WDF"

