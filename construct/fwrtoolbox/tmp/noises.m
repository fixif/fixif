% build H
Te=1e-3;

[num,den]=butter(4,0.04);
H11=tf(num,den,Te);
[num,den]=butter(4,0.14);
H12=tf(num,den,Te);
[num,den]=butter(3,0.05);
H13=tf(num,den,Te);
[num,den]=butter(3,0.15);
H21=tf(num,den,Te);
[num,den]=butter(5,0.12);
H22=tf(num,den,Te);
[num,den]=butter(5,0.08);
H23=tf(num,den,Te);
H=[H11 H12 H13; H21 H22 H23];

% build U
N=1e6;
U = [ rand(1,N) + ones(1,N)*rand(1,1); rand(1,N) + ones(1,N)*rand(1,1); rand(1,N) + ones(1,N)*rand(1,1) ]; 

muU = mean(U,2);
psiU = psi(U);
sigma2U = trace(psiU);

% build Y
Y=lsim(H,U)';

muY = mean(Y,2);
psiY = psi(Y);
sigma2Y = trace(psiY);

%
[A,B,C,D]=ssdata(H);
S=ss(A,B,C,D,Te);
Wo=dlyap(A',C'*C);
trace(psiU * (D'*D+B'*Wo*B) )
sigma2Y
phiU=chol(psiU);
norm(H*phiU,2)^2