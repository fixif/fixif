%% Higher-order realization implementation

clc;
close all;
clear all;

%[num, den] =butter(4,0.05); %Example I
[num, den] =butter(3,[0.75 0.9]); % Example II

H=tf(num,den,1);
[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});
m=size(Aq,1);
[z p k]=zpkdata(H);
Z=z{1};
P=p{1};

%Z1 for Example I
% h1=tf(zpk([Z(2) Z(3)],[P(3) P(4)],1));
% h2=tf(zpk([Z(1) Z(4)],[P(1) P(2)],k));
% 
% sys1=canon(h1, 'companion');
% R1 = SS2FWR(sys1.A,sys1.B,sys1.C,sys1.D);
% 
% sys2=canon(h2, 'companion');
% R2 = SS2FWR(sys2.A,sys2.B,sys2.C,sys2.D);
% 
% R_c=R2*R1;


%Z1 for Example II
%  h1=tf(zpk([Z(5) Z(6)],[P(3) P(4)],1));
%  h2=tf(zpk([Z(1) Z(4)],[P(5) P(6)],k));
%  h3=tf(zpk([Z(2) Z(3)],[P(1) P(2)],1));

% h1=tf(zpk([Z(1) Z(2)],[P(3) P(4)],1));
%  h2=tf(zpk([Z(3) Z(4)],[P(5) P(6)],k));
%  h3=tf(zpk([Z(5) Z(6)],[P(1) P(2)],1)); 

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

% R1 = relaxedl2scaling(R_c);
% R1 = computeW(R1);
% displayR( 'cascade 2nd order companion', R1)




%Z2 (Methode de Gang Li)
[S2 S2s]  = rhoDFIIt2FWS( H, 0.5*[ones(1,m)], 1);
%S2_H = optim(S2, {'l2scaling' 'no' 'method' 'newton'  }, @MsensH);
load S2_H_ex2
S2_H.gamma = 2^-4*round(S2_H.gamma*2^4);
displayR( 'rhoDFIIt - MsensH optimized', S2_H.R)



%S2s_H = optim(S2s, {'l2scaling' 'no' 'method' 'newton'  }, @MsensH);
load S2s_H_ex2
S2s_H.gamma = 2^-4*round(S2s_H.gamma*2^4);
displayR( 'equivalent state-sapce rhoDFiit - MsensH optimized', S2s_H.R)


% S2_P = optim(S2, {'l2scaling' 'no' 'method' 'newton'  }, @MsensPole);
% S2_P.gamma = 2^-4*round(S2_H.gamma*2^4);
% displayR( 'rhoDFIIt - MsensPole optimized', S2_P.R)
% 
% S2_R = optim(S2, {'l2scaling' 'no' 'method' 'newton'  }, @MsensPole);
% S2_R.gamma = 2^-4*round(S2_H.gamma*2^4);
% displayR( 'rhoDFIIt - RNG optimized', S2_R.R)


%Z2 bis (Gang Li mais scaling rel�ch�)
S2bis = rhoDFIIt2FWS( H, S2_H.Gamma, 1, -[ones(1,m)], 1);
%S2bis_H = optim(S2bis, {'l2scaling' 'no' 'method' 'newton' 'Display' 'Iter' }, @MsensH);
load S2bis_H_ex2
S2bis_H.gamma = 2^-4*round(S2bis_H.gamma*2^4);
displayR( 'rhoDFIIt with relaxed L2-scaling - MsensH optimized', S2bis_H.R)


 
  
% Z3 delta-modal 
R3 = Modaldelta2FWR( ss(H) );
displayR( 'Delta-modal', R3)



% Z4 rho-modal 
 S4 = OpModalrho2FWS( ss(H) );
 %S4opt = optim( S4, {'Display','Iter','method','convex','Min' 1*[1 1 1 1]', 'Max' [4 4 4 4]'},@MsensH)
 load S4opt_ex2
 R4 = S4opt.R;
R4 = OpModalrho2FWR( ss(H),2*[1 1 1 1 1 1]);
R4.P = 2^-4 * round( R4.P*2^4);
displayR( 'rho-modal', R4)
break

R4bis = setFPIS(R4,'DSP16',10);
implementLaTeX(R4bis)




