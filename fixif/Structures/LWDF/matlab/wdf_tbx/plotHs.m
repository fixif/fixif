function plotHs(Hs, axisMode,figNo,freqInterval,phasePlotMode,nPoints,titleString,legendString)
%PLOTHS	  Magnitude and phase plots for transfer function(s) in the s-domain.
%	PLOTHS(Hs) plots the magnitude of the transfer function Hs with linear axes.
%	Hs has to be entered as a structure, with the following fields:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s. 
%	More than one transfer function can be plotted, by writing the Hs's as a 
%	vector e.g. [Hs1 Hs2]. The colorscheme is dictated by MATLAB.
%	In case Unit Elements (UEs) are involved in the description of Hs, 
%	poly_fs and roots_fs are extended to cell arrays: 
%		Hs.poly_fs  ==> { poly_fs  without UEs; number of UEs }.
%		Hs.roots_fs ==> { roots_fs without UEs; number of UEs }.
%
%	PLOTHS(Hs,axisMode) enables plotting with different scales, viz.
%		axisMode 0 (default mode) uses linear frequency- and magnitude-axes,
%		axisMode 1 uses a linear frequency axis and a magnitude axis in dB,
%		axisMode 2 plots in a logarithmic frequency scale (base 10) with a
%				 	magnitude scale in dBs.
%
%	PLOTHS(Hs,axisMode,figNo) also specifies which figure window to use
%
%	PLOTHS(Hs,axisMode,figNo,freqInterval) gives the user control over the
%	frequency range to be plotted. Default freqInterval values are [0 5] for 
%	linear, [0.01 100] for logarithmic plots. 
%	A freqInterval [] signals to use the default values.
%
%	PLOTHS(Hs,axisMode,figNo,freqInterval,phasePlotMode) should be used to 
%	also plot the phase transfer characteristics, where 
%		phasePlotMode 0 (default value) means no phase plot,
%		phasePlotMode 1 plots the phase function in a seperate figure,
%		phasePlotMode 2 plots the phase function below the magnitude transfer
%					function in the same figure.
%
%	PLOTHS(Hs,axisMode,figNo,freqInterval,phasePlotMode,nPoints) gives control
%	over the number of points to be calculated for the plot (default 1000).
%
%	PLOTHS(Hs,axisMode,figNo,freqInterval,phasePlotMode,nPoints,titleString)
%	When no titleString is specified, 'Continuous-time Characteristics' is
%	shown above the plot. titleString replaces the word 'Characteristics'
%	with its own text. 
%
%	PLOTHS(Hs,axisMode,figNo,freqInterval,phasePlotMode,nPoints,titleString, ...
%																legendString)
%	can be used to distinguish combined plots. The legend strings should be 
%	entered as a column vector of strings (same lengths!). 
%
%	Example:
%		Hs1 = nlpf('butter',5);
%		plotHs(Hs1)
%
%		Hs2 = nlpf('vlach',5,1,[2.0 3.0],1,1);
%		plotHs( [Hs1;Hs2], 2,1,[],2,5000,'Transfer Functions', ...
%										['Butter, N = 5';'Vlach, N5+1UE'])
%
% 	See also PLOTHZ.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003
%                                     January 2004: FigNo added


if ~exist('Hs','var')
	error( 'No Hs-data specified ...' );
end
if ( nargin < 2 ),  axisMode = 0;       end
if ( nargin < 8 ),  legendString = [];  end
if ( nargin < 7 ),  titleString = 'Characteristics'; end
if ( nargin < 6 ),  nPoints = 1000;     end
if ( nargin < 5 ),  phasePlotMode = 0;  end
if ( nargin < 4 )
	if ( axisMode == 2 )
		freqInterval = [0.01  100];
	else
		freqInterval = [0 5];
	end
end
if ( nargin < 3 ),  figNo = 1;  end
dBmin = -100;
dBmax =   10;

if ( axisMode == 2 )
	if isempty( freqInterval )		% use default values
		freqInterval = [0.01  100];
	end	
	w = logspace( log10(freqInterval(1)), log10(freqInterval(2)), nPoints );
elseif ( axisMode <= 1 )
	if isempty( freqInterval )		% use default values
		freqInterval = [0 5];
	end	
	w = linspace( freqInterval(1), freqInterval(2), nPoints );
else
	error( 'axisModes 0 to 2 supported (0: lin-lin, 1: lin-log, 2: log-log) ...' );
end


jw  = j * w;
nHs = length(Hs);
Hw  = zeros(nHs,nPoints);
for i = 1:nHs
	poly_fs = Hs(i).poly_fs;
	poly_gs = Hs(i).poly_gs;
	if ~iscell(poly_fs)
		Hw(i,:) = polyval(poly_fs,jw) ./ polyval(poly_gs,jw);
	else
		nUnitElements = poly_fs{2};
		poly_fs       = poly_fs{1};
		% each Unit Element needs an additional multiplication with sqrt(1+w^2),
		mulFac = (1 + w.^2) .^ (nUnitElements/2);
		Hw(i,:) = polyval(poly_fs,jw) .* mulFac ./ polyval(poly_gs,jw);
	end
end


figure( figNo );
if ( phasePlotMode == 2 )
	subplot(2,1, 1);
end

switch axisMode
	case 0
		plot( w, abs(Hw), 'linewidth',1.5);
		axis([xlim 0 1.1]);
		ylabel( 'Magnitude' );
	case 1
		warning off
		plot( w, 20*log10(abs(Hw)), 'linewidth',1.5);
		warning on
		axis([xlim dBmin dBmax]);
		ylabel( 'Magnitude in dB' );
	case 2
		warning off
		semilogx( w, 20*log10(abs(Hw)), 'linewidth',1.5);
		warning on
		axis([freqInterval(1) freqInterval(2) dBmin dBmax]); 
		ylabel( 'Magnitude in dB' );
	otherwise
		error( 'plotModes 0 to 2 supported (0: lin-lin, 1: lin-log, 2: log-log) ...' );
end
grid on

title( [ 'Continuous-time ' titleString] );
xlabel( 'Frequency' );
if ~isempty( legendString )
	legend( legendString );
end

% Note that a Unit Elements doesn't change phase angles, 
% since sqrt(1+w^2) is positive real for each w (angle=0)
if ( phasePlotMode ~= 0 )
	if ( phasePlotMode == 2 )
		subplot(2,1, 2);
	elseif ( phasePlotMode == 1 )
		figure( figNo+1 );
	else
		error( 'Unsupported phasePlotMode ...' );
	end
	if ( axisMode ~= 2 )
		plot( w, 180/pi * unwrap(angle(Hw),[],2), 'linewidth',1.5);
	else
		semilogx( w, 180/pi * unwrap(angle(Hw),[],2), 'linewidth',1.5);
		axis([freqInterval(1) freqInterval(2) ylim]); 
	end		
	ylabel( 'Phase angle in degrees' );
	grid on
	xlabel( 'Frequency' );
	if ( phasePlotMode == 1 )
		title( [ 'Continuous-time ' titleString] );
	end
	if ~isempty( legendString )
		legend( legendString );
	end
end
	