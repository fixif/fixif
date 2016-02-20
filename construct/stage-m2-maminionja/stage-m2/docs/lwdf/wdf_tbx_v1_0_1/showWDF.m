function showWDF(WDF,dlyLorR,figNo)
%SHOWWDF  Show info and structure of Wave Digital Filter 
%	SHOWWDF(WDF) prints the coefficients of the Wave Digital Filter WDF 
%	in the workspace window, and plots a block diagram of the
%	corresponding filter structure in Figure 1.
%	WDF should be a structure that contain the fields
%		WDF.wdaStruct
%		WDF.wdaNo
%		WDF.mulFacs 
% 	In here, WDF.wdaStruct, describes the WDF block diagram:
%		A WDF block diagram is represented with 2 strings, one describing the
%		adaptors in the signal path (bottom row), the second one (top row) 
%		describing the elements or adaptors connected to the serial or parallel 
%		ports of the first mentioned adaptors.
%		So, the bottom row can only consist of the following codes 
%			's' 	-- for a reflection free 3-port serial adaptor,
%			'p'		-- a reflection free 3-port parallel adaptor,
%			'S'		-- a 3-port serial adaptor with two coefficients,
%			'P'		-- a 3-port parallel adaptor with two coefficients,
%			'm'		-- an output invertor or scaling factor, if needed.
%		For all these adaptors, port 1 is the input, port 3 the (reflection free)
%		output, and port 2 the interface to the top row elements.
%		Each element in the top row string is connected to port 2 of the
%		adaptor in the same position in the bottom row string. Possible
%		codes are:
%			'+'		-- a single delay element (translation of a capacitance),
%			'-'		-- a delay element in series with an inverter (inductance),
%			's' 	-- a reflection free serial adaptor (series LC resonator), 
%			'p'		-- a reflection free parallel adaptor (parallel LC resonator),
%			'S' 	-- a 2-port translation of a serial LC resonance circuit,
%			'P'		-- a 2-port translation of a parallel LC resonance circuit,
%			'x'		-- for an empty slot.
%		With the 's' and 'p' adaptors, port 1 is connected to a single delay 
%		element (translation of the capacitance), port 2 to a delay element in 
%		series with an inverter (the inductance), while the reflection free port 3 
%		is connected to port 2 of the corresponding bottom row adaptor.  
%	WDF.wdaNo defines the numbering of the individual adaptors,
%	WDF.mulFacs lists the multiplication coefficients of the adaptors, starting
%	from adaptor 1. The very last adaptor, which is not reflection free, needs
%	two coefficients, while, if the bottom row string ends with an 'm', the last
%	value will be the scaling coefficient.   
%	
%	SHOWWDF(WDF,dlyLorR) can be used to specify where to draw the first delay when 
%	2-port adaptors are used in the top row (resp. in the left A1 or the rightmost 
%	B1 connection of the top-row adaptor). dlyLorR should be an 'L' or 'R'. If 
%	omitted, an 'L' will be used. 
%
%	SHOWWDF(WDF,dlyLorR,figNo) controls the plot option:
%		figNo = 0 means that no circuit diagram should be shown, while
%		figNo = # results, next to the print, in a circuit diagram in figure(#).
%		
%	See also LADDER2WDF, SHOWLWDF.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, February 2004
%									  Feb 2006, added dlyLorR possibility


if ~exist('dlyLorR','var')	% only needed for top row 2-port adaptors
	dlyLorR = 'L';
else 
	if ~ischar(dlyLorR)
		error( 'showWDF syntax error: dlyLorR should be ''L'' or ''R'' ...');
	end 
	dlyLorR = upper(dlyLorR);
end
if ~exist('figNo','var')
	figNo = 1;  
end

wdaCodes = WDF.wdaStruct;
wdaNo	 = WDF.wdaNo;
if ( wdaCodes(2,end) == 'm' )
	wdaCodes = wdaCodes(:,1:end-1);
	wdaNo    = wdaNo(:,1:end-1);
	alphas   = WDF.mulFacs(1:end-1);
	mulFacB3 = WDF.mulFacs(end);
