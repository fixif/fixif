function plotHz(Hz, yAxisMode,figNo,phasePlotMode,nPoints,titleString,legendString)
%PLOTHZ	  Magnitude and phase plots for transfer function(s) in the z-domain.
%	PLOTHZ(Hz) plots the fundamental part of the repetitive magnitude transfer 
%	function Hz with a linear magnitude scale and a normalized frequency scale, 
%	e.g. the actual frequency relative to the sample frequency ( 0 to 0.5 ). 
%	(NB. This corresponds to a range from 0 to pi, for a frequency expressed
%	in radians/sample).
%	Hz has to be entered as a structure, with the following fields:
%		Hz.poly_fz         -- the coefficients of the numerator function
%		Hz.poly_gz         -- the coefficients of the denominator function
%		Hz.ident           -- a string, describing the filter
%		Hz.roots_fz        -- the roots of the numerator 
%		Hz.roots_gz        -- the roots of the denominator
%	where Hz.poly_fz and Hz.poly_gz are vectors of coefficients in either 
%	descending positive powers of z (N,N-1,...,2,1,0), or 
%	ascending negative powers of z (0,-1,-2,...,-(N-1),-N).
%	More than one transfer function can be plotted, by writing the Hz's as a 
%	vector e.g. [Hz1 Hz2]. The colorscheme is dictated by MATLAB.
%	In case Unit Elements (UEs) are involved in the description of Hz, 
%	poly_fz and roots_fz are extended to cell arrays: 
%		Hz.poly_fz  ==> { poly_fz  without UEs; number of UEs }.
%		Hz.roots_fz ==> { roots_fz without UEs; number of UEs }.
%
%	PLOTHZ(Hz,yAxisMode) enables plotting with different vertical scales, viz.
%		axisMode 0 (default mode) uses a linear magnitude axis,
%		axisMode 1 uses a magnitude axis in dB.
%
%	PLOTHZ(Hz,yAxisMode,figNo) also specifies which figure window to use
%
%	PLOTHZ(Hz,yAxisMode,figNo,phasePlotMode) should be used to also plot the 
%	phase transfer characteristics, where 
%		phasePlotMode 0 (default value) means no phase plot,
%		phasePlotMode 1 plots the phase function in a seperate figure,
%		phasePlotMode 2 plots the phase function below the magnitude transfer
%					function in the same figure.
%
%	PLOTHZ(Hz,yAxisMode,figNo,phasePlotMode,nPoints) gives control
%	over the number of points to be calculated for the plot (default 1000).
%
%	PLOTHZ(Hz,yAxisMode,figNo,phasePlotMode,nPoints,titleString)
%	When no titleString is specified, 'Discrete-time Characteristics' is
%	shown above the plot. titleString replaces the word 'Characteristics'
%	with its own text. 
%
%	PLOTHZ(Hz,yAxisMode,figNo,phasePlotMode,nPoints,titleString,legendString)
%	can be used to distinguish combined plots. The legend strings should be 
%	entered as a column vector of strings (same lengths!). 
%
%	Example:
%		Hsn = nlpf('butter',5);
%		Hs1 = nlp2lp(Hsn,fz2fs(0.15));
%		Hz1 = Hs2Hz(Hs1);
%		plotHz(Hz1)
%
%		Hs2 = Hs_vlach(5,1,fz2fs(0.15),fz2fs([0.2 0.25]),2,1);
%		Hz2 = Hs2Hz(Hs2);     
%		plotHz( [Hz1;Hz2], 1,3,2,5000,'Transfer Functions', ...
%								['Butter, N = 5';'Vlach, N5+2UE'])
%
%
% 	See also PLOTHS.
%
%	Warning: When a fairly large number of Unit Elements are being used, the 
%			 accuracy of the output data for normalized frequency values near 
%			 0.5 may deteriorate.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003.
%                                     January 2004: FigNo added


if ~exist('Hz','var')
	error( 'No Hz-data specified ...' );
