function NlpLadder = nlp_ladder(ApproxMethod,filterOrder,varargin)
%NLP_LADDER	 Designs a ladder type normalized lowpass filter
%	NlpLadder = NLP_LADDER(...) returns a MATLAB structure NlpLadder
%	that describes the topology of a ladder type lowpass filter. 
%	Printed information in the command window and some plots are
%	also provided.
%	NlpLadder will contain the fields  
%		NlpLadder.elements		-- a string describing the ladder
%		NlpLadder.values      	-- a (set of) column vector(s) with the 
%								   element values
%	The elements-string may consist of the following elements:
%		'r' for the source resistance, 'R' for the load resistance,
%		'l' for an inductor in a series arm,
%		'C' for a capacitor in a shunt arm, 
%		'p' for a parallel resonance LC-circuit in a series arm, 
%		'S' for a serial resonator LC-circuit in a shunt arm,
%		'U' for Unit Elements.
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	The source resistance Rsource ('r') is choosen to be always 1 Ohm.
%	In case two or more resonators are present in the resulting filter, say 
%	representing frequencies f1 and f2, NlpLadder.values may contain several
%	columns, representing the various permutations of the frequencies 
%	(here column1: f1-f2 and column2: f2-f1).
%	At the end, functions PLOTHS and LADDER2MAGN are called to compare the 
%	theoretical magnitude transfer function with the one reconstructed from
%	the ladder structure as has been found.
%
%	The syntax of the function is  
%	NlpLadder = NLP_LADDER(ApproxMethod,filterOrder, ..additional parameters.. )
%	where ApproxMethod can be one of the strings:
%		'butter', 'cheby', 'invcheby', 'cauer' or 'vlach',
%	the number of additional parameters needed being dependant on the chosen
%	approximation method.
%
%	Without going into much detail, the set of possible commands will be listed
%	here. Details can be found in the m-files Hs_butter.m, Hs_cheby.m, etc.
% 	The variable 'ZorY' is used to specify whether the ladder circuit should
%	start with a series arm (XorY = 'Z') or with a shunt arm (ZorY = 'Y').
%	If left out, the ladder will start with a shunt arm.
%	The first element can be a Unit Elements, if needed.
%	
%	X = NLP_LADDER('butter',filterOrder) 
%	X = NLP_LADDER('butter',filterOrder,ZorY) 
%
%	X = NLP_LADDER('cheby',filterOrder,passBandRipple_dB)
%	X = NLP_LADDER('cheby',filterOrder,passBandRipple_dB,freqNormMode) 
%	X = NLP_LADDER('cheby',filterOrder,passBandRipple_dB, ...
%															freqNormMode,ZorY) 
%
%	X = NLP_LADDER('invcheby',filterOrder,stopBandRipple_dB)
%	X = NLP_LADDER('invcheby',filterOrder,stopBandRipple_dB,freqNormMode)
%	X = NLP_LADDER('invcheby',filterOrder,stopBandRipple_dB, ...
%															freqNormMode,ZorY) 
%
%	X = NLP_LADDER('cauer',filterOrder,passBandRipple_dB, ...
%													stopBandRipple_dB,skwirNorm)
%	X = NLP_LADDER('cauer',filterOrder,passBandRipple_dB, ...
%									   stopBandRipple_dB,skwirNorm,freqNormMode)
%	X = NLP_LADDER('cauer',filterOrder,passBandRipple_dB, ...
%								  stopBandRipple_dB,skwirNorm,freqNormMode,ZorY)
%
%	X = NLP_LADDER('vlach',filterOrder,passBandRipple_dB,stopBandZeros)
%	X = NLP_LADDER('vlach',filterOrder,passBandRipple_dB,stopBandZeros, ...
%															stopBandZerosVector)
%	where the stopBandZeroVector can be used, when there are less stopBandZeros
%	than the filterOrder allows for, to specify the locations of the resonators 
%	with 0's (no resonator here) and 1's (resonator here). 
%	If not specified, resonators are by default filled in from output to input.
%	Furthermore, given a number of zeros and a number of locations, all 
%	possible permutations of the resonators will be calculated.
%	examples:	NlpLadder = NLP_LADDER('vlach',9,1,[1.2 1.5])
%				NlpLadder = NLP_LADDER('vlach',9,1,[1.2 1.5], [ 0 1 1 0 ] );
%	X = NLP_LADDER('vlach',filterOrder,passBandRipple_dB,stopBandZeros, ...
%										 stopBandZerosVector,unitElementsVector)
%	where the number of and the locations of the Unit Elements can be specified
%	in the unitElementsVector with 0's and 1's. Unit Elements are filled in 
%	from input to output.
%	examples:	NlpLadder = NLP_LADDER('vlach',3,1,1.5,[1], [ 1 1 ] )
%				NlpLadder = NLP_LADDER('vlach',3,1,1.5,[1], [ 0 1 1 ] )
%				NlpLadder = NLP_LADDER('vlach',0,1,[],[], [ 1 1 1 1 1 ] )
%	X = NLP_LADDER('vlach',filterOrder,passBandRipple_dB,stopBandZeros, ...
%							  stopBandZerosVector,unitElementsVector,freqNormMode)
%	X = NLP_LADDER('vlach',filterOrder,passBandRipple_dB,stopBandZeros, ...
%	     				 stopBandZerosVector,unitElementsVector,freqNormMode,XorY)
%
%	See also NLPF, NLADDER2LP, NLADDER2HP, NLADDER2BP, NLADDER2BS,
%            LADDERSYNTHESIS, PLOTHS, LADDER2MAGN

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, December 2003


