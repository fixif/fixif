function gen_Benoit(R, u, filename)

% u
ur = ones(R.p,1) * (u(2)-u(1))/2;
um = ones(R.p,1) * (u(2)+u(1))/2;

% fonction de transfert Hu et He
Hu = ss( R.AZ, R.BZ, [inv(R.J)*R.M;R.AZ;R.CZ], [inv(R.J)*R.N; R.BZ; R.DZ], -1 );
He = ss(R.AZ, [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.m) ], R.CZ, [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ],-1);


Rfpis = setFPIS(R, 'DSP16',10);
Rqt = quantized(Rfpis);

% késako ?
HHe = ss( [R.AZ zeros(R.n); (R.AZ-Rqt.AZ) Rqt.AZ],[R.BZ zeros(R.n,R.n+1); (R.BZ-Rqt.BZ) -eye(R.n) zeros(R.n,1)], [(R.CZ-Rqt.CZ) Rqt.CZ], [(R.DZ-Rqt.DZ) zeros(1,R.n) -1], -1);



%display('DC-Gain et WCPG Hu (u-> t,x,y)')
[dcHu wcpgHu] = dc_norminf(Hu);

%display('Intervalles t,x,y')
tm = dcHu*um;
tr = (wcpgHu*ur)';
inter_t = [ tm-tr tm+tr ];

%display('DC-Gain et WCPG He (erreur t,x,y - >y)')
[dcHe wcpgHe] = dc_norminf(He);

l=R.l;
m=R.m;
p=R.p;
n=R.n;
Z=R.Z;
save( filename, 'l', 'm', 'n', 'p', 'Z', 'ur', 'um', 'dcHu', 'wcpgHu', 'dcHe', 'wcpgHe');

