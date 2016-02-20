function [btf, Hs, LWDF] = findFilter()

Wp = 40/500;
Ws = 150/500;

[n,Wn] = buttord(Wp,Ws,3,60);
[z,p,k] = butter(n,Wn);
sys = zpk(z,p,k);
btf = tf(sys);

Hz.poly_fz = num;
Hz.poly_gz = denum;
Hz.ident = 'butterworth filter';
Hz.roots_fz = roots(num);
Hz.roots_gz = roots(denum);

Hs = Hz2Hs(Hz);
LWDF = Hs2LWDF(Hs);
LHZ = LWDF2Hz(LWDF);

rhoButter = max(abs(roots(num)))
rhoHz = max(abs(roots(Hz.poly_fz)))
rhoLHZ = max(abs(LHZ.roots_fz))




end