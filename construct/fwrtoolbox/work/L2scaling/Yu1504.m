H=tf(62.83185307,[1 62.83185307]);
Hd=c2d(H,1e-3,'Tustin');

% initial realization 
S=ss(Hd);
S.b=S.b*4; S.c=S.c/4;
R1=relaxedl2scaling(SS2FWR(S));

% balanced realization
R2=relaxedl2scaling(SS2FWR(balreal(S)));

% optimal SS realization
S1=SS2FWS(S);
S1opt = optim( S1, {'l2scaling','relaxed','Display','Iter'},@MsensH);

% delta realization
Delta = 2^-3;
R3 = relaxedl2scaling( SSdelta2FWR( balreal(S), Delta, 1) );
S2 = SSdelta2FWS( balreal(S), Delta, 1);

S2opt = optim( S2, {'l2scaling','relaxed','Display','Iter'},@MsensH);

% rho realization
R4 = relaxedl2scaling( rhoDFIIt2FWR( Hd, 0.5, 1, 2^-3, 1) );
S3 = rhoDFIIt2FWS( Hd, 0.5, 1, 2^-3, 1);
S3opt = optim( S3, {'l2scaling','relaxed','Display','Iter'},@MsensH);