if ~exist( 'filterOrder','var' )
	error( 'Filter order should be defined ...' );
end
varLength = length(varargin);
% Rsource   = 1;

% default for all filter types: start with a shunt arm
ZorY         = 'Y';
% default freqNormMode, interpretation depending on filter type 
freqNormMode =   0;					

result = 1;		% assume realizable circuit
switch lower(ApproxMethod)
%==========================================================================================
	case 'butter'
		if ( varLength > 0 )
			ZorY = upper( char( varargin(1) ) );
		end			
		% determine reference transfer function
		Hs = nlpf( ApproxMethod, filterOrder );		
		% determine topology
		elementsStr = char( 'C' * ones(1,filterOrder) );
		if ( ZorY == 'Y' );
			elementsStr(2:2:end) = 'l';   % character 'el'
		else
			elementsStr(1:2:end) = 'l';   
		end
		NlpLadder.elements = [ 'r' elementsStr 'R' ];		

		% Now from:
		%	'explicit formula for a double-resistance-terminated lossless ladder'
		%	Active and Passive Analog Filter Design, An Introduction
		%	Lawrence P. Huelsman,  McGraw-Hill, Inc.;  1993
		%	ISBN 0-07-030860-8
		elValues = 2*sin( (1:2:2*filterOrder)*pi/(2*filterOrder) );
		% Source and Load resistors of 1 Ohm are assumed
		% Use column notation
		NlpLadder.values = [ 1.0; elValues(:); 1.0 ];		
				

%==========================================================================================
	case 'cheby'			
		switch varLength
			case 3
				ZorY         = upper( char( varargin(3) ) );
				freqNormMode = varargin{2};					
			case 2
				freqNormMode = varargin{2};
				if ~( isnumeric( freqNormMode ) )
					error( 'Specify freqNormMode before ZorY ...' );
				end				
			case 0
				error( 'No pass band ripple specified ...' );
		end	
		passBandRipple_dB = varargin{1};
		% determine reference transfer function
		Hs = nlpf( ApproxMethod, filterOrder, passBandRipple_dB, freqNormMode ); 
		% determine topology
		elementsStr = char( 'C' * ones(1,filterOrder) );
		if ( ZorY == 'Y' );
			elementsStr(2:2:end) = 'l';   % character 'el'
		else
			elementsStr(1:2:end) = 'l';   
		end
		NlpLadder.elements = [ 'r' elementsStr 'R' ];		

		[elValues,Rload] = lfChebyLC( filterOrder, passBandRipple_dB, freqNormMode );
		% NOTE: the elValue's and Rload above hold true for a ZorY == 'Z' !!!
		if ( ZorY == 'Y' )
			Rload = 1/Rload;
		end
		NlpLadder.values = [ 1.0; elValues(:); Rload ];		