else
	alphas   = WDF.mulFacs;
	mulFacB3 = 1;
end
nWdas   = max( max( wdaNo ) );
nSlices = size( wdaCodes, 2 );

% test for an asymmetric or a symmetric structure of the 3-ports in the bottom row
% This information has been passed by means of WDF.wdaStruct (== wdaCodes), e.g.
% symmetric: psPsp (P or S in the middle), while asymmetric: pspsP (..at end) 
isSymFlag  = 0;							% first assume NOT symmetric
midSliceNo = nSlices +1;				% and set index past last slice 
if ( rem(nSlices,2) ~= 0 )
	testSliceNo = (nSlices+1)/2;
	if ( wdaCodes(2,testSliceNo) < 'a' )	% 'S' and 'P' are < 'a';  's','p' > 'a'	
		isSymFlag  = 1;
		midSliceNo = testSliceNo;
	end
end


% printout to workspace
[row,clmn] = find( wdaNo > 0 ); 
fprintf( '\n' );
% also handle symmetric WDF's with p.e. a11 - a12 - a13 a33 - a14 - a15 
alphaIx = 1;
for i = 1:nWdas
	nAlphas = 1;
	fprintf( 'Adaptor%2d:  ', i );
	switch wdaCodes(row(i),clmn(i))
		case 's'
			fprintf( '3p serial,   p3 matched :' );
		case 'p'
			fprintf( '3p parallel, p3 matched :' );
		case 'S'
			if ( row(i) == 1 )		% top row 2 port series resonator
				fprintf( '2p, with T_B1 and T_B2  :' );	
			else					% bottom row last adaptor
				fprintf( '3p serial               :' );
				nAlphas = 2;
			end
		case 'P'
			if ( row(i) == 1 )		% top row 2 port parallel resonator
				fprintf( '2p, with T_B1 and -T_B2 :' );	
			else					% bottom row last adaptor
				fprintf( '3p parallel             :' );
				nAlphas = 2;
			end
	end
	fprintf( '  alpha1 = %8.5f\n', alphas(alphaIx) );
	alphaIx = alphaIx +1;
	if (nAlphas == 2) 
		fprintf( '%s alpha3 = %8.5f\n', char(' '*ones(1,38)), alphas(alphaIx) );
		alphaIx = alphaIx +1;
	end
end
if ( lower(wdaCodes(2,1)) == 'p' )
	fprintf( 'Brev needs negation\n' );
end
if ( mulFacB3 ~= 1.0 )
	    fprintf( 'Bfwd multiplier :  m3 = %8.5f\n', mulFacB3 );
end

