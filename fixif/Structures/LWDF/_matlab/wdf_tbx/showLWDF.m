function showLWDF(LWDF,dlyLorR,figNo)
%SHOWLWDF	Display the coefficients and the structure of an LWDF  
%	SHOWLWDF(LWDF) prints the coefficients of the Lattice Wave Digital
%	Filter LWDF in the workspace window, and plots a block diagram of the
%	corresponding filter structure in Figure 1.
%	LWDF should be a structure that contains the fields
%		LWDF.wdaCodes
%		LWDF.gamma, 
%		and an optional LWDF.insRegs field.
%	From these, LWDF.wdaCodes should be an array of 2 strings, which  
%	describe the presence and positions of the adaptors to be used. 
%	The following adaptor combinations are recognized:
%		't' 	-- a single delay element
%		's' 	-- one 2-port and one delay element
%		'S' 	-- one 2-port with two cascaded delay elements
%		'd' 	-- two 2-ports with two delay elements
%		'D' 	-- two 2-ports with two times two cascaded delay elements
%		'x' 	-- only an interconnection in this slot
%	LWDF.gamma gives the coefficient values for the 2-ports.
%	For realistic hardware realizsations, pipeline registers may have been inserted
%	in top and bottom chains. The presence of such register pairs are listed 
%	in an additional vector field LWDF.insRegs ( a 1 means that a register pair
%	should be inserted between this slice and the next one ).
%	
%	SHOWLWDF(WDF,dlyLorR) can be used to specify where to draw the 'connecting' 
%	delay in 2nd degree sections, viz. in the left arm (dlyLorR = 'L') or in the 
%	rightmost arm (dlyLorR = 'R'). If omitted, an 'L' will be used. 
%
%	SHOWLWDF(LWDF,dlyLorR,figNo) controls the plot option:
%		figNo = 0 means that no circuit diagram should be shown, while
%		figNo = # results, next to the print, in a circuit diagram in Figure(#).
%		
%	See also HS2LWDF, LWDF2HZ, LWDF_INSREGS, SHOWWDF.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, February 2004
%	  October 2005:  pipelining made possible by inserting registers
%									  Feb 2006, added dlyLorR possibility


if ~exist('dlyLorR','var')	
	dlyLorR = 'L';
else
	if ~ischar(dlyLorR)
		error( 'showLWDF syntax error: dlyLorR should be ''L'' or ''R'' ...');
	end 
	dlyLorR = upper(dlyLorR);
end
if ~exist('figNo','var')
	figNo = 1;  
end

wdaCodes = LWDF.wdaCodes;
gamma	 = LWDF.gamma;

% determine filter order from description in wdaCodes
codes = wdaCodes(:);
order1 = sum( (codes == 't') | (codes == 's') );
order2 = sum( (codes == 'S') | (codes == 'd') );
order4 = sum( (codes == 'D') );
filterOrder = order1 + 2*order2 + 4*order4;

nTopRowSlices    = sum( wdaCodes(1,:) ~= 'x' );
nBottomRowSlices = sum( wdaCodes(2,:) ~= 'x' );

if isfield(LWDF,'insRegs')
	insRegsVec  = LWDF.insRegs;
	insRegsFlag = 1;
	iRegTop     = 1;
	iRegBottom  = 1;
else
	insRegsFlag = 0;
end;


xn = 0;
sliceWidth = 10;
rowOffset  =  6;

if ( (wdaCodes(1,1) == 'S') || any(any( wdaCodes == 'D' )) )
	lwdfType = 'bpsym';
elseif all( wdaCodes(wdaCodes ~= 'x') == 'd' ) 
		lwdfType = 'bp';
	elseif ( wdaCodes(1,1) == 't' )	
			lwdfType = 'birec';
		elseif ( wdaCodes(1,1) == 's' )
				lwdfType = 'lp';
			else
				wdaCodes
				beep;
				error( 'Unknown filter type ...' );
