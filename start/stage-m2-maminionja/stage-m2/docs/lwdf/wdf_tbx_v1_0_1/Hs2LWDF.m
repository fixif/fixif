function [LWDF,Hz,Messages] = Hs2LWDF(Hs,figNo,showMessages,plotOptionsString)
%HS2LWDF	Calculates the coefficients of a Lattice Wave Digital Filter 
%	LWDF = HS2LWDF(Hs) creates a structure LWDF given a transfer function Hs.
%%	The structure Hs should be organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s. Odd polynomials Hs.poly_gs result in low/high pass LWDFs,
%	even polynomials in bandpass/stop LWDFs.
%	The structure LWDF will contain the fields
%		LWDF.wdaCodes and
%		LWDF.gamma
%	LWDF.wdaCodes is an array of 2 strings, which describe the presence
%	and positions of the adaptors to be used. The following adaptor 
%	combinations are recognized
%		't' - a single delay element
%		's' - one 2-port and one delay element
%		'S' - one 2-port with two cascaded delay elements
%		'd' - two 2-ports with two delay elements
%		'D' - two 2-ports with two times two cascaded delay elements
%		'x' - only an interconnection in this slot
%	LWDF.gamma gives the coefficient values for the 2-ports.
%	The block diagram shown (default) can be used to see which adaptor 
%	corresponds to which coefficient.
%
%	[LWDF,Hz] = HS2LWDF(Hs) additionally returns the discrete-time magnitude 
%	transfer function Hz that can be reconstructed from the LWDF structure.
%	
%	[...] = HS2LWDF(Hs,figNo) can be used to control the block diagram plot. 
%	Use figNo = 0 if no output is wanted. When no figNo is specified, 
%	figure(1) will be used for plotting, otherwise figure(figNo). 
%
%	[LWDF,Hz,Messages] = HS2LWDF(Hs,figNo,showMessages) can be used to
%	control the printing of error messages in the workspace window.
%	showMessages 1 acts as 'normal': errors are signalled, while 
%	showMessages 0 suppresses output and returns the error messages in the 
%	output string Messages.
%
%	[LWDF,Hz,Messages] = HS2LWDF(Hs,figNo,showMessages,plotOptionsString)
%	To enable the output of an additional Hz plot, plotOptions can be entered
%	(as a string), which are passed to PLOTHZ. See PLOTHZ for an extensive
%	description of the options.
%
%	Examples:
%		% a 6th order bandpass filter (Butterworth approximation method)
%		[LWDF,Hz] = hs2lwdf(nlp2bp(hs_butter(3),fz2fs(0.15),0.1),1,1,'1,2');
%		
%		% an 11th order bireciprocal cauer filter
%		Hs = Hs_cauer_birec(11,55);  
%		Hs2LWDF(Hs(1),1,1,'1,2');
%
%	See also SHOWLWDF, LWDF2HZ.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, Febrary 2004
%                                     Feb2006: default to dlyLorR = 'L'

% symmetric bpvlach recognized as lowpass transformed to fc=fs/4

if ~exist('showMessages','var') 
	showMessages = 1;
end
if ~exist('figNo','var') 
	figNo = 1;
end
ctol      = 1e-12;

% important checks to judge whether the given transfer function can be
% really translated into a two channel lwdf
poly_fs = Hs.poly_fs;
if ~iscell(poly_fs)
	nUnitElements = 0;
else
	nUnitElements = poly_fs{2};
	poly_fs       = poly_fs{1};
end

roots_gs = cplxpair( Hs.roots_gs );		% be sure the roots are in THIS order
% from cplxpair: ..... The pairs are ordered by increasing real part.
%                Any purely real elements are placed after all the complex pairs.
poly_gs  = poly(roots_gs);

msgStr = '';
errStr = '';
filterOrder    = length(roots_gs);
orgFilterOrder = filterOrder - nUnitElements;
isLowPass      = ( rem(filterOrder,2) == 1 );

