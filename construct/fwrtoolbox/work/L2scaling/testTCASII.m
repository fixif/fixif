A=[0 1 0; 0 0 1; 0.453770 -1.556160 1.974860];
B=[0; 0; 0.242096];
C=[0.095706 0.095086 0.327556];
D=0.015940;

% modification, to change the Hankel singular values
A(3,1)=0.362;

% structuration
Sys=ss(A,B,C,D,-1);
Sys=canon(Sys,'modal');

T=[0 1 0; 0 0 1; 1 0 0];
Sys.A=inv(T)*Sys.A*T; Sys.B=inv(T)*Sys.B;Sys.C=Sys.C*T;
Sys.b=Sys.b-[0.6446;-0.1766;1.648]+[0.5391; -0.8417;0.6232];
Sys.C=Sys.C-[0.1392   0.1653  0.01139] + [0.1664 0.1639 0.2047];

S=SS2FWS(Sys);
S.Rini.WZ=ones(size(S.Rini.WZ));


Sopt=optim(S,{'l2scaling','no','method','newton','Display','Iter'},@MsensH)