end
	
		
% printout of structure printout to workspace
% this should contain coefficients that are zero for reasons of clarity
fprintf( '\nStructure appears to be a ' );
switch lwdfType
	case 'lp'
		fprintf( 'lowpass/highpass filter.\n' );
	case 'birec'
		fprintf( 'bireciprocal lowpass/highpass filter.\n' );
	case 'bp'
		fprintf( 'bandpass/bandstop filter.\n' );
	case 'bpsym'
		fprintf( 'symmetrical (around samplefrequency/4) bandpass/bandstop filter.\n' );
end

gammaNo = 1;
fprintf( 'Top row all-pass sections :\n' );
for i = 1:nTopRowSlices
	switch wdaCodes(1,i)
		case 't'
			fprintf( '  single delay\n' );
		case 's'
			fprintf( '  1st degree section       :  y01 = %8.5f\n', gamma(1,1,1) );
			gammaNo = gammaNo + 1;
		case 'S'
			fprintf( '  single section, 2 delays :  y%02d = %8.5f\n', ...
														   gammaNo, gamma(1,i,1) ); 
			gammaNo = gammaNo + 1;
		case 'd'
			fprintf( '  2nd degree section       :  y%02d = %8.5f\n', ...
														   gammaNo, gamma(1,i,1) ); 
			fprintf( '                              y%02d = %8.5f\n', ...
											  			 gammaNo+1, gamma(2,i,1) ); 
			gammaNo = gammaNo + 2;
		case 'D'
			fprintf( '  double section, 2 delays :  y%02d = %8.5f\n', ...
														   gammaNo, gamma(1,i,1) ); 
			fprintf( '                              y%02d = %8.5f\n', ...
											  			 gammaNo+1, gamma(2,i,1) ); 
			gammaNo = gammaNo + 2;
	end
end
fprintf( 'Bottom row all-pass sections :\n' );
if ( nBottomRowSlices >= 1 )
	for i = 1:nBottomRowSlices
		switch wdaCodes(2,i)
		case 'S'
			fprintf( '  single section, 2 delays :  y%02d = %8.5f\n', ...
													       gammaNo, gamma(1,i,2) ); 
			gammaNo = gammaNo + 1;
		case 'd'
			fprintf( '  2nd degree section       :  y%02d = %8.5f\n', ...
														   gammaNo, gamma(1,i,2) ); 
			fprintf( '                              y%02d = %8.5f\n', ...
											  			 gammaNo+1, gamma(2,i,2) ); 
			gammaNo = gammaNo + 2;
		case 'D'
			fprintf( '  double section, 2 delays :  y%02d = %8.5f\n', ...
														   gammaNo, gamma(1,i,2) ); 
			fprintf( '                              y%02d = %8.5f\n', ...
											  			 gammaNo+1, gamma(2,i,2) ); 
			gammaNo = gammaNo + 2;
		otherwise
			wdaCodes
			beep; 
            error( 'Check LWDF.wdaCodes ...' );
		end
	end
else
	fprintf( '  just a straight connection ...\n' );
end


