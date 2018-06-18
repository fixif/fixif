function [Hs,wp] = Hs_cauer(N,rp,rs,ftype,Wn,normtd)
%HS_CAUER  Cauer lowpass filter design.
%	Hs = HS_CAUER(filterOrder,passBandRipple_dB,stopBandRipple_dB) 
%	returns a structure Hs describing the continuous-time transfer 
%	function of a normalized (cutoff frequency = 1) Cauer approximation 
%	of the ideal lowpass filter. 
%	The structure Hs is organized as follows:
%		Hs.poly_fs         -- the coefficients of the numerator function
%		Hs.poly_gs         -- the coefficients of the denominator function
%		Hs.ident           -- a string, describing the filter
%		Hs.roots_fs        -- the roots of the numerator 
%		Hs.roots_gs        -- the roots of the denominator
%	where poly_fs and poly_gs are vectors of coefficients in descending 
%	powers of s. 
%	The length of the vector poly_gs equals filterOrder+1, while 
%	that of f(s) depends on the choosen filter type (see below).
%
%	[Hs,wp] = HS_CAUER(filterOrder,passBandRipple_dB,stopBandRipple_dB) 
%	additionally returns the frequencies of the peaks in the passband.
%
%	[..] = HS_CAUER_(filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
%																  skwirMode)
%	Here, the parameter skwirMode indicates the filter type, as described 
%	by Skwirzynski in 1965:
%	An odd order filter is always of type 'A' (also the default value here).
% 	Even order Cauer filters of type 'A' can't be realized with lumped 
%	elements, so in that case the transfer function has to be 'transformed' 
%	using a Skwirzynski transformation. Allowable entries then are 'B' or 'C'.
%	Other implementation methods sometimes can cope with even ordered type 
%	'A' designs. 
%	The length of poly_fs equals filterOrder for odd, type 'A' filters;
%	filterOrder+1 for even, type 'A' filters, or filterOrder-1 for
%	type 'B' or 'C' filters.
%
%	[..] = HS_CAUER(filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
%												  skwirMode,cutOffFrequency)
%	returns the output parameters for the specified denormalized cutoff 
%	frequency.
%
%	[..] = HS_CAUER(filterOrder,passBandRipple_dB,stopBandRipple_dB, ...
%								     skwirMode,cutOffFrequency,freqNormMode)
%	By default the cutoff frequency is normalized to equal 1.0 at that point
%	of the transition slope where the design is 'symmetric' with respect to 
%	the passband and stopband ripple. freqNormMode -1 gives the same output.
%	For freqNormMode 0, the cutoff frequency is defined to be at that point 
%	where the magnitude of the transition slope equals the minima of the 
%	passband ripple. freqNormMode 1 defines the cutoff frequency to be at
%	the -3 dB magnitude level.
%
%	See also HS_BUTTER, HS_CHEBY, HS_INVCHEBY, HS_CAUER_BIREC, HS_VLACH.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003 ...


switch nargin
	case 6
		freqNormMode      = normtd;
		cutOffFrequency   = Wn;
		skwirMode         = upper(ftype);
	case 5
		freqNormMode      = -1;
		cutOffFrequency   = Wn;
		skwirMode         = upper(ftype);
	case 4
		freqNormMode      = -1;
		cutOffFrequency   = 1.0;
		skwirMode         = upper(ftype);
	case 3
		freqNormMode      = -1;
		cutOffFrequency   = 1.0;
		skwirMode         = 'A';
	case 2
		error( 'No stop band ripple specified ...' );
	case 1
		error( 'No pass band ripple specified ...' );
	otherwise
		error( 'No parameters ...' );
end
if ~ischar(skwirMode)
	error( 'Syntax error, skwirMode forgotten? ...' );
end
if ~( (skwirMode == 'A') || (skwirMode == 'B') || (skwirMode == 'C') )
	error( 'Unrecognized skwirMode ...' );
end
filterOrder    = N;
oddFilterOrder = ( rem(filterOrder,2) == 1 );
if oddFilterOrder
	if ~( skwirMode == 'A' )
		fprintf( 'Warning: odd filter order, so always Type ''A'' ...\n' );
		beep;
		skwirMode = 'A';
	end
else								% even filter order	
%	if ~( strcmp(skwirMode,'B') | strcmp(skwirMode,'C') )
%		error( 'Even filter order, so Skwirzynski transformation mode ''B'' or ''C'' needed ...' );
%	end
% as of September 16, 2003
% we will allow for even ordered type 'A' filters, while only issueing a warning ...
	if ~( strcmp(skwirMode,'B') || strcmp(skwirMode,'C') )
		fprintf( 'Warning: EVEN filter order, computed as Type ''A''.\n' )
		fprintf( '         If to be implemented with lumped elements,\n' );
		fprintf( '         Skwirzynski transformation mode ''B'' or ''C'' needed ...\n' );
		beep;
	end
