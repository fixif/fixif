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



% forme directe II
R=FWR( 1, [1;0], b0p, [-a1p -a2p], 1, [0 0;1 0], [0;0], [b1p b2p],0)