% check to see whether a plot is wanted
if ( figNo ~= 0 )
	figure( figNo );
	clf
	dTopRow    = any(lower(wdaCodes(1,:)) == 'd' );
	dBottomRow = any(lower(wdaCodes(2,:)) == 'd' );
	if ( dTopRow && dBottomRow )
		figHeight = 650;
	elseif ( dTopRow || dBottomRow )
			figHeight = 500;
		else
			figHeight = 380;
	end		
	set( gcf, 'Position', [ 100 150 ...
			   13*( max(nTopRowSlices,nBottomRowSlices)*sliceWidth + 25 )+10 ...
			   figHeight ] );
	set(gca, 'Xtick', [] );
	set(gca, 'XColor', 'White' );
	set(gca, 'Ytick', [] );
	set(gca, 'YColor', 'White' );
	set(gca, 'Position', [0 0 1 1] );
	axis equal
	hx = line( -2,0 );
	set(hx, 'Color','w');

	x0 = lfDrawInput( xn, rowOffset );
	switch (nTopRowSlices - nBottomRowSlices)
		case  0
			x0TopRow 	= x0;
			x0BottomRow = x0;
		case -1
			if insRegsFlag
				xn = x0 + sliceWidth;
				line( [ x0 xn ], ( rowOffset - [ 2 2 ] ) );
				if ( insRegsVec(1) == 1 )
					xn = lfDrawInsertedReg( xn, rowOffset, [ 'RegT' int2str(iRegTop) ], 1 );
				end
				iRegTop = 2;
			else
				xn = x0 + sliceWidth / 2;
				line( [ x0 xn ], ( rowOffset - [ 2 2 ] ) );
			end
			x0TopRow 	= xn;
			x0BottomRow = x0;
		case  1
			if insRegsFlag
				xn = x0 + sliceWidth;
				line( [ x0 xn ], -( rowOffset - [ 2 2 ] ) );
				if ( insRegsVec(1) == 1 )
					xn = lfDrawInsertedReg( xn, rowOffset, ...
													   [ 'RegB' int2str(iRegBottom) ], -1 );
				end
				iRegBottom = 2;
			else
				xn = x0 + sliceWidth / 2;
				line( [ x0 xn ], -( rowOffset - [ 2 2 ] ) );
			end
			x0TopRow 	= x0;
			x0BottomRow = xn;
	end

	xn = x0TopRow;
	gammaNo = 1;
	for i = 1:nTopRowSlices
		switch wdaCodes(1,i)
			case 't'
				lfDelay( xn, rowOffset );
			case 's'
				lf1stDegreeSection( xn, rowOffset, int2str(gammaNo), 1 );
				lfConnect( xn, rowOffset, 1 );
				gammaNo = gammaNo + 1;
			case 'S'
				lfSingle2TSection( xn, rowOffset, int2str(gammaNo), 1 );
				lfConnect( xn, rowOffset, 1 );
				gammaNo = gammaNo + 1;
			case 'd'
				lf2ndDegreeSection( xn, rowOffset, dlyLorR, int2str(gammaNo), 1 );
				lfConnect( xn, rowOffset, 1 );
				gammaNo = gammaNo + 2;
			case 'D'
				lfDouble2TSection( xn, rowOffset, int2str(gammaNo), 1 );
				lfConnect( xn, rowOffset, 1 );
				gammaNo = gammaNo + 2;
		end
		xn = xn + sliceWidth;
		if ( insRegsFlag && (i ~= nTopRowSlices) )
			if ( (insRegsVec(iRegTop) == 1) )
				xn = lfDrawInsertedReg( xn, rowOffset, [ 'RegT' int2str(iRegTop) ], 1 );
			end
			iRegTop = iRegTop +1;
		end
	end
	xeTopRow = xn;

	xn = x0BottomRow;
	for i = 1:nBottomRowSlices
		switch wdaCodes(2,i)
			case 'S'
				lfSingle2TSection( xn, rowOffset, int2str(gammaNo), -1 );
				gammaNo = gammaNo + 1;
			case 'd'
				lf2ndDegreeSection( xn, rowOffset, dlyLorR, int2str(gammaNo), -1 );
				gammaNo = gammaNo + 2;
			case 'D'
				lfDouble2TSection( xn, rowOffset, int2str(gammaNo), -1 );
				gammaNo = gammaNo + 2;
		end
		lfConnect( xn, rowOffset, -1 );
		xn = xn + sliceWidth;
		if ( insRegsFlag && (i ~= nBottomRowSlices) )
			if ( (insRegsVec(iRegBottom) == 1) )
				xn = lfDrawInsertedReg( xn, rowOffset, [ 'RegB' int2str(iRegBottom) ], -1 );
			end
			iRegBottom = iRegBottom +1;
		end
	end
	xn = lfDrawOutputs( xeTopRow, xn, rowOffset, (rem(filterOrder,2) == 1) );
	hx = line( xn + 5, 0 );
	set(hx, 'Color','w');

