% filtre, réalisation
[num, den] = butter(4,0.05);
H=tf(num,den,1);
R = rhoDFIIt2FWR( H, [0.4 0.5 0.6 0.7], 1, 0.06*ones(1,4), 1);

% données d'entrée
betaZ = 16;
betaU = 16; gammaU = 10;    % |U| < 32
betaY = 16;
betaX = 16;
betaT = 16;
betaADD = 32;
betaG = 4;



% change args if they are scalar
if prod( size(betaZ) )==1
    betaZ = betaZ * ones(size(R.Z));
end
if prod( size(betaU) )==1
    betaU = betaU * ones(R.m,1);
end
if prod( size(gammaU) )==1
    gammaU = gammaU * ones(R.m,1);
end
if prod( size(betaY) )==1
    betaY = betaY * ones(R.p,1);
end
if prod( size(betaX) )==1
    betaX = betaX * ones(R.n,1);
end
if prod( size(betaT) )==1
    betaT = betaT * ones(R.l,1);
end
if prod( size(betaADD) )==1
    betaADD = betaADD * ones( size(R.Z,1), 1);
end
if prod( size(betaG) )==1
    betaG = betaG * ones( size(R.Z,1), 1);
end


% gammas
H6 = ss(R.AZ,R.BZ, [ inv(R.J)*R.M ; eye(R.n); R.CZ ], [inv(R.J)*R.N; zeros(R.n,R.m); R.DZ],1);
[Yimp Timp] = impulse(H6);
L1 = sum(abs(Yimp))';
betaTXY = [ betaT; betaX; betaY ];
betaTXU = [ betaT; betaX; betaU ];
gammaTXY = betaTXY - ones(size(R.Z,1),1) - ceil( log2( L1*(2*ones(R.m,1)).^(betaU-gammaU-1) ) );
gammaTXU = [ gammaTXY(1:(R.l+R.n)); gammaU ];
gammaZ = betaZ - ones(size(R.Z)) - ceil( log2(abs(R.Z)) );
alpha = max( betaZ - gammaZ + ones(size(R.Z,1),1)*((betaTXU-gammaTXU)'),[],2 );
gammaADD = betaADD - max( betaTXY-betaG-gammaTXY, alpha);

% taking care of null or 1 parameters
eps=1e-12;
i0 = find( abs(r.Z)<eps);
i1 = find( abs(r.Z-1)<eps);
%betaZ(i1)=0;
%gammaZ(i1)=0;
%betaZ(i0)=
%gammaZ(i0)=