% display the port connections
fprintf( '\nAdaptor   port1        port2       port3' );
fprintf( '\n-----------------------------------------\n' );
for i = 1:nWdas
	clmnNo = clmn(i);
	if ( row(i) == 1 )   % top row, so resonator
		switch wdaCodes(1,clmnNo)
			case { 's', 'p' }		% 3port adaptor
				p1Str = [ '  T_C' num2str(clmnNo,'%02d') '  ' ];
				p2Str = [ '  -T_L' num2str(clmnNo,'%02d') '  ' ];
				p3Str = [ '3pA(' int2str(wdaNo(2,clmnNo)) ').p2' ];
			case 'S'
				p1Str = [ '3pA(' int2str(wdaNo(2,clmnNo)) ').p2' ];
				p2Str = '   T_p2';
				p3Str = '';
			case 'P'
				p1Str = [ '3pA(' int2str(wdaNo(2,clmnNo)) ').p2' ];
				p2Str = '  -T_p2';
				p3Str = '';
		end
	else
		if ( clmnNo == 1 )
			p1Str = '  A1/B1  ';
		else 
			if ( isSymFlag && (wdaNo(row(i),clmnNo) == nWdas) )
				p1Str = '  A3/B3  ';
			else
				if ( clmnNo <= midSliceNo )
					fromID = int2str(wdaNo(2,clmnNo-1));
				else
					fromID = int2str(wdaNo(2,clmnNo+1));
				end  
	 			p1Str = [ '3pA(' fromID ').p3' ];
		 	end
	 	end
		switch wdaCodes(1,clmnNo)
			case '+'
				p2Str = [ '   T_C' num2str(clmnNo,'%02d') '  ' ];
			case '-'
				p2Str = [ '  -T_L' num2str(clmnNo,'%02d') '  ' ];
			case { 's', 'p' }
	 			p2Str = [ '-3pA(' int2str(wdaNo(1,clmnNo)) ').p3' ];
			case { 'S', 'P' }
				% p0 means: via T to p1
	 			p2Str = [ ' 2pS(' int2str(wdaNo(1,clmnNo)) ').p0' ];
		end
		if ( ~isSymFlag && (wdaNo(row(i),clmnNo) == nWdas) )
			p3Str = '  A3/B3';
		else
			portID = '1';
			if ( clmnNo <= midSliceNo )
				toID   = int2str(wdaNo(2,clmnNo+1));
				if ( clmnNo == midSliceNo )
					portID = '3';
				end
			else
				toID   = int2str(wdaNo(2,clmnNo-1));
			end  
 			p3Str = [ '3pA(' toID ').p' portID ];
	 	end
 	end
 	fprintf( '  %2d    %s   %s   %s\n', i, p1Str, p2Str, p3Str ); 
end
fprintf( '\n' );


% prepare plot of adaptor structure 
sliceWidth = 9.5 * ones(1,nSlices);
for i = 1:nSlices-1
	if ( (wdaCodes(1,i) == 'p') || (wdaCodes(1,i) == 's') )
		if ( (wdaCodes(1,i+1) == 'p') || (wdaCodes(1,i+1) == 's') )
			sliceWidth(i) = 12.5;
		else
			sliceWidth(i) = 11;
		end
	end
end
if ( mulFacB3 ~= 1 )
	sliceWidth = [ sliceWidth 4 ];
end

% check to see whether a plot is wanted
if ( figNo ~= 0 )
	figure( figNo );
	clf
	figPos = get( gcf, 'Position' );
	if any( ( lower(wdaCodes(1,:)) == 's' ) | ( lower(wdaCodes(1,:)) == 'p' ) )
		figHeight = 350;
	else
		figHeight = 250;
	end
	set( gcf, 'Position', [ 100 figPos(2) 13*( sum(sliceWidth) )+150 ...
																figHeight ] );
	set(gca, 'Xtick', [] );
	set(gca, 'XColor', 'White' );
	set(gca, 'Ytick', [] );
	set(gca, 'YColor', 'White' );
	set(gca, 'Position', [0 0 1 1] );
	axis equal
	hx = line( -2,0 );
	set(hx, 'Color','w');

	xn = 6;
	for i = 1:nSlices
		showSym = ( i > midSliceNo );
		switch wdaCodes(1,i)
			case '-'
				lfTopRowDelayL( xn );
			case '+'
				lfTopRowDelayC( xn );
			case { 's', 'p' }
				lfTopRowAdaptor( xn, upper( wdaCodes(1,i) ), wdaNo(1,i) );
			case { 'S', 'P' }
				lfTwoPortSection( xn, dlyLorR, wdaCodes(1,i), wdaNo(1,i) );
		end	
		switch wdaCodes(2,i)
			case 's'
				lfBottomRowAdaptor( xn, 'S', wdaNo(2,i), sliceWidth(i), 1, showSym );
			case 'p'
				lfBottomRowAdaptor( xn, 'P', wdaNo(2,i), sliceWidth(i), 1, showSym );
			case 'S'
				lfBottomRowAdaptor( xn, 'S', wdaNo(2,i), sliceWidth(i), 0, showSym );
			case 'P'
				lfBottomRowAdaptor( xn, 'P', wdaNo(2,i), sliceWidth(i), 0, showSym );
		end
		xn = xn + sliceWidth(i);
	end

	% text for A3-input
	line( xn + [ 0 1 ], [ 3 3 ] );
	text( xn + 1.8, 2.7, 'A_3 = 0', 'FontName','Times New Roman' );
	xrA = xn + 5;
	% output multiplier (if present), arrow and text for B3-output
	if ( mulFacB3 ~= 1 )
		lfGainB3( xn );
		xn = xn + sliceWidth(end);
	end
	line( xn + [ 0 1 NaN 0.2 1 0.2 ], [ 7 7 NaN 7.4 7 6.6 ] );     % -->
	text( xn + 1.8, 6.7, 'B_{fwd}', 'FontName','Times New Roman' );
	xrB = xn + 3;
	% mark rightmost position of figure (some space at the right)
	hx = line( max(xrA,xrB) + 3, 0 );
	set(hx, 'Color','w');

	% extended input line and A1 text
	line( [ 5 6 ], [ 7 7 ] );     
	text( 3, 6.7, 'A_{in}', 'FontName','Times New Roman' );
	% draw B1 inverter -if needed- and text
	if ( lower(wdaCodes(2,1)) == 's' )
		line( [ 5 6 NaN 5.8 5 5.8 ], [ 3 3 NaN 3.4 3 2.6 ] );
		text( 2.6, 2.7, 'B_{rev}', 'FontName','Times New Roman' );
	else
		lfGainB1;
		text( 0, 2.7, 'B_{rev}', 'FontName','Times New Roman' );
	end
