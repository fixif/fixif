function rho = ripple2rho(ripple)
%RIPPLE2RHO  Ripple to reflection coefficient conversion.
%	rho = RIPPLE2RHO(ripple)  converts pass band ripple in dB
%	to reflection coefficient rho (written as a percentage). 
%
%   See also RIPPLE2RHO.

% a.o. Blinchikoff, equation (3.7-5)       
% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, 2002


rho = 100 * sqrt( 1 - 10.^(-ripple/10) );