%==========================================================================================
	case 'invcheby'
		switch varLength
			case 3
				ZorY         = upper( char( varargin(3) ) );
				freqNormMode = varargin{2};					
			case 2
				freqNormMode = varargin{2};					
				if ~( isnumeric( freqNormMode ) )
					error( 'Specify freqNormMode before ZorY ...' );
				end				
			case 0
				error( 'No stop band ripple specified ...' );
		end	
		stopBandRipple_dB = varargin{1};
		% determine reference transfer function
		Hs = Hs_invcheby(filterOrder, stopBandRipple_dB, 1.0, freqNormMode );
		% extract all necessary information from Hs 
		roots_fs = Hs.roots_fs;
		poly_gs  = Hs.poly_gs;

		% reflection frequencies all at zero frequency
		%
		%                 g(s) + h(s)
		% construct Zi = -------------, while h(s) == g(s)[1] == 1
		%                 g(s) - h(s)
		%
		InputYZ.num = [ 2*poly_gs(1); poly_gs(2:end)' ];
		InputYZ.den = poly_gs(2:end)';
		
		% first, setup topology accounting for the resonators
		elType = [char('x'*ones(1,filterOrder)) 'R'];
		elType(2:2:end-1) = 'W';
		Topology.elTypeStr = elType;
		% then, determine whether a type is to be extracted from a Z or a Y 
		Topology.ZorYStr   = lfCreateZYvector(filterOrder,ZorY);

		ws       = imag( roots_fs(2:2:end) );
		nWs      = length(ws);
		wsIndex  = perms(1:nWs);   % (nWs:-1:1)
		nIndex   = size(wsIndex,1);
		nEls     = length(elType);
		elValues = zeros( 1 + nEls + floor((nEls-1)/2), nIndex );
		i = 1;
		while ( result && ( i <= nIndex ) )
			[elValues(:,i),result] = ladderSynthesis(InputYZ,Topology, ...
														ws(wsIndex(i,:)) );
			i = i +1;
		end
		NlpLadder.elements = lfCodeElements(Topology);
		NlpLadder.values   = elValues;


%==========================================================================================
	case 'cauer'
		% different default freqNormMode for cauer filters
		freqNormMode = -1;
		switch varLength
			case 5 
				ZorY         = upper( char( varargin(5) ) );
				freqNormMode = varargin{4};					
				skwirMode    = upper( varargin{3} );
			case 4
				freqNormMode = varargin{4};
				if ~( isnumeric( freqNormMode ) )
					error( 'Specify freqNormMode before ZorY ...' );
				end				
				skwirMode    = upper( varargin{3} );
			case 3
				skwirMode    = upper( varargin{3} );
			case 1
				error( 'No stop band ripple specified ...' );
			case 0
				error( 'No pass band ripple specified ...' );
		end	
		passBandRipple_dB = varargin{1};
		stopBandRipple_dB = varargin{2};
		oddFilterOrder = ( rem(filterOrder,2) == 1 );
		if oddFilterOrder
			if ~( skwirMode == 'A' )
			 	skwirMode = 'A';
			 	fprintf( 'WARNING: odd filterOrder, so skwirMode set to ''A'' ...\n' );
			 	beep; pause(0.5); beep;
			 end
		elseif ~( (skwirMode == 'B') || (skwirMode == 'C') )
			error( 'Even filterOrder should have skwirMode B or C ...' );
		end
		% determine reference transfer function
		[Hs,wp] = Hs_cauer( filterOrder, passBandRipple_dB, stopBandRipple_dB, ...
                                                       skwirMode, 1.0, freqNormMode );
		% ... extract the necessary information from Hs 
		roots_fs = Hs.roots_fs;
		poly_gs  = Hs.poly_gs;

		% reconstruct h(s) in order to compute the input impedance/admittance
		poly_hs = poly([ j*wp; -j*wp]);
		% for odd filterOrders, there should be only a SINGLE pole at f_zero,
		% so strip off the last zero of poly_hs (e.g. divide by s)
		if ( skwirMode == 'A' )
			poly_hs = poly_hs(1:end-1);
		end
		InputYZ.num = ( poly_gs + poly_hs )';
		denYZ       = ( poly_gs - poly_hs )';
		InputYZ.den = denYZ(2:end);

		% first, setup topology accounting for the resonators
		elType = [ char('x'*ones(1,filterOrder)) 'R' ];
		if ( skwirMode == 'A' )
			elType(2:2:end-1) = 'W';
		else
			elType(2:2:end-2) = 'W';
		end
		Topology.elTypeStr = elType;
		% then, determine whether a type is to be extracted from a Z or a Y 
		Topology.ZorYStr   = lfCreateZYvector(filterOrder,ZorY);

		ws       = imag( roots_fs(2:2:end) );
		nWs      = length(ws);
		wsIndex  = perms(1:nWs);   % (nWs:-1:1)
		nIndex   = size(wsIndex,1);
		elValues = zeros( 1 + length(elType) + nWs, nIndex );
		i = 1;
		while ( result && ( i <= nIndex ) )
			[elValues(:,i),result] = ladderSynthesis(InputYZ,Topology, ...
														ws(wsIndex(i,:)) );
			i = i +1;
		end
		NlpLadder.elements = lfCodeElements(Topology);
		NlpLadder.values   = elValues;


%==========================================================================================
%    nlp_ladder(ApproxMethod,filterOrder,passBandRipple,stopBandZeros, stopBandZerosVector,
%                                                unitElementsVector, freqNormMode, ZorY );
	case 'vlach'
		stopBandZeros    = [];
		stopBandZerosVec = [];
		unitElementsVec  = [];
		maxStopBandZeros = fix( filterOrder/2 );
		switch varLength
			case 6 
				ZorY             = upper( char( varargin(6) ) );
				freqNormMode     = varargin{5};
				unitElementsVec  = varargin{4};
				stopBandZerosVec = varargin{3};
				stopBandZeros    = varargin{2};
			case 5 
				freqNormMode     = varargin{5};
				unitElementsVec  = varargin{4};
				stopBandZerosVec = varargin{3};
				stopBandZeros    = varargin{2};
			case 4
				unitElementsVec  = varargin{4};
				stopBandZerosVec = varargin{3};
				stopBandZeros    = varargin{2};
			case 3
				stopBandZerosVec = varargin{3};
				stopBandZeros    = varargin{2};
			case 2
				stopBandZeros    = varargin{2};
			case 0
				error( 'No pass band ripple specified ...' );
		end	
		passBandRipple_dB = varargin{1};
		nStopBandZeros    = length(stopBandZeros);
		if ( nStopBandZeros > maxStopBandZeros )
			error( 'Maximum possible number of stopBandZeros equals %d ...', ...
			                                                         maxStopBandZeros );
		end
		if ( (varLength == 2) || (nStopBandZeros == 0) )% || (nStopBandZeros == maxStopBandZeros) )
			stopBandZerosVec = [ zeros(1,maxStopBandZeros-nStopBandZeros) ones(1,nStopBandZeros) ];
		end
		if ( sum( stopBandZerosVec == 1 ) ~= nStopBandZeros )
			error( 'stopBandzerosVector should show %d entries from which %d are 1''s ...', ...
			 													maxStopBandZeros, nStopBandZeros );
		end
		if ( length(stopBandZerosVec) ~= maxStopBandZeros )
			error( 'stopBandZerosVector should show %d entries ...', maxStopBandZeros );
		end
		nUnitElements = sum( unitElementsVec == 1 );
		if ( (nUnitElements + sum(unitElementsVec == 0)) ~= length(unitElementsVec) )
			error( 'UnitElements vector should contain only 0''s and/or 1''s ...' );
		end
		if ( (filterOrder == 0) && (nUnitElements == 0) )
			error( 'filterOrder 0 only possible if Unit Elements present ...' );
		end
		% determine reference transfer function
		[Hs,wp] = Hs_vlach(filterOrder, passBandRipple_dB, 1.0, stopBandZeros, ...
                                   	   				  nUnitElements, freqNormMode );
		% ... extract the necessary information from Hs
		poly_fs = Hs.poly_fs;
		if ( nUnitElements >= 1 )
			poly_fs = poly_fs{1};
		end 
		poly_gs = Hs.poly_gs;

		% reconstruct h(s) in order to compute the input impedance/admittance
		poly_hs = poly([ j*wp; -j*wp]);
		% for odd order filters, there should be only a SINGLE pole at f_zero,
		% so strip off the last zero of poly_hs (e.g. divide by s)
		if ( rem(filterOrder + nUnitElements,2) == 1 )		% odd overall Order
			poly_hs = poly_hs(1:end-1);
		end
		% special treatment if all UnitElements filter,
		% magnitude level -rp dB for cutOffFrequency == 1.0
		% NOTE: freqNormMode 1 (-3 dB) results in 'Not realizable'-errors
		if ( (filterOrder == 0) && (nUnitElements >= 1) )
			e = sqrt( 10^(passBandRipple_dB/10) -1 );
			C = sqrt(2)^nUnitElements / prod(1-wp.^2);
			poly_hs = e*C*poly_fs * poly_hs;
		end
		InputYZ.num = ( poly_gs + poly_hs )';
		denYZ 		= ( poly_gs - poly_hs )';
		if ( abs(denYZ(1)) <= 1e-12 )		% not true if only UnitElements
			denYZ = denYZ(2:end);
		end
		InputYZ.den = denYZ;

		% first, setup topology accounting for stopBandZerosVec and unitElementsVec
		elType = [ char('x'*ones(1,filterOrder)) 'R' ];
		elType( 2*find(stopBandZerosVec) ) = 'W';
		for i = length(unitElementsVec):-1:1
  			if ( unitElementsVec(i) == 1 )
  				ipos = min(filterOrder+1,i);
    			elType = [ elType(1:ipos-1) 'U' elType(ipos:end) ];
  			end
		end
		Topology.elTypeStr = elType;
		% then, determine whether a type is to be extracted from a Z or a Y 
		Topology.ZorYStr   = lfCreateZYvector(filterOrder+nUnitElements, ZorY);

		sbzIndex = perms(1:nStopBandZeros);   % (nWs:-1:1)
		nIndex   = size(sbzIndex,1);
		elValues = zeros(filterOrder + nStopBandZeros + nUnitElements +2,nIndex);
		i = 1;
		while ( result && ( i <= nIndex ) )
			[elValues(:,i),result] = ladderSynthesis(InputYZ,Topology, ...
												stopBandZeros(sbzIndex(i,:)) );
			i = i +1;
		end
		NlpLadder.elements = lfCodeElements(Topology);
		NlpLadder.values   = elValues;

		
