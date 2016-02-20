% exemple papier L2scaling
%

[num,den]=butter(3,[0.075 0.09]);
H=tf(num,den,-1);
Sys=balreal(ss(H));
S=SS2FWS(Sys);

% optimal realization without L2scaling
%S1=optim(S,{'l2scaling','no','method','fmincon','Display','Iter'},@MsensH)
load S1
[M1 MZ1]=MsensH(S1.R);


% S1 with l2-scaling
S2=S1;
[U Y W]=l2scaling(S1.R);
S2.T=S2.T*U;
[M2 MZ2]=MsensH(S2.R);


% opt with strict L2scaling
%S3=optim(S1,{'l2scaling','yes','method','fmincon','Display','Iter'},@MsensH)
load S3
[M3 MZ3]=MsensH(S3.R);

% opt with relaxed L2scaling
%S4=optim(S,{'l2scaling','relaxed','method','fmincon','Display','Iter'},@MsensH)
