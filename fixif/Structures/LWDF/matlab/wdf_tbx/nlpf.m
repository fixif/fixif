function Hs = nlpf(ApproxMethod,filterOrder,varargin)
%NLPF	Design of normalized lowpass filters in the continuous-time domain
%	Hs = NLPF(....) returns a structure Hs describing the continuous-time 
%	transfer function of a normalized (cutoff frequency = 1) approximation 
%	of the ideal lowpass filter. 
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s.
%
%	The syntax of the function is  
%	Hs = NLPF(ApproxMethod,filterOrder, ...variable number of parameters... ) 
%	ApproxMethod can be one of the strings:
%		'butter', 'cheby', 'invcheby', 'cauer' or 'vlach',
%	the number of additional parameters needed being dependant on the chosen
%	approximation method.
%
%	Without going into detail, the set of possible commands will be listed
%	here. Details can be found in the m-files Hs_butter.m, Hs_cheby.m, etc.
% 	
%	Hs = NLPF('butter',filterOrder)
%	Hs = NLPF('cheby',filterOrder,passBandRipple_dB)
%	Hs = NLPF('cheby',filterOrder,passBandRipple_dB,freqNormMode) 
%	Hs = NLPF('invcheby',filterOrder,stopBandRipple_dB)
%	Hs = NLPF('invcheby',filterOrder,stopBandRipple_dB,freqNormMode)
%	Hs = NLPF('cauer',filterOrder,passBandRipple_dB,stopBandRipple_dB,skwirNorm)
%	Hs = NLPF('cauer',filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
%														 skwirNorm,freqNormMode)
%	Hs = NLPF('vlach',filterOrder,passBandRipple_dB)
%	Hs = NLPF('vlach',filterOrder,passBandRipple_dB,stopBandZeros)
%	Hs = NLPF('vlach',filterOrder,passBandRipple_dB,stopBandZeros,nUnitElements)
%	Hs = NLPF('vlach',filterOrder,passBandRipple_dB,stopBandZeros, ...
%													 nUnitElements,freqNormMode)
%
%	See also HS_BUTTER, HS_CHEBY, HS_INVCHEBY, HS_CAUER, HS_VLACH

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003



if ~exist('filterOrder','var')
	error('Filter order should be defined ...' );
end
varLength = length(varargin);

switch lower(ApproxMethod)
%==========================================================================================
	case 'butter'
		Hs = Hs_butter(filterOrder,1.0);

%==========================================================================================
	case 'cheby'
		switch varLength
			case 2
				freqNormMode = varargin{2};					
			case 1
				freqNormMode = 0;					
			case 0
				error( 'No pass band ripple specified ...' );
		end	
		passBandRipple_dB = varargin{1};
		Hs = Hs_cheby(filterOrder,passBandRipple_dB, 1.0, freqNormMode);
	
%==========================================================================================
	case 'invcheby'
		switch varLength
			case 2
				freqNormMode = varargin{2};					
			case 1
				freqNormMode = 0;					
			case 0
				error( 'No stop band ripple specified ...' );
		end	
		stopBandRipple_dB = varargin{1};
		Hs = Hs_invcheby(filterOrder,stopBandRipple_dB, 1.0, freqNormMode);

%==========================================================================================
	case 'cauer'
		skwirMode    = 'A';
		freqNormMode = 0;
		switch varLength
			case 4
				skwirMode    = upper( varargin{3} );
				freqNormMode = varargin{4};
			case 3
				skwirMode    = upper( varargin{3} );
			case 1
				error( 'No stop band ripple specified ...' );
			case 0
				error( 'No pass band ripple specified ...' );
		end	
		passBandRipple_dB = varargin{1};
		stopBandRipple_dB = varargin{2};
		Hs = Hs_cauer(filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
                                                            skwirMode, 1.0, freqNormMode );

%==========================================================================================
	case 'vlach'
		stopBandZeros = [];
		nUnitElements =  0;
		freqNormMode  =  0;
		switch varLength
			case 4
				stopBandZeros = varargin{2};
				nUnitElements = varargin{3};
				freqNormMode  = varargin{4};
			case 3
				stopBandZeros = varargin{2};
				nUnitElements = varargin{3};
			case 2
				stopBandZeros = varargin{2};
			case 0
				error( 'No pass band ripple specified ...' );
		end	
		passBandRipple_dB = varargin{1};
		if ( (filterOrder == 0) && (nUnitElements == 0) )
			error( 'filterOrder 0 only possible if Unit Elements present ...' );
		end
		Hs = Hs_vlach(filterOrder,passBandRipple_dB, ...
                                         1.0, stopBandZeros, nUnitElements, freqNormMode);
	
%==========================================================================================
	otherwise
		error( 'Unknown ApproxMethod ...' );
end