end
if ( nargin < 7 ),  legendString = [];  end
if ( nargin < 6 ),  titleString = 'Characteristics'; end
if ( nargin < 5 ),  nPoints = 1000;     end
if ( nargin < 4 ),  phasePlotMode = 0;  end
if ( nargin < 3 ),  figNo = 1;          end
if ( nargin < 2 ),  yAxisMode = 0;      end
dBmin = -100;
dBmax =   10;


stepSize = pi/(nPoints-1);
% do not try to plot the very last point in case Unit Elements are involved (see below)
w = 0:stepSize:pi-stepSize;
z = exp(j*w);

nHz  = length(Hz);
Hpsi = zeros(nHz,nPoints-1);

for i = 1:nHz
	poly_fz = Hz(i).poly_fz;
	poly_gz = Hz(i).poly_gz;
	if ~iscell(poly_fz)
		Hpsi(i,:) = polyval(poly_fz,z) ./ polyval(poly_gz,z);
	else
		nUnitElements = poly_fz{2};
		poly_fz       = poly_fz{1};
		% each Unit Element needs an additional multiplication with sqrt(1-W^2),
		%            2   z - 1
		% where W = ---.-------   and T is the sample period. 
		%            T   z + 1
		% According to our definitions, we always use T = 2 (fs=1.0 <==> fz=0.25).
		% Note: for w -> pi, W -> j*infinite, but this should be overruled by
		%       H(z) -> 0
		%       If no special action is taken, problems would arise for 
		%       nUnitElements larger than about 6
%		W = (z - 1)./(z + 1);   	% NOTE: ought to be purely imaginary
%		mulFac = (1 - W.^2) .^ (nUnitElements/2);
% mulFac can be simplified to:
		mulFac = ( 2 ./ (1 + cos(w) ) ) .^ (nUnitElements/2);
		if ( all( mulFac < 1e15 ) )
			Hpsi(i,:) = polyval(poly_fz,z) .* mulFac ./ polyval(poly_gz,z);
		else
			Hp = abs(polyval(poly_fz,z) ./ polyval(poly_gz,z));
			ix = find( mulFac < 1e15);
			ixOK = ix(end);
			% limit problematic data to constant values
			Hp( ixOK+1:end )     = Hp(ixOK);
			mulFac( ixOK+1:end ) = mulFac(ixOK);
			Hpsi(i,:) = Hp .* mulFac;
		end
	end
end

figure( figNo );
if ( phasePlotMode == 2 )
	subplot(2,1, 1);
end

switch yAxisMode
	case 0
		plot(w/2/pi,abs(Hpsi), 'linewidth',1.5);
		axis([0 0.5 0 1.1]);
		ylabel( 'Magnitude' );
	case 1
		warning off
		plot(w/2/pi,20*log10(abs(Hpsi)), 'linewidth',1.5);
		warning on
		axis([0 0.5 dBmin dBmax]);
		ylabel( 'Magnitude in dB' );
	otherwise
		error( 'plotModes 0 or 1 supported (0: lin-lin, 1: lin-log) ...' );
end
grid on

title( [ 'Discrete-time ' titleString] );
xlabel( 'Frequency / Sample Frequency' );
if ~isempty( legendString )
	legend( legendString );
end

if ( phasePlotMode ~= 0 )
	if ( phasePlotMode == 2 )
		subplot(2,1, 2);
	elseif (phasePlotMode == 1 )
		figure( figNo+1 );
	else
		error( 'Unsupported phasePlotMode ...' );
	end
	plot(w/2/pi,180/pi * unwrap(angle(Hpsi),[],2), 'linewidth',1.5);
	axis([0 0.5 ylim]);
	ylabel( 'Phase angle in degrees' );
	grid on
	xlabel( 'Frequency / Sample Frequency' );
	if ( phasePlotMode == 1 )
		title( [ 'Discrete-time ' titleString] );
	end
	if ~isempty( legendString )
		legend( legendString );
	end
end
	