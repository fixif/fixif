%% Effect FWL

clc;
close all;
clear all;

Nbbits=16;


% initial filter
[num, den] =butter(3,[0.75 0.9]); % Filtre d'ordre 6
H=tf(num,den,-1);
[Aq,Bq,Cq,Dq] = tf2ss(H.num{1},H.den{1});


% % SSdelta (from DFIIq)
% R1 = SSdelta2FWR( ss(Aq,Bq,Cq,Dq), 2^(-3));
% R1 = setFPIS( R1, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
% [R1q, DeltaZ] = quantized( R1);
% 
% 
% % balanced SS
% [sysb,g] = balreal(ss(Aq,Bq,Cq,Dq));
% R2 = SS2FWR( sysb);
% R2 = setFPIS( R2, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
% [R2q, DeltaZ] = quantized( R2);
% 
% 
% % Direct Form I q
% R3 = DFIq2FWR( H );
% R3 = setFPIS( R3, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
% [R3q, DeltaZ] = quantized( R3);
% 
% 
% % plot
% figure(1)
% hold on;
% AXIS([10^(-4) 10 -300 20])
% bodemag(H)
% bodemag(tf(R1q))
% bodemag(tf(R2q))
% bodemag(tf(R3q))
% legend('H reference','forme SS en \delta','forme equilibree', 'forme directe I', 2 );
% hold off;

S= rhoDFIIt2FWS( H, [0 0 0 0 0 0], 1);
R1 = setFPIS( S.R, 32, 1,Nbbits , 32, 32, 32, 32, 32, 'RAM' );
[R1q, DeltaZ] = quantized( R1);

S= rhoDFIIt2FWS( H, [1 1 1 1 1 1],1);
R2 = setFPIS( S.R, 32, 1,Nbbits , 32, 32, 32, 32, 32, 'RAM' );
[R2q, DeltaZ] = quantized(R2);

S= rhoDFIIt2FWS( H, [-0.8125 -0.75 -0.6875 -0.75 -0.75 -0.75], 1);
R3 = setFPIS( S.R, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
[R3q, DeltaZ] = quantized(R3);


% plot
figure(1)
w0=0:0.01:pi; 
repf=freqz(num,den,w0); 

[num,den] = ss2tf(R1q.AZ,R1q.BZ,R1q.CZ,R1q.DZ);
repf1=freqz(num,den,w0); 

[num,den] = ss2tf(R2q.AZ,R2q.BZ,R2q.CZ,R2q.DZ);
repf2=freqz(num,den,w0); 

[num,den] = ss2tf(R3q.AZ,R3q.BZ,R3q.CZ,R3q.DZ);
repf3=freqz(num,den,w0); 

plot(w0/2/pi,20*log10(abs(repf)),w0/2/pi,20*log10(abs(repf1)),w0/2/pi,20*log10(abs(repf2)),w0/2/pi,20*log10(abs(repf3)))
legend('H reference', 'qDFIIt', '\deltaDFII','\rhoDFIIt', 1 );
AXIS([.35 0.5 -15 5])
grid on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Example in the end %%%%%%%%%%%%%%%%%%%%%%%



% Cascad form
[z p k]=zpkdata(H);

Z=z{1};
P=p{1};

 h1=tf(zpk([Z(1) Z(2)],[P(3) P(4)],1));
 h2=tf(zpk([Z(3) Z(4)],[P(5) P(6)],k));
 h3=tf(zpk([Z(5) Z(6)],[P(1) P(2)],1));

sys1=canon(h1, 'companion');
TR1 = SS2FWR(sys1.A,sys1.B,sys1.C,sys1.D);
sys2=canon(h2, 'companion');
TR2 = SS2FWR(sys2.A,sys2.B,sys2.C,sys2.D);
sys3=canon(h3, 'companion');
TR3 = SS2FWR(sys3.A,sys3.B,sys3.C,sys3.D);

R4=TR1*TR2*TR3;
R4= relaxedl2scaling(R4);

R4 = setFPIS( R4, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
[R4q, DeltaZ] = quantized( R4);


% rho Direct Form II transposed
S= rhoDFIIt2FWS( H, [-0.8125 -0.75 -0.6875 -0.75 -0.75 -0.75], 1);
R5 = setFPIS( S.R, 32, 1, 11, 32, 32, 32, 32, 32, 'RAM' );
[R5q, DeltaZ] = quantized( R5);


% modal delta
R_delta = Modaldelta2FWR( ss(H) );
R6 = setFPIS( R_delta, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
[R6q, DeltaZ] = quantized( R6);


% modal rho
R7=Modalrho2FWR (ss(H), [-0.5625 -0.6875 -0.8125 -0.9375 -0.625 -0.875],1);
R7 = setFPIS( R7, 32, 1, Nbbits, 32, 32, 32, 32, 32, 'RAM' );
[R7q, DeltaZ] = quantized( R7);



% plot
figure (2)
%R_q_s= relaxedl2scaling(R_q);
%bodemag(tf(R_q_s))
% hold on;
% bodemag(tf(H))
% bodemag(tf(R4q))
% bodemag(tf(R5q))
% bodemag(tf(R6q))
% bodemag(tf(R7q))
% legend('H reference','cascade form','\rho DFIIt', '\delta-modal', '\rho-modal', 2 );
% AXIS([10^(-2) 10 -180 30])
% 
% norm( tf(R4q) - tf(H) )
% norm( tf(R5q) - tf(H) )
% norm( tf(R6q) - tf(H) )
% norm( tf(R7q)-tf(H))

[num,den] = ss2tf(R4q.AZ,R4q.BZ,R4q.CZ,R4q.DZ);
repf4=freqz(num,den,w0); 

[num,den] = ss2tf(R5q.AZ,R5q.BZ,R5q.CZ,R5q.DZ);
repf5=freqz(num,den,w0); 

[num,den] = ss2tf(R7q.AZ,R7q.BZ,R7q.CZ,R7q.DZ);
repf7=freqz(num,den,w0); 

plot(w0/2/pi,20*log10(abs(repf)),w0/2/pi,20*log10(abs(repf4)),w0/2/pi,20*log10(abs(repf5)),w0/2/pi,20*log10(abs(repf7)))
legend('H reference','cascade form','\rhoDFIIt','\rho-modal', 1 );
AXIS([0.35 0.5 -15 5])
grid on










