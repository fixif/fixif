% initial matrices
A=[0 1 0; 0 0 1; 0.453770 -1.556160 1.974860];
B=[0; 0; 0.242096];
C=[0.095706 0.095086 0.327556];
D=0.015940;

% modification, to change the Hankel singular values
A(3,1)=0.362;

% structuration
Sys=ss(A,B,C,D,-1);
Sys=canon(Sys,'modal');

S=SS2FWS(Sys);
S.Rini.WZ=ones(size(S.Rini.WZ));

% optimal realization
%Sopt=optim(S,{'l2scaling','no','method','newton','Display','Iter'},@MsensH)
load Sopt

% optimal L2-scaled
%SoptL2=optim(S,{'l2scaling','yes','method','newton','Display','Iter'},@MsensH)
load SoptL2

% optimal L2 relaxed
%SoptL2r=optim(S,{'l2scaling','relaxed','method','newton','Display','Iter'},@MsensH)
load SoptL2r


