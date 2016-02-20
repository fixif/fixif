rng(53756)

% random ss
S=drss(4,1);
H=tf(S)

% conversion rhoDFIIt
FS=rhoDFIIt2FWS( H, [1 1 1 1 ],[1 1 1 1],[1 1 1 1],[1 1 1 1]);

% rhoDFIIt optimal
Sopt = optim(FS, {'display','iter'},@L1RNG);
Sopt.gamma;
Ropt=Sopt.R;

% algo
implementCdouble(Ropt);

% magnitude
Hmax = ss(Ropt.AZ, Ropt.BZ, [ inv(Ropt.J)*Ropt.M ; eye(Ropt.n); Ropt.CZ ], [inv(Ropt.J)*Ropt.N; zeros(Ropt.n,Ropt.m); Ropt.DZ],-1);
[dcmax norminfmax] = dc_norminf(Hmax)

% DFIq
Rd=DFIq2FWR(H.num{1},H.den{1});

H2 = ss(Ropt.AZ, [ Ropt.K*inv(Ropt.J) eye(Ropt.n) zeros(Ropt.n,Ropt.m) ], Ropt.CZ, [ Ropt.L*inv(Ropt.J) zeros(Ropt.p,Ropt.n) eye(Ropt.p) ],-1);
H2d = ss(Rd.AZ, [ Rd.K*inv(Rd.J) eye(Rd.n) zeros(Rd.n,Rd.m) ], Rd.CZ, [ Rd.L*inv(Rd.J) zeros(Rd.p,Rd.n) eye(Rd.p) ],-1);

[dc norminf] = dc_norminf(H2);
[dc2 norminf2] = dc_norminf(H2d);

e0=ones(9,1);
e1=1e-2*ones(9,1);

disp('ex erreur sop');
[e0-e1 e0+e1];

disp('erreur rhoDFIIt');
[e0*dc-e1*norminf e0*dc+e1*norminf];

disp('erreur DFIt');
[e0*dc2-e1*norminf2 e0*dc2+e1*norminf2];


