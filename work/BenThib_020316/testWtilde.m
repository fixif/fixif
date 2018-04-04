rng(1);
n=10;
delta=1e-4;

S=drss(n);

deltaA=rand(size(S.A))*delta; Atilde = S.A+deltaA;
deltaB=rand(size(S.B))*delta; Btilde = S.B+deltaB;
deltaC=rand(size(S.C))*delta; Ctilde = S.C+deltaC;
deltaD=rand(size(S.D))*delta; Dtilde = S.D+deltaD;

Htilde = ss( [S.A zeros(n,n); Atilde-S.A Atilde], [S.B;Btilde-S.B], [Ctilde-S.C Ctilde], Dtilde-S.D,-1);


dHdZ = ss( [S.A S.B*S.C; zeros(n,n) S.A], [zeros(n,n) S.B; eye(n) zeros(n,1)], [eye(n) zeros(n,n); zeros(1,n) S.C], [zeros(n,n) zeros(n,1); zeros(1,n) 1], -1);

deltaZ=[deltaA deltaB; deltaC deltaD];


t=dHdZ*deltaZ';
tr=0;
for i=1:11
    tr=tr+t(i,i);
end
