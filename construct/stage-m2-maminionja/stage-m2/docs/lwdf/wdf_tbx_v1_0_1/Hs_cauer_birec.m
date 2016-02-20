function [Hs,passBandRipple_dB,wp,Ws,ws,errorMsg] = Hs_cauer_birec(N,rs,showErrors)
%HS_CAUER_BIREC  Designs a discrete-time Bireciprocal Cauer low/highpass filter.
%	Hs = HS_CAUER_BIREC(filterOrder,stopBandRipple_dB) returns a 
%	structure Hs describing the continuous-time transfer function of 
%	a normalized (cutoff frequency = 1) Cauer approximation of the ideal 
%	lowpass filter, that, when translated into the discrete-time domain and 
%	implemented as a Wave Digital Filter results in a bireciprocal design, 
%	e.g. 'symmetrical' lowpass and higpass transfer characteristics.
%	A bireciprocal design requires that filterOrder is odd, while the 
%	passband ripple will be derived from the specified stopBandRipple_dB.
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s. 
%	Special emphasis is given to the fact that the roots of poly_gs
%	have to be on the unit circle.
%
%	[Hs,passBandRipple_dB,wp,Ws,ws] = HS_CAUER_BIREC(filterOrder, ...
%														stopBandRipple_dB)
%	returns a number of additional parameters, such as the passBandRipple_dB 
%	that is derived from the specified stopBandRipple_dB, the positions of 
%	those frequencies (relative to the Sampling Frequency) in the passband
%	where the magnitude equals 1.0 (wp), the frequency on the transitionband 
%	where the magnitude equals that of the peaks of the stopband ripple (Ws), 
%	and the frequencies of the stopband zeros (ws).
%
%	See also HS_CAUER, HS2LWDF.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003 ...


filterOrder       =  N;
stopBandRipple_dB = rs;
clear N rs
if ~exist('showErrors','var')
	showErrors = 1;
end

try
	if ( rem(filterOrder,2) == 0 )
		errorMsg = 'FilterOrder should be ODD ...'; 
  		error( errorMsg );
	end
	if ~( stopBandRipple_dB > 0 )
		errorMsg = 'stopBandRipple_dB should be positive ...'; 
  		error( errorMsg );
	end
	
	% for information only
	es2 = 10^(stopBandRipple_dB/10) -1;
	passBandRipple_dB = 10*log10(1/es2 +1);

	% determine k from the design specifications
	% extensions: 2 = squared, r = square root, q = quote
	k1  = 1/es2;
	K1  = lfAGM_K(k1);
	k1q = sqrt(1-k1^2);
	if (k1q == 1)
  		errorMsg = 'Stopband ripple specification is too extreme ...';
  		error( errorMsg );
	end
	K1q = lfAGM_K(k1q);
	q   = exp(-pi*K1q/K1/filterOrder);
	k   = 4*sqrt(q)*((1+q^2+q^6+q^12)/(1+2*q+2*q^4+2*q^9))^2;
	k2  = k^2;
	K   = lfAGM_K(k);

	% calculation of the poles of the denominator polynomial
	% first start with Ovec = Sn(...)
	% ellipj.m usually found in $MATLABROOT\toolbox\matlab\specfun\ directory
	Ovec  = ellipj( 2*K*(1:(filterOrder-1)/2)/filterOrder, k2);
	Ovec  = Ovec(:);
	Ovec2 = Ovec.^2;

	V    = sqrt( (1 - k2*Ovec2) .* (1 - Ovec2) );
	WxO  = (k+1)*Ovec;
	angl = atan2( WxO, V );
	plh  = -( cos(angl) + j*sin(angl) );

	% for informational purposes only
	kq = sqrt(k);
	Ws = 1/kq;  
	wp = kq*Ovec;
	ws = flipud(1./wp);

	roots_fs  = j*[-ws'; ws'];
	% make column wise, interleaved -j and +j
	roots_fs  = roots_fs(:);

	Nplh     = length(plh);
	roots_gs = zeros(2*Nplh +1,1);
	% the following ordering is correct for inputs to lwdf.m
	roots_gs(1)            = -1;
	roots_gs(2:2:2*Nplh)   = plh;
	roots_gs(3:2:2*Nplh+1) = conj(plh);

	errorMsg = '';
	% for compatibility reasons return the results in a structure Hs
	poly_fs = poly(roots_fs);
	Hs1.poly_fs  = poly(roots_fs)/poly_fs(end);
	Hs1.poly_gs  = poly(roots_gs);
	Hs1.ident    = [ 'LP PROTOTYPE: ''cauer_birec'',' num2str(filterOrder)	',' num2str(stopBandRipple_dB) ];
	Hs1.roots_fs = roots_fs;
	Hs1.roots_gs = roots_gs;

	Hs2.poly_fs  = [ fliplr(Hs1.poly_fs) 0 ];
	Hs2.poly_gs  = poly(roots_gs);
	Hs2.ident    = [ Hs1.ident '; complementary H(s)' ];
	Hs2.roots_fs = [ 0; flipud(1./roots_fs) ];
	Hs2.roots_gs = roots_gs;

	Hs =[ Hs1 Hs2 ];
	
catch
	if showErrors
		error( errorMsg );
	else
		Hs = [];
		passBandRipple_dB = [];
		wp = [];  
		Ws = [];
		ws = [];
	end

end

%====================================================================================
%======  Local functions  ===========================================================
%====================================================================================

function K = lfAGM_K(k)
% Compute K, the complete elliptic integral of the first kind
% for modulus k.
% Compare with MATLAB's 'ellipke.m': 
%   K = ellipke(k^2) should return the same output value 
% See the several articles about the use of the 
% Arithmetic-Geometric Mean for calculations concerning elliptical functions
%
% Huib, August 2002

  tol = eps;    % 2.2204e-016
  a = []; b = []; c = []; mm = [];
  
  a(1)  = 1;
  b(1)  = sqrt(1-k^2);
  mm(1) = 1;
  i = 1;
  while (mm(i) > tol)
  	  i = i + 1;
  	  a(i) = ( a(i-1) + b(i-1) ) / 2;
	  b(i) = sqrt( a(i-1) * b(i-1) );
	  c(i) = ( a(i-1) - b(i-1) ) / 2;
	  mm(i) = 2^i * c(i)^2;
  end
  K = pi / (2*a(i));
