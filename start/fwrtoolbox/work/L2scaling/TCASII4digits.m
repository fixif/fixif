A4d = [ 0.3820 0 0; 0 0.7964 0.5598; 0 -0.5598 0.7964 ];
B4d = [ 0.5391; -0.8417; 0.6232 ];
C4d = [ 0.1664 0.1639 0.2047 ];
D4d = 0.0159;

Sys4d = ss(A4d,B4d,C4d,D4d,-1);
S4d = SS2FWS(Sys4d);
S4d.Rini.WZ = ones(4);



%Sopt4d = optim(S4d,{'l2scaling','no','method','newton','Display','Iter'},@MsensH)
load Sopt4d
%SoptL24d = optim(S4d,{'l2scaling','yes','method','newton','Display','Iter'},@MsensH)
load SoptL24d
%SoptL2r4d = optim(S4d,{'l2scaling','relaxed','method','newton','Display','Iter'},@MsensH)
load SoptL2r4d