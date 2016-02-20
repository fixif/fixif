% TAC example
%

load 'exNjab'
Sysp = ss( Sysp.A, [Sysp.B Sysp.B], [Sysp.C; Sysp.C], 0);
Delta=2^-5;

% SS structuration
S1 = SS2FWS( balreal(Reg));
S1opt = optim( S1, {'Method','ASA'}, @MsensH_cl, Sysp);
