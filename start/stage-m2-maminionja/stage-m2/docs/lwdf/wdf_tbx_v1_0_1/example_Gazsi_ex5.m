% This example calculates the 
% "Cauer parameter (elliptical) bireciprocal low-pass filter"
% that has been described in detail by L. Gaszi as Example 5
% in   Explicit Formulas for Lattice Wave Digital Filters,
%      IEEE Trans on Circuits and Systems, Vol. CAS-32, No 1, Jan 1985,
% on pages 83, 85-87.
%
% Parameters taken from Gazsi, are the filter order N=19 and 
% the stopband loss value of 76.89 dB.
%
% Compare the results obtained here with Gazsi's Figures 14a and 14c.
% Note that the numbering of the adaptors and coefficients differs:
%    my_notation |   Gazsi
%    -----------------------
%        y01     |  gamma_3
%        y02     |  gamma_7
%        y03     |  gamma_11
%        y04     |  gamma_15
%        y05     |  gamma_1
%        y06     |  gamma_5
%        y07     |  gamma_9
%        y08     |  gamma_13
%        y09     |  gamma_17


clear all
[Hs,passBandRipple_dB] = Hs_cauer_birec( 19, 76.89 );
LWDF = Hs2LWDF( Hs(1) );

plotHz( LWDF2Hz(LWDF),1,2 );
xy = get( figure(2), 'Position' );		   

plotHz( Hs2Hz( Hs(1) ),1,3 );
set( figure(3), 'Position', [ 1.07 0.95 1 1].*xy );
ca = get( figure(3), 'CurrentAxes' );
set(ca, 'XTick', (0:4:32)/64 );
set(ca, 'XTickLabel', [' 0.0'; ' 4.0'; ' 8.0'; '12.0'; '16.0'; '20.0'; '24.0'; '28.0'; '32.0']);

title( 'Discrete-time Low-Pass Transfer Characteristic' );
xlabel( 'Frequency in kHz' );



    