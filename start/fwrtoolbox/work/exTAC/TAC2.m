% Exemple Njabkele
% Msens_cl
%
% $Id$

load 'exNjab'
Te=Reg.Ts;

% transformation in standard form
Sysp = ss( Sysp.A, [Sysp.B Sysp.B], [Sysp.C; Sysp.C], 0);

% parameters
Delta=2^-5;
Delta=5e-4;
S1 = strvcat(   '\begin{tiny}\begin{equation*}', 'Z_=');
S2 = strvcat(   '\end{equation*}', '\begin{equation*}', '\en{\dede{\tilde{H}}{Z}}_{Z_} =');
S3 = strvcat(   '\end{equation*}\end{tiny}');


%==================
% Forme directe II
disp('Forme directe II')
[num,den] = ss2tf(Reg.A,Reg.B,Reg.C,Reg.D);
[A,B,C,D] = tf2ss(num,den);
R2 = SS2FWR(A,B,C,D);
MsensH_cl(R2,Sysp)
MsensPole_cl(R2,Sysp)

%R2.WZ = ones(size(R2.WZ));
%[M2 MZ2] = MsensH_cl(R2,Sysp);
%strvcat( S1, matMW2latex(R2.Z,R2.WZ,'%.3e'), S2, matMW2latex(MZ2,R2.WZ,'%.3e'), S3);


%==================
% Forme �quilibr�e
try
disp('Forme �quilibr�e')
R3 = SS2FWR( balreal(Reg) );
MsensH_cl(R3,Sysp)
MsensPole_cl(R3,Sysp)
catch
end

%R3.WZ = ones(size(R3.WZ));
%[M3 MZ3] = MsensH_cl(R3,Sysp);
%strvcat( S1, matMW2latex(R3.Z,R3.WZ,'%.3e'), S2, matMW2latex(MZ3,R3.WZ,'%.3e'), S3);



%==========================
% Forme directe II en delta
disp('Forme directe II en delta')
[numd,dend] = z2del(num,den,Delta);
[Ad,Bd,Cd,Dd] = tf2ss(numd,dend);
R4 = SSdelta2FWR(Ad,Bd,Cd,Dd,Delta,1);

MsensH_cl(R4,Sysp)
MsensPole_cl(R4,Sysp)

%R4.WZ = ones(size(R4.WZ));
%[M4 MZ4] = MsensH_cl(R4,Sysp);
%strvcat( S1, matMW2latex(R4.Z,R4.WZ,'%.3e'), S2, matMW2latex(MZ4,R4.WZ,'%.3e'), S3);




% Forme delta optimale
disp('Forme delta optimale')
S5 = SSdelta2FWS(Ad,Bd,Cd,Dd, Delta,1);
S5.Rini.WM = ones(size(S5.Rini.WM));
load S5opt %S5opt = optim( S5, {'Display','Iter', 'MaxFunEvals',1e4}, @MsensH_cl, Sysp)

MsensH_cl(S5opt.R,Sysp)
MsensPole_cl(S5opt.R,Sysp)

%R5.WZ = ones(size(R5.WZ));
%[M5 MZ5] = MsensH_cl(R5,Sysp);
%strvcat( S1, matMW2latex(R5.Z,R5.WZ,'%.3e'), S2, matMW2latex(MZ5,R5.WZ,'%.3e'), S3);
