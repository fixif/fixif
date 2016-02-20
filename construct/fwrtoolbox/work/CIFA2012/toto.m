function [A,B,C,D] = toto(g,T,xi,wc)

b0 = g*T^2;
b1 = 2*b0;
b2 = b0;
a0 = 4*xi*wc*T + wc^2*T^2 + 4;
a1 = 2*wc^2*T^2 - 8;
a2 = -4*xi*wc*T + wc^2*T^2 + 4;

A = [ -a1/a0 -a2/a0; 1 0];
B = [1;0];
C = [ (b1*a0-b0*a1)/a0^2 (b2*a0-b0*a2)/a0^2 ];
D = b0/a0;