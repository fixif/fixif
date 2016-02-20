
% paramètres signifiants
fc = 10;
fe = 200;
xi = 1/2;
% paramètres déduits
wc = 2*pi*fc;
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
H = tf([b0p b1p b2p],[1 a1p a2p], T);

%================
% forme directe I
R1 = DFIq2FWR(H);

% forme directe II
R2 = SS2FWR(ss(H));

% formes d'états
S1 = SS2FWS( balreal(ss(H)) );
R3 = S1.Rini;
S1 = optim( S1, {'method','ASA','l2scaling','relaxed2'},@error_tf);
R4 = S1.R

% forme delta-ss
S2 = SSdelta2FWS( balreal(ss(H)), 1/32, 1 );
S2 = optim( S2, {'method','ASA','l2scaling','relaxed2'},@error_tf);
R5 = S2.R;

% forme rhoDFIIt
S3 = rhoDFIIt2FWSrelaxedL2( H, [1 1], 1, 1/32*[1 1], 1);
S3 = optim( S3, {'method','ASA','l2scaling','relaxed2'},@error_tf);
R6 = S3.R;




%===============
% resultats
 
y1 = resultat(R1,'R1');
y2 = resultat(R2,'R2');
y3 = resultat(R3,'R3');
y4 = resultat(R4,'R4');
y5 = resultat(R5,'R5');
y6 = resultat(R6,'R6');

y0 = step(H,99*T);
