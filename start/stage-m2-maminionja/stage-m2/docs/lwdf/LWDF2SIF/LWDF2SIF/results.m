function [ncoefR, errortfR, errorpoleR, MsensHR, MsensPoleR, RNGR, NOER] = results(R)

[ncoefR, ~] = size(find(sparse(R.WZ)));
errortfR = error_tf(R);
errorpoleR = error_pole(R);
MsensHR = MsensH(R);
MsensPoleR = MsensPole(R);
RNGR = RNG(R);
NOER = NOE(R);