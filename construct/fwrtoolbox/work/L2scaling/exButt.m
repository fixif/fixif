% realisation initial
[num,den]=butter(3,0.4);
H=tf(num,den,1);
Sys=ss(H);

% structuration
S = SS2FWS((52+2/3)*Sys);

% optimal pb
Sl2=optim(S,{'l2scaling','yes','method','fmincon','Display','Iter'},@MsensH)