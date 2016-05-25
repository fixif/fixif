clear all
rng(12345678)

n=7
% random system
S=drss(n);

% random 'deviations'
dA=rand(n);

%Htilde = Hq-H
Htilde = ss( [S.A zeros(n);dA S.A], [S.B;zeros(n,1)], [zeros(1,n) S.C], 0,-1);

% derivative dH/dX
dHdAt = ss( [S.A S.B*S.C; zeros(n) S.A], [zeros(n); eye(n)],[eye(n) zeros(n)],0,-1);
%ss(S.A,S.B,eye(n),0,-1)*ss(S.A,eye(n),S.C,0,-1);

dH = 0;

for i=1:n
    for j=1:n
        dH = dH + dHdAt(i,j)*dA(j,i);
    end
end
