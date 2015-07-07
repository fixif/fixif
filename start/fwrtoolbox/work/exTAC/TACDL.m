% TAC DL

load 'exDL'
Sysp = ss( DL_Plant.A, [DL_Plant.B DL_Plant.B], [DL_Plant.C; DL_Plant.C], 0);

% Forme directe II
disp( 'Forme directe II')
R1 = SS2FWR( canon(DL_Cor,'companion') );
MsensH_cl( R1, Sysp)
MsensPole_cl( R1, Sysp)

% Forme ss equilibree
disp('Forme balancée')
S1 = SS2FWS( balreal(DL_Cor) );
MsensH_cl( S1.R, Sysp)
MsensPole_cl( S1.R, Sysp)

% Forme ss optimale MsensH_cl
disp('Forme ss optimale MsensH_cl')
load S1_H
%S1_H = optim( S1, {'Display','Iter', 'MaxFunEvals',1e5}, @MsensH_cl, Sysp)
MsensH_cl( S1_H.R, Sysp)
MsensPole_cl( S1_H.R, Sysp)

% Forme ss optimale MsensPole_cl
disp('Forme ss optimale MsensPole_cl')
load S1_P   % obtenue sur jerry-01 par S1_P = optim( S1, {'Display','Iter', 'MaxFunEvals',1e5}, @MsensPole_cl, Sysp);
MsensH_cl( S1_P.R, Sysp)
MsensPole_cl( S1_P.R, Sysp)


% Forme rhoDFIIt
warning off
Delta = 2^-5;
S2 = rhoDFIIt2FWS( tf(DL_Cor), ones(10,1), 0, Delta*ones(10,1),1);
disp('Forme rhoDFIIt gamma=0')
S2.Gamma = zeros(10,1); R2a=S2.R;
MsensH_cl( R2a, Sysp)
MsensPole_cl( R2a, Sysp)

disp('Forme rhoDFIIt gamma=1')
S2.Gamma = ones(10,1); R2b=S2.R
MsensH_cl( R2b, Sysp)
MsensPole_cl( R2b, Sysp)


disp('Forme rhoDFIIt optimal MsensPole_cl')
S2.Gamma = [ 0.6261617 ; 0.3288406 ; 0.04442233 ; 0.5848309 ; 0.696381 ; 0.7397787 ; 0.6405012 ; 0.9255434 ; 0.9729877 ; 0.9848002]; R2_P=S2.R;
% obtenu sur pb-thib par S2opt_P = optim( S2, {'method','ASA', 'MinMax',1}, @MsensPole_cl, Sysp)
MsensH_cl( R2_P, Sysp)
MsensPole_cl( R2_P, Sysp)

disp('Forme rhoDFIIt optimal MsensH_cl')
% obtenu par jerry-01 par S2opt_H = optim( S2, {'method','ASA', 'MinMax',1}, @MsensH_cl, Sysp)
R2_H=R2b;
MsensH_cl( R2_H, Sysp)
MsensPole_cl( R2_H, Sysp)