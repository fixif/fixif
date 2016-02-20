% exemple eusipco
%

[num,den]=butter(2,[0.075 0.09]);
H=tf(8*num,den,-1);
Sys=balreal(ss(H));
S=SS2FWS(Sys);

% optimal realization without L2scaling
S1=optim(S,{'l2scaling','no','method','newton','Display','Iter'},@MsensH)
[M1 MZ1]=MsensH(S1.R);


% S1 with l2-scaling
S2=S1;
[U Y W]=l2scaling(S1.R);
S2.T=S2.T*U;
[M2 MZ2]=MsensH(S2.R);


% opt with strict L2scaling
S3=optim(S1,{'l2scaling','yes','method','newton','Display','Iter'},@MsensH)
[M3 MZ3]=MsensH(S3.R);

% opt with relaxed L2scaling
S4=optim(S,{'l2scaling','relaxed','method','newton','Display','Iter'},@MsensH)
[M4 MZ4]=MsensH(S4.R);

% direct form II
RDF=SS2FWR(ss(H));
[M5 MZ5] = MsensH(RDF);