end


%==========================================================================================
%=========  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ============
%==========================================================================================

function lfTopRowDelayL( x0 )
  line( x0 + [ 4 6 6 4 4 ], 10 + [ 0 0 2 2 0 ], 'LineWidth',2 );
  text( x0 + 4.5, 11, '-T', 'FontName','Times New Roman', 'FontWeight','bold' );
  line( x0 + [ 3 3 4 NaN 6 7 7 ], [ 10 11 11 NaN 11 11 10 ] );
  line( x0 + [ 2.6 3 3.4 ], 10 + [ -0.8 0 -0.8 ] );    


%==========================================================================================
function lfTopRowDelayC( x0 )
  line( x0 + [ 4 6 6 4 4 ], 10 + [ 0 0 2 2 0 ], 'LineWidth',2 );
  text( x0 + 4.7, 11, 'T', 'FontName','Times New Roman', 'FontAngle','italic' );
  line( x0 + [ 3 3 4 NaN 6 7 7 ], [ 10 11 11 NaN 11 11 10 ] );
  line( x0 + [ 2.6 3 3.4 ], 10 + [ -0.8 0 -0.8 ] );    


%==========================================================================================
function lfTopRowAdaptor( x0, tChar, i )
  % adaptor box
  line( x0 + [ 2 8 8 2 2 ], [ 11 11 17 17 11 ], 'LineWidth',2 );
  % delays
  line( x0 + [ 4 6 6 4 4 ], [ 19 19 21 21 19 ], 'LineWidth',2 );
  text( x0 + 4.7, 20, 'T', 'FontName','Times New Roman', 'FontAngle','italic' );
  line( x0 + [ 10 12 12 10 10 ], [ 13 13 15 15 13 ], 'LineWidth',2 );
  text( x0 + 10.5, 14, '-T', 'FontName','Times New Roman', 'FontWeight','bold' );
  % connection lines
  line( x0 + [ 3 3 4 NaN 6 7 7 ], [ 17 20 20 NaN 20 20 17 ] );
  line( x0 + [ 8 11 11 NaN 11 11 8 ], [ 16 16 15 NaN 13 12 12 ] );
  line( x0 + [ 3 3 NaN 7 7 ], [ 10 11 NaN 10 11 ] );
  line( x0 + 7, 10 );
  % arrows
  line( x0 + [ 2.6 3 3.4 ],  [ 18.2 19 18.2 ] );
  line( x0 + [ 6.6 7 7.4 ],  [ 17.8 17 17.8 ] );
  line( x0 + [ 9.2 10 9.2 ], [ 16.4 16 15.6 ] );
  line( x0 + [ 8.8 8 8.8 ],  [ 12.4 12 11.6 ] );
  line( x0 + [ 2.6 3 3.4 ],  [ 10.2 11 10.2 ] );    
  % matched input
  line( x0 + [ 3 3 ],     [ 11 12 ] );
  line( x0 + [ 2.5 3.5 ], [ 12 12 ], 'LineWidth',3 );
  % port numbers
  text( x0 + 4.8, 16.2, '1', 'FontName','Times New Roman', 'FontSize', 8 );
  text( x0 + 7.0, 14.2, '2', 'FontName','Times New Roman', 'FontSize', 8 );
  text( x0 + 4.8, 11.8, '3', 'FontName','Times New Roman', 'FontSize', 8 );
  % type and ident
  % text( x0 + 4.2, 9.6, '-1', 'FontName','Symbol' );
  if strcmp(upper(tChar),'S')
	% symbolic reference for Serial Adaptor
	line( x0 + [ 3.6 6.4 ], [ 14 14 ] );
	a = (0:30:360) * pi/180;
	R = 0.3;
	line( x0 + 5 + R*cos(a), 14 + R*sin(a) ); 
  else
	% symbolic reference for Parallel Adaptor
	line( x0 + [ 4.7 4.7 ], [ 12.9 15.1 ] ); 
	line( x0 + [ 5.3 5.3 ], [ 12.9 15.1 ] ); 
  end
  text( x0 - 0.8, 18, [ 'A_{' int2str(i) '}.\alpha_1' ], ...
  											'FontName','Times New Roman' );


