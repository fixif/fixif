
clc;
close all;
clear all;

load 'exDL'

m=size(DL_Cor.A,1);
Sysp = ss( DL_Plant.A, [DL_Plant.B DL_Plant.B], [DL_Plant.C; DL_Plant.C],0);

%Z1 (Forme directe II)
R1 = SS2FWR( canon(DL_Cor,'companion') );
R1 = relaxedl2scaling(R1);
R1 = computeW(R1);
displayR_BOBF( 'Forme directe II', R1,Sysp)




%Z2 (Methode de Gang Li)
[S2 S2s]  = rhoDFIIt2FWS( tf(DL_Cor), 0.5*[ones(1,m)], 1);
S2_H = optim(S2, {'method','simplex', 'MinMax',1 }, @MsensH);
S2_H.gamma = 2^-4*round(S2_H.gamma*2^4);
displayR_BOBF( 'rhoDFIIt - MsensH optimized', S2_H.R,Sysp)

 %S2s_H.gamma = S2_H.gamma;
 displayR_BOBF( 'equivalent state-sapce rhoDFiit - MsensH optimized', S2_H.R,Sysp)


% Z3 delta-modal
% R3 = Modaldelta2FWR( DL_Cor.A, DL_Cor.B, DL_Cor.C, DL_Cor.D  );
% displayR( 'Delta-modal', R3)


% Rho delta-modal
 R4 = OpModalrho2FWR( DL_Cor );
 %R4.P = 2^-4 * round( R4.P*2^4 );
 displayR_BOBF( 'rho-modal', R4,Sysp)

%  balanced realization
  R5 = SS2FWR ( balreal ( DL_Cor ) );
  displayR_BOBF( 'balanced realization', R5,Sysp)


% boucle fermée

MsensH_cl( R4, Sysp)
MsensPole_cl( R4, Sysp)
RNG_cl(R4, Sysp)


