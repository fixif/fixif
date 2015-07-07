%% Higher-order realization implementation


clc;
close all;
clear all;

%[num, den] =butter(3,[0.75 0.9]); % Filtre d'ordre 6
[num, den] =butter(4,0.05);
H=tf(num,den,1);




% Realisation par espace d'etat avec operateur q 
disp('q-based state-space realization with relaxed L2 scaling (without optimization of sub-sections)');
[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});
R = SS2FWR(Aq,Bq,Cq,Dq);
R = relaxedl2scaling(R);
R = computeW(R);
MsensH(R)
MsensPole(R)
[add, mul]= computationalCost(R)



% Realisation en forme modale avec operateur q 
disp('q-based modal state-space realization with relaxed L2 scaling (without optimization of sub-sections)');
sys=canon(H,'modal');
R_modale = SS2FWR(sys.A,sys.B,sys.C,sys.D);
R_modale= relaxedl2scaling(R_modale);
R_modale = computeW(R_modale);
MsensH(R_modale)
MsensPole(R_modale)
[add, mul]= computationalCost(R_modale)




%Methode de Gang Li
disp('Method of Gang Li');
m=size(Aq,1);
S = rhoDFIIt2FWS( H, [ones(1,m)], 1);
S_rhoDFIIt2 = optim(S, {'l2scaling' 'no' 'method' 'simplex' }, @MsensH);
MsensH(S_rhoDFIIt2.R)
MsensPole(S_rhoDFIIt2.R)
[add, mul]= computationalCost(S_rhoDFIIt2.R)


% Method of Feng 
disp('Method of Feng ^_^ ^_^ ^_^ ^_^ ^_^');
R_yu = Modaldelta2FWR( ss(H) );
MsensH(R_yu)
MsensPole(R_yu)
[add, mul]= computationalCost(R_yu)



S_yu = Modalrho2FWS( ss(H),[ones(1,m)],1  );
S_o = optim(S_yu, { 'l2scaling' 'no' 'method' 'ASA' }, @MsensH);
MsensH(S_o.R)
MsensPole(S_o.R)
[add, mul]= computationalCost(S_o.R)