%==========================================================================================
function lfTwoPortSection( x0, dlyLorR, tChar, i )
  % adaptor box
  line( x0 + [ 2 8 8 2 2 ], [ 14 14 18 18 14 ], 'LineWidth',2 );
  % top most delay ...
  line( x0 + [ 4 6 6 4 4 ], [ 20 20 22 22 20 ], 'LineWidth',2 );
  if ( tChar == 'S' )
	  text( x0 + 4.7, 21,  'T', 'FontName','Times New Roman', 'FontAngle','italic' );
  else
	  text( x0 + 4.5, 21, '-T', 'FontName','Times New Roman', 'FontWeight','bold' );
  end
  %  ... with connection lines
  line( x0 + [ 3 3 4 NaN 6 7 7 ], [ 18 21 21 NaN 21 21 18 ] );
  % ... and arrows
  line( x0 + [ 2.6 3 3.4 ], [ 19.2 20 19.2 ] );
  line( x0 + [ 6.6 7 7.4 ], [ 18.8 18 18.8 ] );
  if ( dlyLorR == 'L' )
    line( x0 + [ 2 4 4 2 2 ], [ 10 10 12 12 10 ], 'LineWidth',2 );	% delay box
    text( x0 + 2.7, 11, 'T', 'FontName','Times New Roman', 'FontAngle','italic' );
    line( x0 + [ 2.6 3 3.4 ], [ 9.2 10 9.2 ] );		% delay in-arrow
    line( x0 + [ 3 3 NaN 7 7 ], [ 12 14 NaN 14 10 ] );	% lines to A1 and from B1
  else
    line( x0 + [ 3 3 NaN 7 7 ], [ 10 14 NaN 14 12 ] );	% lines to A1 and from B1
    line( x0 + [ 6.6 7 7.4 ], [ 12.8 12 12.8 ] );		% delay in-arrow
    line( x0 + [ 6 8 8 6 6 ], [ 10 10 12 12 10 ], 'LineWidth',2 );	% delay box
    text( x0 + 6.7, 11, 'T', 'FontName','Times New Roman', 'FontAngle','italic' );
  end
  line( x0 + [ 2.6 3 3.4 ], [ 13.2 14 13.2 ] );			% adaptor A1-in-arrow

  % port numbers
  text( x0 + 4.2, 17.2, '2', 'FontName','Times New Roman', 'FontSize', 8 );
  text( x0 + 4.2, 14.8, '1', 'FontName','Times New Roman', 'FontSize', 8 );
  % type and ident
  line( x0 + [ 5.2 7.2 ], [ 16 16 ] );
  a = (0:30:360) * pi/180;
  R = 0.2;
  line( x0 + 6.2 + R*cos(a), 16 + R*sin(a) ); 
  line( x0 + [ 5.7 5.7 ], [ 15.1 16.9 ] ); 
  line( x0 + [ 6.7 6.7 ], [ 15.1 16.9 ] ); 

  text( x0 - 0.8, 19, [ 'A_{' int2str(i) '}.\alpha_1' ], ...
  											'FontName','Times New Roman' );


