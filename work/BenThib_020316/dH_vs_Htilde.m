clear all
rng(12345678)

n=7
% random system
S=drss(n);

% random 'deviations'
dA=zeros(n);%rand(n);
dB=rand(n,1);
dC=rand(1,n);
dD=rand(1,1);
dX=[dA dB;dC dD];

%Htilde = Hq-H
Htilde = ss([S.A zeros(n);dA S.A+dA], [S.B;dB], [dC S.C+dC],dD,-1);

% derivative dH/dX
dHdX=ss([S.A S.B*S.C;zeros(n) S.A],[zeros(n) S.B;eye(n) zeros(n,1)],[eye(n) zeros(n);zeros(1,n) S.C], [zeros(n) zeros(n,1);zeros(1,n) 1],-1);

% is Htilde =? \sum_{ij} dH/dX_{ij} * dX_{ij} (1st order approx; should be true for B,C and D)
dH=ss(0,0,0,0,-1);
for i=1:n+1
    for j=1:n+1
        dH = dH + dHdX(i,j) * dX(j,i);
    end
end
