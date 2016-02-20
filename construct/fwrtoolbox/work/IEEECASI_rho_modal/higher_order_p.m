%% Higher-order realization implementation


clc;
close all;
clear all;

[num, den] =butter(4,0.05); %Example I
%[num, den] =butter(3,[0.75 0.9]); % Example II

H=tf(num,den,1);




[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});

m=size(Aq,1);

[z p k]=zpkdata(H);
Z=z{1};
P=p{1};

%Z1 for Example I
 h1=tf(zpk([Z(2) Z(3)],[P(3) P(4)],1));
 h2=tf(zpk([Z(1) Z(4)],[P(1) P(2)],k));

 sys1=canon(h1, 'companion');
R1 = SS2FWR(sys1.A,sys1.B,sys1.C,sys1.D);

sys2=canon(h2, 'companion');
R2 = SS2FWR(sys2.A,sys2.B,sys2.C,sys2.D);

R_c=R2*R1;

%Z1 for Example II
%  h1=tf(zpk([Z(5) Z(6)],[P(3) P(4)],1));
%  h2=tf(zpk([Z(1) Z(4)],[P(5) P(6)],k));
%  h3=tf(zpk([Z(2) Z(3)],[P(1) P(2)],1));
% 
% sys1=canon(h1, 'companion');
% R1 = SS2FWR(sys1.A,sys1.B,sys1.C,sys1.D);
% 
% sys2=canon(h2, 'companion');
% R2 = SS2FWR(sys2.A,sys2.B,sys2.C,sys2.D);
% 
% sys3=canon(h3, 'companion');
% R3 = SS2FWR(sys3.A,sys3.B,sys3.C,sys3.D);
% 
% R_c=R1*R2*R3;



R_c_s= relaxedl2scaling(R_c);
R_c_s = computeW(R_c_s);
MsensH(R_c_s)
MsensPole(R_c_s)
RNG(R_c_s)
[add, mul]= computationalCost(R_c_s)



%Z2 (Methode de Gang Li)
disp('Method of Gang Li');
S = rhoDFIIt2FWS( H, 0.5*[ones(1,m)], 1);
S_rhoDFIIt2 = optim(S, {'l2scaling' 'no' 'method' 'ASA' }, @MsensH);
MsensH(S_rhoDFIIt2.R)
MsensPole(S_rhoDFIIt2.R)


S= rhoDFIIt2FWS( H, [1 0.9375 0.875 0.9375], 1); %optimal gamma for Example I
S= rhoDFIIt2FWS( H, [-0.8125 -0.75 -0.6875 -0.75 -0.75 -0.75], 1); %optimal gamma for Example II


MsensH(S.R)
MsensPole(S.R)
RNG(S.R)
[add, mul]= computationalCost(S.R)
 
% Z3 delta-modal 
R_delta = Modaldelta2FWR( ss(H) );
MsensH(R_delta)
MsensPole(R_delta)
RNG(R_delta)
[add, mul]= computationalCost(R_delta)
 

% Z4 rho-modal 
R4 = OpModalrho2FWR1( ss(H) );


R5=Modalrho2FWR (ss(H), [0.9375 0.9375 0.9375 0.8125],1); %optimal gamma for Example I
R5=Modalrho2FWR (ss(H), [-0.5625 -0.6875 -0.8125 -0.9375 -0.625 -0.875],1); %optimal gamma for Example II

MsensH(R5)
MsensPole(R5)
RNG(R5)
[add, mul]= computationalCost(R5)


 





