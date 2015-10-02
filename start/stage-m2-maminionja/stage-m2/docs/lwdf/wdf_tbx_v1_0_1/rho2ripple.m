function ripple_dB = rho2ripple(rho)
%RHO2RIPPLE  Reflection coefficient to ripple conversion.
%	ripple_dB = RHO2RIPPLE(rho)  converts reflection coefficient 
%	rho (given as a percentage) to pass band ripple in dB
%
%   See also RIPPLE2RHO.

% a.o. Blinchikoff, equation (3.7-5)       
% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, 2002


ripple_dB = -10 * log10( 1 - (rho/100).^2 );   