%==========================================================================================
	otherwise
		error( 'Unknown ApproxMethod ...' );
end

if result
	switch ApproxMethod
		case { 'butter', 'cheby' }
			nFreqPoints = 1000;
		case { 'invcheby', 'cauer' }
			nFreqPoints = 2500;
		case 'vlach'
			if ( nStopBandZeros == 0 )
				nFreqPoints = 1000;
			else
				nFreqPoints = 2500;
			end
	end
	showLadder(NlpLadder,1,[ ApproxMethod ' lowpass filter' ] );
	plotHs( Hs, 1, 2,[],[], nFreqPoints );
	% check the first (or only) configuration, no plot yet
	[magn_dB,freq] = ladder2Magn(NlpLadder, nFreqPoints,0);
	figure(2)
	hold on
	plot( freq,magn_dB, 'r:','LineWidth',2 );
	hold off
	legend( 'reference magnitude function', 'reconstructed from ladder topology' );
else
	close all;
   	error('NLP_LADDER:SYNTHESIS', ...
   					'Circuit not realizable within proper accuracy bounds ...');
end


%==========================================================================================
%==========================================================================================
%=========  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ============
%==========================================================================================
%==========================================================================================

function zyVec = lfCreateZYvector(nElements,ZorY)
  zyVec = char( 'Y' * ones(1,nElements+1) );
  if ( ZorY == 'Y' )
	  zyVec(2:2:end) = 'Z';
  else
	  zyVec(1:2:end) = 'Z';
  end