end % if figure to be shown ...


%==========================================================================================
%=========  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ============
%==========================================================================================

function xe = lfDrawInput( x0, y0 )
  line( x0 + [ 2 5 NaN 6 5 5 6 ], [ 0 0 NaN y0-2 y0-2 -y0+2 -y0+2 ] );
  % arrow
  line( x0 + [ 3.2 4 3.2 ], [ 0.4 0 -0.4 ] );
  text( x0, 1, 'Input', 'FontName','Times New Roman' );
  xe = 6;

%==========================================================================================
function xe = lfDrawOutputs( x1, x2, y0, oddOrder )
  x0 = max(x1,x2);
  line( x0 + [ 7 9 9 7 7 ],    y0 - [ 5 5 1 1 5 ], 'LineWidth',2 ); 
  line( x0 + [ 7 9 9 7 7 ],   -y0 + [ 5 5 1 1 5 ], 'LineWidth',2 ); 
  line( x0 + [ 3 5 3 3 ],      y0 - [ 1 2 3 1 ],   'LineWidth',2 ); 
  line( x0 + [ 11 13 11 11 ],  y0 - [ 4 3 2 4 ],   'LineWidth',2 ); 
  line( x0 + [ 11 13 11 11 ], -y0 + [ 4 3 2 4 ],   'LineWidth',2 ); 
  % connecting lines
  line( [ x1 x0+3 ],  y0 - [ 2 2 ] );
  line( [ x2 x0+7 ], -y0 + [ 2 2 ] );
  line( x0 + [ 4 4 7 ],  -y0 + [ 2 8 8 ] );
  line( x0 + [ 1 1 7 NaN 5 7 ],   y0 - [ 2 8 8 NaN 2 2 ] );
  line( x0 + [ 9 11 NaN 13 15],   y0 - [ 3 3 NaN 3 3 ] );
  line( x0 + [ 9 11 NaN 13 15 ], -y0 + [ 3 3 NaN 3 3 ] );
  % arrows
  line( x0 + [ 6.2 7 6.2 ],    y0 - [ 2.4 2 1.6 ] );
  line( x0 + [ 6.2 7 6.2 ],    y0 - [ 4.4 4 3.6 ] );
  line( x0 + [ 6.2 7 6.2 ],   -y0 + [ 2.4 2 1.6 ] );
  line( x0 + [ 6.2 7 6.2 ],   -y0 + [ 4.4 4 3.6 ] );
  line( x0 + [14.2 15 14.2 ],  y0 - [ 3.4 3 2.6 ] );
  line( x0 + [14.2 15 14.2 ], -y0 + [ 3.4 3 2.6 ] );
  %text info
  text( x0 + 11.2,  y0 - 1, '1/2', 'FontName','Times New Roman' );
  text( x0 + 11.2, -y0 + 1, '1/2', 'FontName','Times New Roman' );
  text( x0 +  3.2,  y0 + 0,  '-1', 'FontName','Symbol' );
  text( x0 +  7.7,  y0 - 3,   '+', 'FontName','Times New Roman' );
  text( x0 +  7.7, -y0 + 3,   '+', 'FontName','Times New Roman' );
  text( x0 + 16.5,   0, 'Outputs', 'FontName','Times New Roman' );
  if oddOrder
  	text( x0 + 15.7,  y0 - 3, 'highpass',  'FontName','Times New Roman' );
  	text( x0 + 15.7, -y0 + 3, 'lowpass', 'FontName','Times New Roman' );
  else
  	text( x0 + 15.7,  y0 - 3, 'bandpass', 'FontName','Times New Roman' );
  	text( x0 + 15.7, -y0 + 3, 'bandstop', 'FontName','Times New Roman' );
  end
  xe = x0 + 19;

