%% Higher-order realization implementation

clc;
close all;
clear all;

[num, den] =butter(6,0.035,'high'); %Example I
%[num, den] =butter(3,[0.55 0.7]); % Example II

H=tf(num,den,1);
[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});
m=size(Aq,1);

[z p k]=zpkdata(H);
Z=z{1};
P=p{1};



%Z2 (Methode de Gang Li)
% [S2 S2s]  = rhoDFIIt2FWS( H, 0.5*[ones(1,m)], 1);
% S2_H = optim(S2, {'l2scaling' 'no' 'method' 'simplex'  }, @MsensH);
% S2_H.gamma = 2^-4*round(S2_H.gamma*2^4);
% displayR( 'rhoDFIIt - MsensH optimized', S2_H.R)

[S2bis,S2sbis] = rhoDFIIt2FWSrelaxedL2( H, 0.5*[ones(1,m)], 1,  -[ones(1,m)], 1);
S2bis_H = optim(S2bis, {'l2scaling' 'no' 'method' 'simplex'  }, @MsensH);
S2bis_H.gamma = 2^-4*round(S2bis_H.gamma*2^4);
%S2bis_H.gamma = S2_H.gamma;
displayR( 'rhoDFIIt with relaxed L2-scaling- MsensH optimized', S2bis_H.R)

S2sbis.gamma = S2bis_H.gamma;
displayR( 'equivalent state-sapce rhoDFiitwith relaxed L2-scaling- MsensH optimized', S2sbis.R)

% Z4 rho-modal 
S4 = OpModalrho2FWS( ss(H) );
R4 = S4.R;
R4.P = 2^-4 * round( R4.P*2^4);
displayR( 'rho-modal', R4)


% Z3 delta-modal 
R3 = Modaldelta2FWR( ss(H) );
displayR( 'Delta-modal', R3)









