function showLadder(Ladder,figNo,figNameString)
%SHOWLADDER   Print the values and plot the schematics of a ladder filter
%	SHOWLADDER(Ladder) prints the element values and plots the schematics
%	of a ladder topology, given in the MATLAB structure Ladder. 
%	Ladder has to contain the fields
%		Ladder.elements		-- a string describing the ladder
%		Ladder.values      	-- a (set of) column vector(s) with the 
%								   element values
%	The elements-string may consist of the following elements:
%		'r' for the source resistance, 'R' for the load resistance,
%		'l' or 'L' for an inductor, 
%		'c' or 'C' for a capacitor, 
%		's' or 'S' for a serial LC-resonator and 
%		'p' or 'P' for a parallel LC-resonator.
%	The lowercase notation is used to identify elements in serie arms,
%	while the uppercase is used for elements in shunt arms.
%	Moreover, also Unit Elements can be present, denoted by a 'U'.
%	The values-vector contains the values of the elements in the same sequence
%	as given in the elements-string. Each resonator circuit needs two values,
%	where always the first one denotes the inductor value and the second one
%	the capacitor value.
%	In case two or more resonator circuits are present, say representing 
%	frequencies f1 and f2, Ladder.values may contain multiple columns, 
%	representing the various permutations of the frequencies 
%	(here column1: f1-f2 and column2: f2-f1).
%
%	SHOWLADDER(Ladder,figNo) indicates which figure to use for the plot.
%
%	SHOWLADDER(Ladder,figNo,figNameString) adds an identification text to the
%	figure's Title Bar.
%
%	See also  LADDERSYNTHESIS

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2004.


if ( nargin < 3 )
	figNameString = '';
end
if ( ( nargin < 2 ) || isempty( figNo ) )
	figNo = 1;
end

elCodes  = Ladder.elements;
elValues = Ladder.values;
nConfigs = size( elValues,2 );
for i = 1:nConfigs
	fprintf( '\n' );
	if ( nConfigs > 1 )
		fprintf( 'Configuration %d:\n', i );
	end
	lfPrintValues( elCodes, elValues(:,i) );
end
lfDrawLadder(elCodes,figNo,figNameString);



%==========================================================================================
%=========  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ======  LOCAL FUNCTIONS  ============
%==========================================================================================

function lfPrintValues(elCodes,elValues)

  str_l = 'in series arm';
  str_v = 'in shunt arm';
  fprintf( '   Rs   %8.5f Ohm\n', elValues(1)  );
  elNo  = 2;
  for i = 1:length(elCodes)-2
	  switch elCodes(i+1)
		  case 'l'
			  fprintf( '   L%02d  %8.5f H   %s\n', i, elValues(elNo), str_l );
		  case 'L'
			  fprintf( '   L%02d  %8.5f H   %s\n', i, elValues(elNo), str_v );
		  case 'c'
			  fprintf( '   C%02d  %8.5f F   %s\n', i, elValues(elNo), str_l );
		  case 'C'
			  fprintf( '   C%02d  %8.5f F   %s\n', i, elValues(elNo), str_v );
		  case 'p'
			  fprintf( '   L%02d  %8.5f H, parallel with\n', i, elValues(elNo) );
			  fprintf( '   C%02d  %8.5f F   %s\n', i, elValues(elNo+1), str_l );
		      elNo = elNo +1;
		  case 'P'
			  fprintf( '   L%02d  %8.5f H, parallel with\n', i, elValues(elNo) );
			  fprintf( '   C%02d  %8.5f F   %s\n', i, elValues(elNo+1), str_v );
		      elNo = elNo +1;
		  case 's'
			  fprintf( '   L%02d  %8.5f H, in series with\n', i, elValues(elNo) );
			  fprintf( '   C%02d  %8.5f F   %s\n', i, elValues(elNo+1), str_l );
		      elNo = elNo +1;
		  case 'S'
			  fprintf( '   L%02d  %8.5f H, in series with\n', i, elValues(elNo) );
			  fprintf( '   C%02d  %8.5f F   %s\n', i, elValues(elNo+1), str_v );
		      elNo = elNo +1;
		  case 'U'
      		  fprintf( '  UE%02d  %8.5f Ohm\n', i, elValues(elNo) );
	  end
      elNo = elNo +1;
  end
  fprintf( '   RL   %8.5f Ohm\n', elValues(end)  );

 
 
