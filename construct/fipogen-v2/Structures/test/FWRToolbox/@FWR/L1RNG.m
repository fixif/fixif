function m = L1RNG(R)

% H1
H1 = ss(R.AZ, R.BZ, [ inv(R.J)*R.M ; eye(R.n); R.CZ ], [inv(R.J)*R.N; zeros(R.n,R.m); R.DZ],-1);
[Yimp Timp] = impulse(H1);
b1 = squeeze(sum(abs(Yimp)))';

% H2
H2 = ss(R.AZ, [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.m) ], R.CZ, [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ],-1);
[Yimp Timp] = impulse(H2);
b2 = squeeze(sum(abs(Yimp)))';

m = b2*b1;