%==========================================================================================
function lf1stDegreeSection( x0, y0, numChar, ud )
  % 2port adaptor
  line( x0 + [ 2 8 8 2 2 ], ud*( y0 + [ 0 0 4 4 0 ] ), 'LineWidth',2 );
  % delay element
  line( x0 + [ 4 6 6 4 4 ], ud*( y0 + [ 6 6 8 8 6 ] ), 'LineWidth',2 );
  % connecting lines
  line( x0 + [ 3 3 4 NaN 6 7 7 ], ud*( y0 + [ 4 7 7 NaN 7 7 4 ] ) );
  % arrows
  line( x0 + [ 2.6 3 3.4 ], ud*( y0 + [ 5.2 6 5.2 ] ) );
  line( x0 + [ 6.6 7 7.4 ], ud*( y0 + [ 4.8 4 4.8 ] ) );
  % text info
  text( x0 + 4.7, ud*( y0 + 7 ), 'T', 'FontName','Times New Roman', ...
  														   'FontAngle', 'italic' );
  text( x0 + 4.7, ud*( y0 + 2 ), [ '\gamma_{' numChar '}' ], 'FontName','Symbol' );
  

%==========================================================================================
function lf2ndDegreeSection( x0, y0, dlyLorR, numChar, ud )
  % 2port adaptor
  line( x0 + [ 2 8 8 2 2 ], ud*( y0 + [ 0 0 4 4 0 ] ), 'LineWidth',2 );
  % fixed arrows
  line( x0 + [ 2.6 3 3.4 ], ud*( y0 + [ 9.2 10 9.2 ] ) );
  line( x0 + [ 6.6 7 7.4 ], ud*( y0 + [ 4.8  4 4.8 ] ) );
  if ( dlyLorR == 'L' )
    % delay element in left arm
    line( x0 + [ 2 4 4 2 2 ], ud*( y0 + [ 6 6 8 8 6 ] ), 'LineWidth',2 );
    % connecting lines
    line( x0 + [ 3 3 NaN 3 3 ], ud*( y0 + [ 4 6 NaN 8 10 ] ) );
    line( x0 + [ 7 7 ], ud*( y0 + [ 4 10 ] ) );
    % arrow to delay box
    line( x0 + [ 2.6 3 3.4 ], ud*( y0 + [ 5.2 6 5.2 ] ) );
    % text info
    text( x0 + 2.7, ud*( y0 + 7 ), 'T', 'FontName','Times New Roman', ...
  														   'FontAngle', 'italic' );
  else
    % delay element in right arm
    line( x0 + [ 6 8 8 6 6 ], ud*( y0 + [ 6 6 8 8 6 ] ), 'LineWidth',2 );
    % connecting lines
    line( x0 + [ 3 3 ], ud*( y0 + [ 4 10 ] ) );
    line( x0 + [ 7 7 NaN 7 7 ], ud*( y0 + [ 4 6 NaN 8 10 ] ) );
    % arrow to delay box
    line( x0 + [ 6.6 7 7.4 ], ud*( y0 + [ 8.8 8 8.8 ] ) );
    % text info
    text( x0 + 6.7, ud*( y0 + 7 ), 'T', 'FontName','Times New Roman', ...
  														   'FontAngle', 'italic' );
  end  
  text( x0 + 4.7, ud*( y0 + 2 ), [ '\gamma_{' numChar '}' ], 'FontName','Symbol' );
  % complete with 'odd'-section
  lf1stDegreeSection( x0, y0 + 10, int2str( str2num(numChar) +1 ), ud );


%==========================================================================================
function lfConnect( x0, y0, ud )
  line( x0 + [ 0 3 3 NaN 7 7 10 ], ud*( y0 + [ -2 -2 0 NaN 0 -2 -2 ] ) );
  % arrow
  line( x0 + [ 2.6 3 3.4 ], ud*( y0 + [ -0.8 0 -0.8 ] ) );
  