%==========================================================================================
function lfBottomRowAdaptor( x0, tChar, i, xe, matched, showSym )
  % adaptor box
  line( x0 + [ 2 8 8 2 2 ], [ 2 2 8 8 2 ], 'LineWidth',2 );
  % connection lines
  line( x0 + [ 0 2 NaN 8 xe NaN 0 2 NaN 8 xe ], [ 3 3 NaN 3 3 NaN 7 7 NaN 7 7 ] );
  line( x0 + [ 3 3 NaN 7 7 ], [ 8 10 NaN 10 8 ] );
  % arrows
  line( x0 + [ 1.2 2 1.2 ], [ 7.4 7 6.6 ] );     % -->
  line( x0 + [ 6.6 7 7.4 ], [ 8.8 8 8.8 ] );     %
  line( x0 + [ 8.8 8 8.8 ], [ 3.4 3 2.6 ] );     % <--
  if ~showSym
    idStr = '13';
  else
    idStr = '31';
  end
  text( x0 + 2.4, 5.1, idStr(1), 'FontName','Times New Roman', 'FontSize', 8 );
  text( x0 + 4.8, 7.2,   '2',    'FontName','Times New Roman', 'FontSize', 8 );
  text( x0 + 7.1, 5.1, idStr(2), 'FontName','Times New Roman', 'FontSize', 8 );
  text( x0+3, 0.8, [ 'A_{' int2str(i) '}.\alpha_1' ], 'FontName','Times New Roman' );

  if strcmp(upper(tChar),'S')
	% symbolic reference for Serial Adaptor
	line( x0 + [ 3.6 6.4 ], [ 5 5 ] );
	a = (0:30:360) * pi/180;
	R = 0.3;
	line( x0 + 5 + R*cos(a), 5 + R*sin(a) ); 
  else
	% symbolic reference for Parallel Adaptor
	line( x0 + [ 4.7 4.7 ], [ 3.9 6.1 ] ); 
	line( x0 + [ 5.3 5.3 ], [ 3.9 6.1 ] ); 
  end

  % matched input
  if matched
	  if ~showSym
		  line( x0 + [ 7 8 ], [ 3 3 ] );
	  	  line( x0 + [ 7 7 ], [ 2.5 3.5 ], 'LineWidth',3 );
	  else
		  line( x0 + [ 2 3 ], [ 7 7 ] );
	  	  line( x0 + [ 3 3 ], [ 6.5 7.5 ], 'LineWidth',3 );
	  end	  
  else
	  text( x0+3, -0.7, [ 'A_{' int2str(i) '}.\alpha_3' ], 'FontName','Times New Roman' );
  end
  

%==========================================================================================
function lfGainB1
  line( [ 4 6 6 4 ], [ 3 4 2 3 ], 'LineWidth', 2 );
  line( [ 2 4 NaN 2.8 2 2.8 ], [ 3 3 NaN 3.4 3 2.6 ] );
  text( 4.5, 1.2, '-1', 'FontName','Symbol' );
  

%==========================================================================================
function lfGainB3( x0 )
  line( x0 + [ 1 3 1 1 ], [ 6 7 8 6 ], 'LineWidth', 2 );
  line( x0 + [ 0 1 NaN 3 4 ], [ 7 7 NaN 7 7 ] );
  text( x0 + 1.5, 8.7, 'm_3', 'FontName','Times New Roman' );
