
% filter
Te=1;

% A = [0 1 0 ; 0 0 1; 0.4537681314 -1.556161238 1.974861148];
% B=[0; 0; 1];
% C=[0.0231752363 0.023016947 0.079306721];
% S=ss(A,B,C,0,Te);
% H=tf(S)

[num,den] = butter(2,0.04);
H=tf(num,den,Te);
S=canon(ss(H),'companion');


% input
N=1e6;
u = 8*rand(N,1) + 10*rand(1,1)*ones(N,1);


%======================
% R1 : forme directe II
R1 = SS2FWR( S );
R1 = setFPIS(R1,'DSP16',20);
implementMATLAB(R1,'filterR1')

R1q=quantized(R1);
y1i = filterR1(u);
y1q = realize(R1q,u');

xi1=y1i'-y1q';
Psi1 = psi(xi1)
ONP1 = ONP(R1)


%=========================
% R2 : forme espace d'Žtat
S2 = SS2FWS( balreal(ss(R1)) );
S2.Rini = setFPIS(S2.Rini,'DSP16',20);

opt={'method','ASA','MinMax',1e3};
%S2 = optim( S2, opt, @ONP)
S2.T = [      3.017772759208404e+02    -2.497917057025070e+02
    -2.369725355182113e+02    -1.261516998755145e+02 ];
implementMATLAB(S2.R,'filterR2')

R2q=quantized(S2.R);
y2i = filterR2(u);
y2q = realize(R2q,u');

xi2=y2i'-y2q';
Psi2 = psi(xi2)
ONP2 = ONP(S2.R)



%==================
% R3 : forme delta
Delta = 2^-5;
S3 = SSdelta2FWS( balreal(ss(R1)), Delta);
S3.Rini = setFPIS(S3.Rini,'DSP16',20);
%S3 = optim( S3, opt, @ONP)
S3.T = [
     1.678102734379968e+03    -1.947446825048010e+03
     1.735715983175546e+03     2.820964808821728e+03];
implementMATLAB(S3.R,'filterR3')

R3q=quantized(S3.R);
y3i = filterR3(u);
y3q = realize(R3q,u');

xi3=y3i'-y3q';
Psi3 = psi(xi3)
ONP3 = ONP(S3.R)



