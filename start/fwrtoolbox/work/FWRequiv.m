function Req = FWRequiv(R)

J = [ R.J zeros(R.l,R.n) ; -R.K eye(R.n) ];
K = [ zeros(R.n,R.l) eye(R.n) ];
L = [ R.L zeros(R.p,R.n) ];
M = [ R.M ; R.P ];
N = [ R.N ; R.Q ];
P = zeros(R.n);
Q = zeros(R.n,R.m);
RR = R.R;
S = R.S;

Req = FWR(J,K,L,M,N,P,Q,RR,S);