%==========================================================================================
function lfDrawLadder(elCodes,figNo,figNameString)

  nElements = length(elCodes);
  figWidth = 17;
  for i = 1:nElements
  	  switch elCodes(i)
  	  	  case { 'L', 'C', 'S' }
  	  	  	  dWidth =  4;
  	  	  case { 'l', 'c' }
  	  	  	  dWidth =  6;
  	  	  case { 'p', 'U' }
  	  	  	  dWidth =  8;
  	  	  case 's'
  	  	  	  dWidth =  9;
  	  	  otherwise
  	  	  	  dWidth = 10;
  	  end
  	  figWidth = figWidth + dWidth;
  end
  xNext = lfDrawLC( 'init', figNo, figNameString, ...
  										[100 500  figWidth*8  250] );
  for i = 1:nElements
	  xNext = lfDrawLC( elCodes(i), xNext, i-1 );
  end	
  lfDrawLC( 'close', xNext   ,figNo );			

%==========================================================================================
function nextStartPos = lfDrawLC( codeString, varargin )

  if ( length(codeString) > 1 )
  	  codeString = upper( codeString );
  end
  switch codeString
	  case 'INIT'
		  figNo    = varargin{1};
		  figNameStr  = varargin{2};
		  figPosition = varargin{3};
	  case 'CLOSE'
		  xLeft       = varargin{1};   
		  figNo    = varargin{2};
	  otherwise		
		  xLeft       = varargin{1};
		  nElement    = varargin{2};
  end

  switch codeString
	  case 'INIT'
		  % prepare the figure for the structure
		  figure( figNo );
		  clf;
		  set(gcf, 'Name', figNameStr );
		  set(gcf, 'Position', figPosition );
		  set(gca, 'Xtick', [] );
		  set(gca, 'XColor', 'White' );
		  set(gca, 'Ytick', [] );
		  set(gca, 'YColor', 'White' );
		  set(gca, 'Position', [0 0 1 1] );
		  axis equal
		  xEnd = 0;
	  case 'CLOSE'
		  h = line( -7,7 );
		  set(h, 'Color','w');
		  h = line( xLeft +10, -17 );
		  set(h, 'Color','w');
		  xEnd = []; 
	  case 'l'
		  xMarks = xLeft + [ 0 1 5 6 ];
		  yMark  = -11;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xMarks(2)   0;
		                xMarks(3) xEnd        0;
		                xMarks(1) xEnd       yMark ] );
		  % the inductor
		  lfSerialArmInductor( xMarks(2), 0, 2 );
		  % identification text
		  lfIdentText( xLeft +2.4, 2.1, sprintf( 'L_{%d}', nElement ) );
	  case 'L'
		  xMarks   = xLeft + [ 0 2 4 ];
		  yMarks   = [ -3.5  -7.5  -11 ];
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xEnd      0;
		                xMarks(1) xEnd  yMarks(end) ] );
		  % vertical connection lines
		  xVertical = xMarks(2);
		  lfVerLines( [ xVertical      0     yMarks(1);
		                xVertical  yMarks(2) yMarks(end) ] );
		  % the inductor
		  lfShuntArmInductor( xVertical, yMarks(1), 2 );
  		  % identification text
		  lfIdentText( xVertical+0.8, -5.6, sprintf( 'L_{%d}', nElement ) );
	  case 'c'
		  xMarks = xLeft + [ 0 2.6 3.4 6 ];
		  yMark  = -11;
		  capWidth = 0.9;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xMarks(2)     0;
		                xMarks(3)   xEnd        0;
		                xMarks(1)   xEnd       yMark ] );
		  % the capacitor
		  yVector = [ -capWidth  capWidth  NaN  -capWidth  capWidth ];
		  lfComponent( [xMarks(2) xMarks(2) NaN xMarks(3) xMarks(3)], yVector, 3 );
		  % identification text
		  lfIdentText( xLeft +2.4, 2.1, sprintf( 'C_{%d}', nElement ) );
	  case 'C'
		  xMarks   = xLeft + [ 0 2 4 ];
		  yMarks   = [ -5.1  -5.9  -11 ];
		  capWidth = 0.9;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xEnd      0;
		                xMarks(1) xEnd  yMarks(end) ] );
		  % vertical connection lines
		  xVertical = xMarks(2);
		  lfVerLines( [ xVertical      0     yMarks(1);
		                xVertical  yMarks(2) yMarks(end) ] );
		  % the capacitor
		  xVector = [ xVertical-capWidth  xVertical+capWidth  NaN ...
		                                     xVertical-capWidth  xVertical+capWidth ];
		  lfComponent( xVector, [yMarks(1) yMarks(1) NaN yMarks(2) yMarks(2)], 3 );
		  % identification text
		  lfIdentText( xVertical+1.4, -5.6, sprintf( 'C_{%d}', nElement ) );
	  case 's'
		  xMarks = xLeft + [ 0 1 5  7.0  7.8  9 ];
		  yMark  = -11;
		  capWidth = 0.9;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xMarks(2)  0;
		                xMarks(3) xMarks(4)  0;
		                xMarks(5) xEnd       0;
		                xMarks(1) xEnd     yMark ] ) ;
		  % the inductor
		  lfSerialArmInductor( xMarks(2), 0, 2 );
		  % the capacitor
		  yVector = [ -capWidth  capWidth  NaN  -capWidth  capWidth ];
		  lfComponent( [xMarks(4) xMarks(4) NaN xMarks(5) xMarks(5)], yVector, 3 );
		  % identification text
		  lfIdentText( xLeft +2.4, 2.1,     sprintf( 'L_{%d}', nElement ) );
		  lfIdentText( xMarks(4) -0.2, 2.1, sprintf( 'C_{%d}', nElement ) );
	  case 'S'
		  xMarks = xLeft + [ 0 2 4 ];
		  yMarks = [ -2.5 -6.5 -8.3 -9 -11 ];
		  capWidth = 0.9;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xEnd       0;
		                xMarks(1) xEnd  yMarks(end) ] );
		  % vertical connection lines
		  xVertical = xMarks(2);
		  lfVerLines( [ xVertical      0     yMarks(1);
		                xVertical  yMarks(2) yMarks(3);
		                xVertical  yMarks(4) yMarks(end) ] );
		  % the inductor
		  lfShuntArmInductor( xVertical, yMarks(1), 2 );
		  % the capacitor
		  xVector = [ xVertical-capWidth  xVertical+capWidth  NaN ...
		                                     xVertical-capWidth  xVertical+capWidth ];
		  lfComponent( xVector, [yMarks(3) yMarks(3) NaN yMarks(4) yMarks(4)], 3 );
		  % identification text
		  lfIdentText( xVertical+1.4, -4.7, sprintf( 'L_{%d}', nElement ) );
		  lfIdentText( xVertical+1.4, -8.7, sprintf( 'C_{%d}', nElement ) );
	  case 'p'
		  xMarks = xLeft + [ 0 1 2 3.6 4.4 6 7 8 ];
		  yMarks = [ 1.5 -1.5 -11 ];
		  capWidth = 0.9;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connecting lines
		  lfHorLines( [ xMarks(1) xMarks(2)   0;
		                xMarks(7) xEnd        0;
		                xMarks(1) xEnd   yMarks(end) ] );
		  % connecting lines from component to component
		  line( [xMarks(3) xMarks(2) xMarks(2) xMarks(4)], ...
			  						[yMarks(1) yMarks(1) yMarks(2) yMarks(2)] );
		  line( [xMarks(6) xMarks(7) xMarks(7) xMarks(5)], ...
									[yMarks(1) yMarks(1) yMarks(2) yMarks(2)] );
		  % the inductor
		  lfSerialArmInductor( xMarks(3), yMarks(1), 2 );
		  % the capacitor
		  yLevel  = yMarks(2);
		  yVector = [ yLevel-capWidth  yLevel+capWidth  NaN ...
											yLevel-capWidth  yLevel+capWidth ];
		  lfComponent( [xMarks(4) xMarks(4) NaN xMarks(5) xMarks(5)], yVector, 3 );
		  % identification text
		  lfIdentText( xMarks(3)+1.4, 3.4,  sprintf( 'L_{%d}', nElement ) );
		  lfIdentText( xMarks(3)+1.4, -3.7, sprintf( 'C_{%d}', nElement ) );
	  case 'P'
		  xMarks = xLeft + [ 0  3.0  5  7.0  10 ];
		  yMarks = [ -2  -3.5  -5.1  -5.9  -7.5  -9  -11 ];
		  capWidth = 0.9;
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connecting lines
		  lfHorLines( [ xMarks(1) xEnd           0;
		                xMarks(2) xMarks(4)  yMarks(1);
		                xMarks(2) xMarks(4)  yMarks(end-1);
		                xMarks(1) xEnd       yMarks(end) ] );
		  % vertical connection lines
		  xVertical = xMarks(3);
		  xL = xMarks(2);
		  xC = xMarks(4);
		  lfVerLines( [ xVertical       0         yMarks(1);
		                   xL       yMarks(1)     yMarks(2);
		                   xL       yMarks(5)     yMarks(6);
		                   xC       yMarks(1)     yMarks(3);
		                   xC       yMarks(4)     yMarks(6);
		                xVertical  yMarks(end-1) yMarks(end) ] );
		  % the inductor
		  lfShuntArmInductor( xL, yMarks(2), 2 );
		  % the capacitor
		  xVector = [ xC-capWidth  xC+capWidth  NaN  xC-capWidth  xC+capWidth ];
		  lfComponent( xVector, [yMarks(3) yMarks(3) NaN yMarks(4) yMarks(4)], 3 );
		  % identification text
		  lfIdentText( xL+0.6, -5.6, sprintf( 'L_{%d}', nElement ) );
		  lfIdentText( xC+1.4, -5.6, sprintf( 'C_{%d}', nElement ) );
	  case 'U'
		  ueWidth  = 4;
		  ueHeight = 13;
		  xMarks   = xLeft + [ 0 2 ueWidth+2 ueWidth+4 ];
		  yMarks   = [ -(11-ueHeight)/2  -(11+ueHeight)/2  -11 ];
		  xUE      = [ 0  ueWidth  ueWidth      0       0 ];
		  yUE      = [ 0      0   -ueHeight  -ueHeight  0 ];
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xEnd       0;
		                xMarks(1) xEnd  yMarks(end) ] );
		  % the Unit Element's block
		  lfComponent( xMarks(2)+xUE, yMarks(1)+yUE, 2 );
		  % identification text
		  lfIdentText( xLeft+2.8, -5.6, sprintf( 'UE_{%d}', nElement ) );
	  case 'r'
		  resWidth  = 3.6;
		  resHeight = 1.15;
		  xMarks    = xLeft + [ 0  1  resWidth+1  resWidth+4 ];
		  yMarks    = [ resHeight/2  -resHeight/2  -11 ];
		  xRes      = [ 0  resWidth   resWidth       0       0 ];
		  yRes      = [ 0     0      -resHeight  -resHeight  0 ];
		  % new horizontal position for next element
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xMarks(2)   0; 
		  			    xMarks(3) xEnd        0; 
		  			    xMarks(1) xEnd   yMarks(end) ] );
		  % the resistor
		  lfComponent( xMarks(2)+xRes, yMarks(1)+yRes, 2 );
		  % identification text
		  lfIdentText( xLeft +2.4, 2.1, 'R_S' );
	  case 'R'
		  xMarks    = xLeft + [ 0 4 ];
		  resWidth  = 0.55;
		  resHeight = 4;
		  yMarks    = [ -(11-resHeight)/2  -(11+resHeight)/2  -11 ];
		  xRes      = [ -resWidth  resWidth  resWidth   -resWidth  -resWidth ];
		  yRes      = [     0         0     -resHeight  -resHeight     0     ];
		  % rightmost horizontal position
		  xEnd = xMarks(end);
		  % horizontal connection lines
		  lfHorLines( [ xMarks(1) xEnd       0;
		                xMarks(1) xEnd  yMarks(end) ] );
		  % vertical connection lines
		  xVertical = xMarks(2);
		  lfVerLines( [ xVertical      0     yMarks(1);
		                xVertical  yMarks(2) yMarks(end) ] );
		  % the resistor 
		  lfComponent( xVertical+xRes, yMarks(1)+yRes, 2 );
		  % identification text
		  lfIdentText( xEnd +1, -5.6, 'R_L' );
  end		 
  nextStartPos = xEnd;	


