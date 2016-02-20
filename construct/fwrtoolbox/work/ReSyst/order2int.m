intvalinit('DisplayInfsup')
close all

L3=zeros(32,1);
L2=zeros(32,1);
L2br=zeros(32,1);
for nbbits=4:32
 
 
% paramètres signifiants
fc = 10;%infsup(9.9995,10.0005);%10;
fe = 200;
xi = infsup(0.4,0.6);%+infsup(-2^-nbbits,2^-nbbits); %0.5
% paramètres déduits
pii = pi;%quantized_int(pi,nbbits);
wc = 2*pii*fc;
g = wc^2;
T = 1/fe;

% coefficients
b0 = g*T^2;
b1 = 2*b0;
b2 = b0;
a0 = 4*xi*wc*T + wc^2*T^2 + 4;
a1 = 2*wc^2*T^2 - 8;
a2 = wc^2*T^2 - 4*xi*wc*T + 4;

b0p = b0/a0;
b1p = b1/a0;
b2p = b2/a0;
a0p = 1;
a1p = a1/a0;
a2p = a2/a0;

% fonction de transfert
%H = tf([b0p b1p b2p],[1 a1p a2p], T);
num=[b0p b1p b2p];
den=[1 a1p a2p]; 
H=tf(mid(num),mid(den),-1);


%================
% forme directe I
R1 = DFIq2FWR(num,den);

[Aint,Bint,Cint,Dint] = tf2ss_int(num,den);

% forme canonique
R2 = SS2FWR(Aint,Bint,Cint,Dint);
S2 = SS2FWS(mid(Aint),mid(Bint),mid(Cint),mid(Dint));
S2int=SS2FWS( Aint,Bint,Cint,Dint );

dR2 = R2 + (-S2.R);
L2(nbbits) = norm2_int(dR2);


% balreal
[Sbr,G,T,Ti] = balreal( ss(S2.R) );
S2.T = T;
S2int.T = T;
dR2br = S2.R + (-S2int.R);
L2br(nbbits) = norm2_int(dR2br);


% formes d'états
%S1 = SS2FWS( balreal(ss(H)) );
%R3 = S1.Rini;
%S1 = optim( S1, {'method','ASA','l2scaling','relaxed2'},@error_tf);
%R4 = S1.R
%
%% forme delta-ss
%S2 = SSdelta2FWS( balreal(ss(H)), 1/32, 1 );
%S2 = optim( S2, {'method','ASA','l2scaling','relaxed2'},@error_tf);
%R5 = S2.R;
%

% forme rhoDFIIt
%S3 = rhoDFIIt2FWSrelaxedL2( H, [1 1], 1, 1/32*[1 1], 1);
%S3 = optim( S3, {'method','ASA','l2scaling','relaxed2'},@error_tf);
%R6 = S3.R;
%
%
%
%
%%===============
%% resultats
% 
%y1 = resultat(R1,'R1');
%y2 = resultat(R2,'R2');
%y3 = resultat(R3,'R3');
%y4 = resultat(R4,'R4');
%y5 = resultat(R5,'R5');
%y6 = resultat(R6,'R6');
%
%y0 = step(H,99*T);


R3 = rhoDFIIt2FWR( H , [1 1], 1, 1/32*[1 1], 1);
R3int = rhoDFIIt2ndFWR( num,den , [1 1], 1, 1/32*[1 1], 1);
dR3 = R3+(-R3int);

L3(nbbits) = norm2_int(dR3);

end

L2( find(isnan(L2)) )  = -1;
L3( find(isnan(L3)) )  = -1;
L2br( find(isnan(L2br)) )  = -1;


 semilogy(L2,'r*');hold on; semilogy(L3,'b*'); semilogy(L2br,'g*');
 legend('forme canonique', 'deltaDFIIt','balanced')
xlabel('nb bits')
ylabel('H2 norme de la différence h-h_intervalle')