end	
passBandRipple_dB = rp;
stopBandRipple_dB = rs;

clear N rp rs normtd ftype


% determine k from the design specifications
% normalization: Amax <==> 1
% extensions: 2 = squared, r = square root, q = quote
k1  = sqrt( (10^(passBandRipple_dB/10) -1 ) / (10^(stopBandRipple_dB/10) -1) );
K1  = lfAGM_K(k1);
k1q = sqrt(1-k1^2);
if (k1q == 1)
	error( 'Cannot design a filter with this combination of pass band and stop band ripples ...' );
end
K1q = lfAGM_K(k1q);
q   = exp(-pi*K1q/K1/filterOrder);
k   = 4*sqrt(q)*((1+q^2+q^6+q^12)/(1+2*q+2*q^4+2*q^9))^2;

e   = sqrt( 10^(passBandRipple_dB/10) -1 );
k2  = k^2;
kr  = sqrt(k);
kq  = sqrt(1-k2);
K   = lfAGM_K(k);

% calculation of the poles and the characteristic frequencies
% for freqNormMode 1, i.e. w=1 determined by the passband ripple
if oddFilterOrder
	% ellipj.m usually found in $MATLABROOT\toolbox\matlab\specfun\ directory
	O = ellipj( 2*K*(1:(filterOrder-1)/2)/filterOrder, k2);
else
	O = ellipj( (2*(1:filterOrder/2)-1)*K/filterOrder, k2);
end 
O  = O(:);
O2 = O.^2;

v0  = K/filterOrder/K1 * abs( lfAGM_asc( 1/e, k1q ) );
[Sn,Cn] = ellipj( v0, kq^2 );
rho0  = -Sn/Cn;
rho02 = rho0^2;

V = sqrt( (1 - k2*O2) .* (1 - O2) );
W = sqrt( (1 + k2*rho02) * (1 + rho02) );

plh = (rho0*V + j*O*W) ./ (1 + k2*rho02*O2);
[tmp,ix] = sort(abs(real(plh)));
Nplh = length(plh);
poles = zeros(2*Nplh,1);
poles(1:2:2*Nplh)   = plh(ix);
poles(2:2:2*Nplh+1) = conj(plh(ix));
if oddFilterOrder
	poles = [poles; rho0];
end 

wp = sort(O);
ws = flipud(1./(k*wp));

if ( freqNormMode == -1 )
	wp = kr * wp;
	ws = kr * ws;
	poles = kr * poles;
end

% Reference point is "wn=1", so point of symmetry for freqNormMode -1
% or 'passbandripple point' for freqNormMode 0.
% Note: original Skwirzynski transformation method described for 'symmetric' 
%		normalization method, freqNormMode -1
if ~oddFilterOrder
	switch skwirMode
		% Skwirzynski transformations for even order designs
		% ws(end) == inf omitted from ws-vector
		case 'B'
			if ( freqNormMode == -1 )
				Ckwp2 = wp(1)^2;
			else
				Ckwp2 = k2*wp(1)^2;
			end
			wp = sqrt((1-Ckwp2)./(1-Ckwp2*wp.^2)).*wp;
			ws = ws(1:end-1);
			ws = sqrt((1-Ckwp2)./(1-Ckwp2*ws.^2)).*ws;
			poles = sqrt((1-Ckwp2)./(1+Ckwp2*poles.^2)).*poles;

		case 'C'
			wp1_2 = wp(1)^2;
			if ( freqNormMode == -1 )
				Cm  = 1;
				Ckwp1_2 = wp1_2;
			else
				Ckwp1_2 = k2*wp1_2;
				Cm  = sqrt((1-Ckwp1_2)/(1-wp1_2));
			end
			wp2 = wp.^2;
			wp  = Cm*sqrt( (wp2-wp1_2)./(1-Ckwp1_2*wp2) );
			ws2 = ws(1:end-1).^2;
			ws  = Cm*sqrt( (ws2-wp1_2)./(1-Ckwp1_2*ws2) );
			P2  = poles.^2;
			poles = Cm*sqrt( (P2 + wp1_2)./(1 + Ckwp1_2*P2) );
			poles = -conj(poles);
		
		otherwise
			% we will allow for even ordered filters of type 'A'
			% error( 'Shouldn''t reach this point: error using Skwirzynski mode ...' );
	end