%==========================================================================================
function lfIdentText(xPos,yPos,identString)
  text( xPos, yPos, identString, 'FontName','Times New Roman' );

%==========================================================================================
function lfHorLines(xyMat)
  penUp = NaN * ones(1,size(xyMat,1));
  xPos  = [      xyMat(:,1:2)';       penUp ];
  yPos  = [ [xyMat(:,3) xyMat(:,3)]'; penUp ];
  line( xPos, yPos, 'Color',[0 0 1] );

%==========================================================================================
function lfVerLines(xyMat)
  penUp = NaN * ones(1,size(xyMat,1));
  xPos = [ [xyMat(:,1) xyMat(:,1)]'; penUp ];
  yPos = [      xyMat(:,2:3)';       penUp ];
  line( xPos, yPos, 'Color',[0 0 1] );

%==========================================================================================
function lfComponent(xVector,yVector,Width)
  line( xVector, yVector, 'LineWidth',Width );

%==========================================================================================
function lfSerialArmInductor(xStart,yStart,Width)
  line( xStart + [ 0  0.067  0.25  0.5  0.75  0.933  1  1.067  1.25  1.5  1.75  1.933 ...
 		     2  2.067  2.25  2.5  2.75  2.933  3  3.067  3.25  3.5  3.75  3.933  4 ], ...
		yStart + [ 0  0.25  0.433  0.5  0.433  0.25  0  0.25  0.433  0.5  0.433  0.25 ...
             0  0.25  0.433  0.5  0.433  0.25  0  0.25  0.433  0.5  0.433  0.25  0 ], ...
        'LineWidth', Width );

%==========================================================================================
function lfShuntArmInductor(xStart,yStart,Width)
  line( xStart - [ 0  0.25  0.433  0.5  0.433  0.25  0  0.25  0.433  0.5  0.433  0.25 ...
		     0  0.25  0.433  0.5  0.433  0.25  0  0.25  0.433  0.5  0.433  0.25  0 ], ...
		yStart - [ 0  0.067  0.25  0.5  0.75  0.933  1  1.067  1.25  1.5  1.75  1.933 ...
		     2  2.067  2.25  2.5  2.75  2.933  3  3.067  3.25  3.5  3.75  3.933  4 ], ...
        'LineWidth', Width );