try

	if isLowPass
	
		msgStr = 'LWDF: ODD filter order, so LOW/HIGH pass filter assumed\n';
		if ( rem(nUnitElements,2) == 1 )
			errStr = '... but ODD number of Unit Elements (incorrect stopband results) ...';
			error( errStr );
		end
		% single root should be the first one from now on
		roots_gs = [ roots_gs(end); roots_gs(1:2:end-1) ];
		% now compute the coefficients for the lp/hp lwdf architecture
		nSlices = ceil( length(roots_gs)/2 );
		codes = char( 'x' * repmat( [1;1],1,nSlices) );
		gamma   = NaN * ones( 2,nSlices,2 );
		B0      = -roots_gs(1);
		gamma(1,1,1) = (1-B0) / (1+B0);	% first of top row
		if ( filterOrder > 1 )
			y = lfRoots2y( roots_gs(2:end), ctol );
			% rest of top row
			gamma(:,2:nSlices,1) = y(:,2:2:end);
			% complete bottom row	
			gamma(:,1:length(roots_gs)-nSlices,2) = y(:,1:2:end);
			codes( (gamma(2,:,:) ~= 0) & ~isnan(gamma(2,:,:)) ) = 'd';
			codes( gamma(2,:,:) == 0 ) = 'S';
		end
		if ( gamma(1,1,1) ~= 0 ) 
			codes(1,1) = 's';
		else
			codes(1,1) = 't';
		end

	else								% bandpass, needs some more effort

		msgStr = 'LWDF: EVEN filter order, so BANDpass/stop filter assumed\n';
		% check that roots do compose half of a circle, e.g. sorting by the real parts
		% should give a different sequence than sorting by the imaginary parts
		% Exception: a 2nd order filter needs special treatment:
		%   a 2nd order low/high pass can't be realized with an lwdf
		%   but a 1st order bandpass/stop tranformed is oke, however
		% both give just one complex conjugated g(s) root-pair, so just test on
		% only sequence not sufficient: check to see whether H(w-->inf) == 0
		testRoots    = roots_gs( imag(roots_gs) > 0 );
		lenTestRoots = length(testRoots);
		[dummy,imagIx] = sort(imag(testRoots));
		if ( lenTestRoots > 1 )		% order higher than 2
			evenOrderOK = ~all( imagIx' == 1:lenTestRoots );
		else						% if == 1, 2nd order
			poly_fs = Hs.poly_fs;
			degreeNum = length(poly_fs) -1;
			degreeDen = length(poly_gs) -1;
			if ( degreeNum < degreeDen )
				evenOrderOK = ( abs(poly_fs(end)) < ctol ); 
			else
				evenOrderOK = ( ( abs(poly_fs(end)/poly_gs(end) -1.0) < ctol ) & ...
									( abs(poly_fs(1)/poly_gs(1) -1.0) < ctol ) );
			end
		end
		if ~evenOrderOK 
			errStr = 'Even order TRANSFER FUNCTION violation  ...';
			error( errStr );
		end
		% the poles should lie on some part of two circular-like shapes
		% in case the shapes would overlap, which is not allowed, some roots become real
		if ( any( abs( imag(roots_gs) ) < ctol ) )
			if showMessages
				zplane( [], roots_gs );
			end
			errStr = 'Can''t handle circuits with real roots ... ';
			errStr = [ errStr 'Try reducing the BandWidth' ];
			error( errStr );
		end
		% use only those in the upper half of the complex plane (roots are cplx-paired)
		roots_gs = roots_gs(2:2:end);
		if ( length(roots_gs) == 1 )
			transformedLowPass  = 1; 	% 1st order		
		else
			% first re-sort on modulus (like done with MATLAB's sort)
			roots_gs = sort( roots_gs );
			% these roots are in the correct order when calculated via a Vlach bandpass design
			% but not necessarily if they are obtained using a bandpass/stop transformation.
			% In case a transformation has been used, the roots will lie pairwise on straight 
			% starting from the origin.
			[angleSortedRoots,angleSortedIx] = sort( angle(roots_gs) );
			transformedLowPass  = ( abs(angleSortedRoots(2) - angleSortedRoots(1)) < ctol );
		end;
		baseOrder           = orgFilterOrder/2;
		oddOrderBase        = ( rem(baseOrder, 2) == 1 );
		if ( transformedLowPass && oddOrderBase )
			msgStr2 = 'Recognized as a transformedOddFilter ...\n';
			msgStr = [ msgStr msgStr2 ];
			% descending order of angles wanted, first the tranformed real root (if any)
			if ( length(roots_gs) > 1 )
				roots_gs = flipud( roots_gs(angleSortedIx) );
			end
		elseif transformedLowPass		% only remaining vlach bandpasses
				if showMessages
					zplane( [], roots_gs );
				end
				errStr = 'TRANSFORMATIONS from EVEN order lowpass prototypes';
				errStr = [ errStr ' not correctly realizable ...' ];
				error( errStr );
			elseif oddOrderBase
			 	% odd order vlach filter
			 	middleNo = ceil( length(roots_gs)/2 );
			 	tmp = [ roots_gs(middleNo:end); zeros(middleNo-1,1) ]; 
			 	tmp(4:2:end) = tmp(3:1+length(roots_gs)-middleNo);
			 	tmp(3:2:end) = flipud( roots_gs(1:middleNo-1) );
			 	roots_gs = tmp;
		end
		
		% now compute the coefficients for the lwdf architecture
		if oddOrderBase

			A0 = -2*real(roots_gs(1));
			B0 = real(roots_gs(1)).^2 + imag(roots_gs(1)).^2;
			symmetricShape = ( abs(B0 - 1.0) <  100*ctol );
			if symmetricShape 
				y0     = [ (A0-B0-1)/(A0+B0+1); NaN ];
				wdaChr = 'S';
			else
				y0     = [ (A0-B0-1)/(A0+B0+1); (1-B0)/(1+B0) ];
				wdaChr = 'd';
			end
			if ( length(roots_gs) > 1 )
				y = lfRoots2y( roots_gs(2:end), ctol );
				if symmetricShape 
					y1 = y(1,1:2:end);
					y2 = y(2,1:2:end);
					y  = [ -y1.^2; ...
						  ( 2*y1 + ( y2.*(1-y1) ).^2 ) ./ ( 1 + y1.^2 ) ];
					wdaStr = char( 'D' * ones(1,length(y)) );
					nD4Slices = (baseOrder-1)/2;
					if ( rem(nD4Slices,2) == 1 )	% 3,7,11 etc				      
						gamma(:,:,1) = [ y0  y(:,2:2:end-1) ];
						gamma(:,:,2) = y(:,1:2:end);
						codes = [ [ wdaChr wdaStr(2:2:end-1) ];
                					              wdaStr(1:2:end) ];
					else							% 5,9,13 etc
						gamma(:,:,1) = [    y0  y(:,2:2:end)      ];
						gamma(:,:,2) = [ y(:,1:2:end-1) [NaN;NaN] ];
						codes = [ [ wdaChr wdaStr(2:2:end) ];
						          [ wdaStr(1:2:end-1) 'x'  ]  ];
					end					
				else		% asymmetric, only d-type sections
					yIx     = 1;
					rowNo   = 2;
					gammaIx = [ 2; 1 ];
					gamma = NaN * ones( 2,ceil(baseOrder/2), 2 );
					gamma(:,1,1) = y0;
					while ( yIx < size(y,2) )
						gamma(:,gammaIx(rowNo):gammaIx(rowNo)+1,rowNo) = y(:,yIx:yIx+1);
						yIx = yIx + 2;
						gammaIx(rowNo) = gammaIx(rowNo) + 2;
						rowNo = rem(rowNo,2) + 1;
					end
					codes = char( 'd' * ones(2, ceil(baseOrder/2) ) );
					codes(rowNo,end) = 'x';
					if ~transformedLowPass 		% asymmetric bpvlach 6,10,14,18, ... 
						[gamma,codes] = lfInvertIfNeeded(filterOrder,Hs.roots_fs, ...
														min(imag(roots_gs)),gamma,codes);
					end
				end
				
			else		%  length(roots_gs) == 1, so transformed 1st order
				gamma = reshape( [ y0; NaN; NaN ], 2,1,2 );
				codes = [ wdaChr; 'x' ];
			end		

		else			% not 'oddOrderBase'

			% only possible in case of ASYMMETRIC bpvlach 8,12,16,etc, only dd's
			y = lfRoots2y( roots_gs, ctol );
			gamma(:,:,1) = y(:,1:2:end);
			gamma(:,:,2) = y(:,2:2:end);
			codes = char( 'd' * ones(2,length(y)/2) );
			if ~transformedLowPass 		
				[gamma,codes] = lfInvertIfNeeded(filterOrder,Hs.roots_fs, ...
														min(imag(roots_gs)),gamma,codes);
			end	
		end
	
	end					% is lowpass or is bandpass
	
catch
	if showMessages
		error(errStr);
	else
		LWDF = [];
		Hz   = [];
		Messages.warning = msgStr;
		Messages.error   = errStr;
	end
end

if isempty(errStr)
	LWDF.wdaCodes = codes;
	LWDF.gamma    = gamma;
	Hz = LWDF2Hz( LWDF );
	Messages.warning = msgStr;
	Messages.error   = errStr;

	if showMessages
		fprintf( msgStr );
	end

	if ( figNo ~= 0 )
		showLWDF( LWDF, 'L', figNo );
	end
	if exist('plotOptionsString','var')
		if ( ischar(plotOptionsString) && ~isempty(plotOptionsString) )
			eval( ['plotHz(Hz,' plotOptionsString ');'] );
		else
			plotHz( Hz );
		end
	end
end


%==========================================================================================
%=========  LOCAL FUNCTIONS  ==============================================================
%==========================================================================================
function y = lfRoots2y( roots_gs, ctol )
  roots_gs = roots_gs';
  y  = zeros( 2,length(roots_gs) );
  Ai = -2*real(roots_gs);
  Bi = real(roots_gs).^2 + imag(roots_gs).^2;
  y(1,:) = (Ai-Bi-1) ./ (Ai+Bi+1);
  y(2,:) =    (1-Bi) ./ (1+Bi);
  y( abs(y) <= ctol ) = 0;


function [gamma_o,codes_o] = lfInvertIfNeeded(filterOrder,roots_fs,refVal,gamma_i,codes_i)
  invNeeded = ( rem(filterOrder+2,8) == 0 );
  nZerosIn0 = ( sum(abs(imag((roots_fs))) < 1e-10) + 1 ) / 2; 
  posZeros  = imag( roots_fs( imag(roots_fs) > 0 ) );
  if ~isempty(posZeros)
  	  nLowerBandZeros = nZerosIn0 + sum( refVal > posZeros );
  else
  	  nLowerBandZeros = nZerosIn0;
  end
  invNeeded = rem( invNeeded + (rem(nLowerBandZeros,2) == 0), 2 );
  if invNeeded
	  gamma_o(:,:,1) = gamma_i(:,:,2);
	  gamma_o(:,:,2) = gamma_i(:,:,1);
	  codes_o = flipud(codes_i);
  end	
