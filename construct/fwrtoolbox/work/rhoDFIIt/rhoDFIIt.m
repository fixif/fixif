function [Valpha,Vbeta,K,M] = rhoDFIIt( Vb, Va, gamma, Delta)

% normalisation
Vb = Vb'/Va(1);
Va = Va'/Va(1);

n = length(Delta);
K = prod(Delta);

M = zeros(n+1);
for i=1:n
    M(i:n+1,i) = poly( gamma(i:n) )' / prod(Delta(i:n));
end
M(n+1,n+1)=1;

Valpha = inv(K)*inv(M)*Va;
Vbeta = inv(K)*inv(M)*Vb;