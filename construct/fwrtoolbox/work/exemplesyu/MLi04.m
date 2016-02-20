function [ML2,G] = MLi04( H, gamma)

R=rhoDFIIt2FWR(H,gamma,1);

num = H.num{1};
den = H.den{1};
Va = den'/den(1);
Vb = num'/den(1);
p1=length(Va)-1;
p2=length(Vb)-1;
p3=length(gamma);

if ( all([p2 p3]==p1) )
    p=p1;
else
    error('errors in dimensions')
end

    
%=====================================
% build Valpha_bar, Vbeta_bar
% by considering Delta_k=1 forall k

% build Tbar
Tbar=zeros(p+1,p+1);
Tbar(p+1,p+1)=1;
for i=p:-1:1
    Tbar(i,i:p+1) = poly( gamma(i:p) );
end

% Valpha_bar and Vbeta_bar
Valpha_bar = inv(Tbar)'*Va;
Vbeta_bar = inv(Tbar)'*Vb;

% equivalent state-space (Abar,Bbar,Cbar,Dbar)
A0 = diag(ones(p-1,1),1);
A0(1:end,1) = -Valpha_bar(2:end);
Arho = diag(gamma) + A0;
Brho = Vbeta_bar(2:end) - Vbeta_bar(1)*Valpha_bar(2:end);
Crho = zeros(1,p); Crho(1,1) = 1;
Drho = Vbeta_bar(1);


%====================
% l2-scaling

% compute delta (leading to a l2-scaled realization) 
Srho = ss(Arho,Brho,Crho, Drho,1);
Wc = gram(Srho,'c');

delta=zeros(1,p);
delta(1) = sqrt( Wc(1,1) );
for i=2:p
		delta(i) = sqrt( Wc(i,i) / Wc(i-1,i-1) );
end


% compute Valpha and Vbeta
Tbar=zeros(p+1,p+1);
Tbar(p+1,p+1)=1;
for i=p:-1:1
	Tbar(i,i:p+1) = poly( gamma(i:p) ) / prod( delta(i:p) );
end
Ka = prod(delta(:));
Valpha = inv(Ka*Tbar)'*Va;
Vbeta = inv(Ka*Tbar)'*Vb;


% equivalent l2-scaled state-space
d=zeros(p,1);
for i=1:p
    d(i) = inv( prod(delta(1:i)) );
end
Tsc = diag(d);
A = Tsc*Arho*inv(Tsc);
B = Tsc*Brho;
C = Crho*inv(Tsc);
D = Drho;   % can also be computed from Valpha and Vbeta
S = ss(A,B,C,D,1);
A0 = diag(ones(p-1,1),1);
A0(1:end,1) = -Valpha(2:end);


%==================
% L2-sensitivity
%eq (36)
dHdbeta = ss(A',C',eye(p),0,-1);
dHdbeta0 = ss(A,Valpha(2:end),-C,1,-1);
dHdalpha = ss(A,B,-C,-D,-1)*dHdbeta;
E=eye(p);
for k=1:p
	dHddelta(k) = ss( A,A0*E(:,k)*E(:,k)',C,E(:,1)'*E(:,k)*E(:,k)',-1) * ss(A,B,eye(p),0,-1);
end

ML2 = norm(dHdbeta)^2 + norm(dHdbeta0)^2 + norm(dHdalpha)^2 + norm(dHddelta)^2;

disp('ML2 : Formule [Li04b]')
ML2
disp('ML2 : Formule SIF')
MsensH(R)


%=====
% RNG
% eq (33)
Wrho = gram(S,'o');
tol=1e-8;
Q1=diag( abs(abs(gamma)-1)>tol & abs(gamma)>tol );
G = 3*trace(Wrho) + 2*(1+Valpha(2:end)'*Wrho*Valpha(2:end)) + trace(Q1*Wrho) - E(:,p)'*Wrho*E(:,p);

disp('RNG : Formule [Li04b]')
G
disp('RNG : Formule SIF')
RNG(R)
