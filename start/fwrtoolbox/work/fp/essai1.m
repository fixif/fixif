% filtre, réalisation
[num, den] = butter(4,0.05);
H=tf(num,den,1);
R = rhoDFIIt2FWR( H, [0.4 0.5 0.6 0.7], 1, 2^-4*ones(1,4), 1);


% données d'entrée / sortie
betaU = 16; betaY = 16;
alphaU = 5;
u=28*(2*(rand(50000,1)-0.5*ones(50000,1)));
Ufp = quantif(u,betaU,alphaU);


% choix réalisation
betaT = 16*ones(4,1); betaX = 16*ones(4,1);
betaADD = 16;
betaZ = 16*ones(size(R.Z));

%
H6 = ss(R.AZ,R.BZ, [ inv(R.J)*R.M ; eye(R.n); R.CZ ], [inv(R.J)*R.N; zeros(R.n,R.m); R.DZ],1);
[Yimp Timp] = impulse(H6);
L1 = sum(abs(Yimp))';

alphaTXY = ceil(log2(L1)) + ones(R.l+R.n+R.p,R.m)*alphaU;
alphaTXU = [ alphaTXY(1:8,1); alphaU ];

alphaZ = ceil(log2(abs(R.Z)));

alphaADD = max( alphaTXY, max( (ones(R.l+R.n+R.m,1)*alphaTXU' + alphaZ + 1)' )' );

alphaZp = alphaADD*ones(1,R.l+R.n+R.p) - ones(R.l+R.n+R.m,1)*alphaTXU' - 1 ;