else
	wp = [ 0; wp ];		% odd order filter start with a peak at zero frequency
end

roots_fs  = j*[-ws'; ws'];
% make column wise, interleaved -j and +j
roots_fs  = roots_fs(:);
roots_gs  = poles;

K0 = real(prod(-roots_gs)/prod(-roots_fs));
if (~oddFilterOrder && (skwirMode == 'A')) || (skwirMode == 'B')
	K0 = K0 / (10 ^ (passBandRipple_dB/20));
end

if ( freqNormMode == 1 )	% -3 dB mode
	if ( passBandRipple_dB < 3.0103 )
		w3 = lfFind3dbFreq(K0*poly(roots_fs),poly(roots_gs), ...
							1,10^(-passBandRipple_dB/20), 1/k,10^(-stopBandRipple_dB/20) );
	else
		w3 = lfFind3dbFreq(K0*poly(roots_fs),poly(roots_gs), ...
												 wp(end),1, 1,10^(-passBandRipple_dB/20) );
	end
	orgCutOffFrequency = cutOffFrequency;
	cutOffFrequency = cutOffFrequency / w3;
end

% re-order the roots of g(s) to facilitate their use in lwdf-design
roots_gs = flipud(roots_gs);
% adjust for the cutOffFrequency asked for if needed
if ( cutOffFrequency ~= 1.0 )
	wp = cutOffFrequency * wp;
	roots_fs = cutOffFrequency * roots_fs;
	roots_gs = cutOffFrequency * roots_gs;
	K0 = K0 * ( cutOffFrequency ^ ( filterOrder - length(roots_fs) ) );
end

% construct the output polynomials and return the results in a structure Hs
Hs.poly_fs  = K0 * poly(roots_fs);
Hs.poly_gs  = poly(roots_gs);
if ( freqNormMode == 1 )	% -3 dB mode
	cutOffFrequency = orgCutOffFrequency;
end
Hs.ident    = [ 'LP PROTOTYPE: ''cauer'',' num2str(filterOrder) ...
				',' num2str(passBandRipple_dB) ',' num2str(stopBandRipple_dB) ...
				',''' skwirMode ''',' num2str(cutOffFrequency) ',' num2str(freqNormMode) ];
Hs.roots_fs = roots_fs;
Hs.roots_gs = roots_gs;



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
  
  
%==========================================================================================
function u = lfAGM_asc(SC,k)
% Compute the value of u belonging to the inverse elliptical sc-function
% (where sc = sn/cn) with modulus k
% Based on the Arithmetic-Geometric Mean method used for the calculation of
% the 'forward' sn-functions
%
% Huib, October 2002

  tol = eps;    % 2.2204e-016
  a = []; b = []; c = []; fi = [];
  
  a(1) = 1;
  b(1) = sqrt(1-k^2);
  c(1) = k;
  fi(1) = atan(abs(SC));
  i = 1;
  while (abs(c(i)) > tol)
  	  i = i + 1;
	  a(i) = ( a(i-1) + b(i-1) ) / 2;
	  b(i) = sqrt( a(i-1) * b(i-1) );
	  c(i) = ( a(i-1) - b(i-1) ) / 2;
	  fi_x = 2*fi(i-1);
	  fi(i) = atan2( sin(fi_x), c(i)/a(i) + cos(fi_x) );
	  % find the only possible correct value of fi(i) !
	  while (fi(i) < 2*fi(i-1)-pi/2) 
	  	fi(i) = fi(i) + 2*pi;
	  end
  end
  u = sign(SC)*fi(i)/(2^(i-1))/a(i);
  

%==========================================================================================
function w3 = lfFind3dbFreq(fs,gs,x1,y1,x2,y2)
% search the frequency for which the modulus of
% f(s) over g(s) reaches the -3 dB level
  yr = 1/sqrt(2);
  xn = x1 + (y1-yr)/(y1-y2)*(x2-x1);
  yn = abs( polyval(fs,j*xn) ./ polyval(gs,j*xn) );
  cnt = 0;
  while ( ( abs(yr-yn) > 1e-6 ) && (cnt < 25) )
	  if ( yn < yr )
		  x2 = xn;
		  y2 = yn;
	  else
		  x1 = xn;
		  y1 = yn;
	  end
	  xn = x1 + (y1-yr)/(y1-y2)*(x2-x1);
	  yn = abs( polyval(fs,j*xn) ./ polyval(gs,j*xn) );
	  cnt = cnt +1;
  end
  if ( cnt == 25 )
	  error( 'Can''t find -3 dB level ...' );
  end
  w3 = xn;
    