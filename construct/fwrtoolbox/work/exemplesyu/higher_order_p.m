%% Higher-order realization implementation


clc;
close all;
clear all;

[num, den] =butter(3,[0.75 0.9]); % Filtre d'ordre 6
%[num, den] =butter(4,0.05);
H=tf(num,den,1);



% Realisation par espace d'etat avec operateur q 
disp('q-based state-space realization with relaxed L2 scaling (without optimization)');
[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});
R_q = SS2FWR(Aq,Bq,Cq,Dq);
R_q = relaxedl2scaling(R_q);
R_q = computeW(R_q);
MsensH(R_q)
MsensPole(R_q)
[add, mul]= computationalCost(R_q)


m=size(Aq,1);




%Methode de Gang Li
disp('Method of Gang Li');
S = rhoDFIIt2FWS( H, 0.5*[ones(1,m)], 1);
S_rhoDFIIt2 = optim(S, {'l2scaling' 'no' 'method' 'ASA' }, @MsensH);
MsensH(S_rhoDFIIt2.R)
MsensPole(S_rhoDFIIt2.R)
%[add, mul]= computationalCost(S_rhoDFIIt2.R)


%S= rhoDFIIt2FWS( H, [-0.8125 -0.75 -0.6875 -0.75 -0.75 -0.75], 1);
S= rhoDFIIt2FWS( H, [1 0.9375 0.875 0.9375], 1);

%S= rhoDFIIt2FWS( H, [1  1 0.9375 0.9375], 1); % Result of Li in paper of 4th-order filter
MsensH(S.R)
MsensPole(S.R)

%RNG
%RNG1(S.R)
[ML2,G] = MLi04( H, [1  1 0.9375 0.9375])
 
% disp('delta-based modal state-space realization with relaxed L2 scaling without optimization ');
R_delta = Modaldelta2FWR( ss(H) );
MsensH(R_delta)
MsensPole(R_delta)
RNG1(R_delta)
%[add, mul]= computationalCost(R_delta)
% 

% 
% disp('\rho-based modal state-space realization with relaxed L2 scaling with global optimization');
% S = Modalrho2FWS( ss(H),[ones(1,m)],1  );
% S_o = optim(S, { 'l2scaling' 'no' 'method' 'ASA' }, @MsensH);
% MsensH(S_o.R)
% MsensPole(S_o.R)
% [add, mul]= computationalCost(S_o.R)


disp('***********************************************************************');

R4 = OpModalrho2FWR( ss(H) );
MsensH(R4)
MsensPole(R4)
[add, mul]= computationalCost(R4)

R5=Modalrho2FWR (ss(H), [-0.5625 -0.6875 -0.8125 -0.9375 -0.625 -0.875],1);
R5=Modalrho2FWR (ss(H), [0.9375 0.9375 0.9375 0.8125],1);
MsensH(R5)
MsensPole(R5)
[add, mul]= computationalCost(R5)

%RNG
RNG1(R5)
