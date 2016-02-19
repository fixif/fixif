function [N,rp,rs,ftype,Wn,normtd] = cc2pars(filterOrder,rho,theta,ftype)
%CC2PARS    Convert a Cauer Classification into toolbox parameters
%	[N,rp,rs,ftype,Wn,normtd] = CC2PARS(filterOrder,rho,theta,ftype)
% 	Cauer filters are often classified in a format like	'Cnn t rh ma' 
%	(e.g. 'C06 B 25 47'), in which
%		nn = filterOrder, 
%		t  = type 'A', 'B' or 'C' ('A' sometimes omitted),
%		rh = rho = reflection coefficient as a percentage,
%		ma = theta = modular angle in degrees,
%	while the Cauer functions here need:
%	filterOrder (N), passBandRipple_dB (rp), stopBandRipple_dB (rs),
%	skwirMode (fType), cutOffFrequency (Wn) and freqNormMode (normtd).

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, January 2006

if ~exist('ftype','var')
	ftype = 'A';
else
	ftype = upper(ftype);
	if ~( (ftype == 'B') || (ftype == 'C') )
		error( 'ftype should be ''A'', ''B'' or ''C'' ...' );
	end	
end 
passBandRipple_dB = rho2ripple(rho);

%===============================================================================
% k follows from the given theta (= modular angle)
k   = sin(theta*pi/180);
%===============================================================================
k2  = k^2;
kq  = sqrt(1-k2);
K   = lfAGM_K(k);
Kq  = lfAGM_K(kq);
% Antoniou,  (5.42) and (5.43), page 125
q1  = exp(-pi*filterOrder*Kq/K);
k1  = 4*sqrt(q1)*((1+q1^2+q1^6+q1^12)/(1+2*q1+2*q1^4+2*q1^9))^2;
stopBandRipple_dB = 10*log10( (10^(passBandRipple_dB/10) -1)/(k1^2) +1 );
%===============================================================================

N  = filterOrder;
rp = passBandRipple_dB;
rs = stopBandRipple_dB;
Wn = 1;
normtd = 0;



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
 