%==========================================================================================
function lfDelay( x0, y0 )
  line( x0 + [ 4 6 6 4 4 ], y0 + [ -3 -3 -1 -1 -3 ], 'LineWidth',2 );
  text( x0 + 4.7, y0 -2, 'T', 'FontName','Times New Roman', 'FontAngle','italic' );
  % connection lines
  line( x0 + [ 0 4 NaN 6 10 ], y0 + [ -2 -2 NaN -2 -2 ] );
  % arrow
  line( x0 + [ 3.2 4 3.2 ], y0 + [ -1.6 -2 -2.4 ] );


%==========================================================================================
function lfSingle2TSection( x0, y0, numChar, ud )
  % 2port adaptor
  line( x0 + [ 2 8 8 2 2 ], ud*( y0 + [ 0 0 4 4 0 ] ), 'LineWidth',2 );
  % 2T delays element
  line( x0 + [ 3.8 6.2 6.2 3.8 3.8 ], ud*( y0 + [ 6 6 8 8 6 ] ), 'LineWidth',2 );
  % connecting lines
  line( x0 + [ 3 3 3.8 NaN 6.2 7 7 ], ud*( y0 + [ 4 7 7 NaN 7 7 4 ] ) );
  % arrows
  line( x0 + [ 2.6 3 3.4 ], ud*( y0 + [ 5.2 6 5.2 ] ) );
  line( x0 + [ 6.6 7 7.4 ], ud*( y0 + [ 4.8 4 4.8 ] ) );
  % text info
  text( x0 + 4.4, ud*( y0 + 7 ), '2T', 'FontName','Times New Roman', ...
  														    'FontAngle','italic' );
  text( x0 + 4.7, ud*( y0 + 2 ), [ '\gamma_{' numChar '}' ], 'FontName','Symbol' );
  

%==========================================================================================
function lfDouble2TSection( x0, y0, numChar, ud )
  % 2port adaptor
  line( x0 + [ 2 8 8 2 2 ], ud*( y0 + [ 0 0 4 4 0 ] ), 'LineWidth',2 );
  % 2T delays element
  line( x0 + [ 2 4 4 2 2 ], ud*( y0 + [ 5.8 5.8 8.2 8.2 5.8 ] ), 'LineWidth',2 );
  % connecting lines
  line( x0 + [ 3 3 NaN 3 3 ], ud*( y0 + [ 4 5.8 NaN 8.2 10 ] ) );
  line( x0 + [ 7 7 ], ud*( y0 + [ 4 10 ] ) );
  % arrows
  line( x0 + [ 2.6 3 3.4 ], ud*( y0 + [ 5.0 5.8 5.0 ] ) );
  line( x0 + [ 6.6 7 7.4 ], ud*( y0 + [ 4.8 4 4.8 ] ) );
  % text info
  if ( ud == 1 )
  	  yPos = y0 + 6.4;
  else
  	  yPos = -y0 - 7.6;
  end
  text( x0 + 3, yPos, '2T', 'FontName','Times New Roman', ...
										     'FontAngle','italic', 'Rotation',90 );
  text( x0 + 4.7, ud*( y0 + 2 ), [ '\gamma_{' numChar '}' ], 'FontName','Symbol' );
  % complete with 'odd'-section
  lfSingle2TSection( x0, y0 + 10, int2str( str2num(numChar) +1 ), ud );


%==========================================================================================
function xe = lfDrawInsertedReg( x0, y0, idStr, ud )
  line( x0 + [ 0 1 NaN 2 3  ],  ud * (y0-2) * ones(1,5) );
  % arrow
  line( x0 + [ 0.2 1 0.2 ], ud*( y0 - [ 2.4 2 1.6 ] ) );
  patch( x0 + [ 1 2 2 1 1 ], ud*( y0 + [ -3 -3 -1 -1 -3 ] ), 'b' );
  text( x0, ud*(y0-4.1), idStr, 'FontName','Arial','FontSize',8 );
  xe = x0 +3;