%==========================================================================================
function [LC,Rload] = lfChebyLC(filterOrder,passBandRipple_dB,freqNormMode)
  % Rsource is assumed to be 1 Ohm.
  %
  % See:	Wai-Kai Chen
  %   	John Wiley & Sons, Inc.
  %   	1986
  %   	ISBN 0-471-82352-X
  % where in the case that K == 1, aHat becomes 0 (Note that K ~= K@dc !!) 
  % For calculation of -3 dB frequency, see
  %   	Computerized Approximation and Synthesis of Lineair Networks
  %   	Jiri Vlach
  %   	pg. 256
  %
  % Note that always Rload == 1 for odd filterOrders.
  % For even filterOrders, when we start from a Zin (and the LC values are 
  % derived for that case), Rload == 2.65972 Ohm.
  % Starting from Yin then results in Rload == 0.37598  ( = 1/2.65972 )

  % implicit choice: Rsource = 1.0;
  k       = 10 ^ ( passBandRipple_dB/10 );
  epsilon = sqrt( k-1 );
  if ( rem(filterOrder,2) == 1 )	% odd order
	  Rload = 1;
  else								% even order
	  % the following choice of Rload implies that we start from a Zin
	  Rload = (2*k-1) + 2*sqrt( k*(k-1) );
  end

  a    = 1/filterOrder * asinh( 1/epsilon );
  tmp1 = ( sinh(a) )^2;
  phi  = ( 1:filterOrder ) * pi / filterOrder;
  fm   = ( (sinh(a))^2 )*ones(1,filterOrder) + ( sin(phi) ).^2;

  Q = [ 1/sinh(a);  zeros(filterOrder-1,1) ];	% column vector
  for i = 2:filterOrder
	  Q(i) = 1 / ( Q(i-1) * fm(i-1) );
  end
  LC = 2 * Q .* sin( (1:2:2*filterOrder)' * pi / (2*filterOrder) );

  if ( freqNormMode == 1)
	  LC = LC * cosh( 1/filterOrder * acosh(1/epsilon) );
  end


%==========================================================================================
function elString = lfCodeElements(topology)
  %           resistor: 'r' or 'R',
  %           inductor: 'l' or 'L', 
  %          capacitor: 'c' or 'C',
  %   series resonator: 's' or 'S',
  % parallel resonator: 'p' or 'P',
  %       unit element: 'U'.
  % Lower case for series arms, upper case for shunt arms.
  elType = topology.elTypeStr;
  zyVec  = topology.ZorYStr;
  elStr = char( ' ' * ones(1,length(elType)-1) );
  for i = 1:length(elType)-1
  	  switch elType(i)
  	  	  case 'x'
  	  	  	  if ( zyVec(i) == 'Z' )
  	  	  	  	 elStr(i) = 'l';
  	  	  	  else
  	  	  	  	 elStr(i) = 'C';
  	  	  	  end 
  	  	  case 'W'
  	  	  	  if ( zyVec(i) == 'Z' )
  	  	  	  	 elStr(i) = 'p';
  	  	  	  else
  	  	  	  	 elStr(i) = 'S';
  	  	  	  end 
  	  	  case 'U'
  	  	  	  elStr(i) = 'U';
	  end  	  	 
  end
  elString = [ 'r' elStr 'R' ];
  

%==========================================================================================
%------  END LOCAL FUNCTION  =======  END OF PROGRAM  =====================================
%==========================================================================================
  