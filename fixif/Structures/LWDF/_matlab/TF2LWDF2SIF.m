function [R] = TF2LWDF2SIF( b, a )
% This function computes the SIF representation for
% a LWDF structure that describes a filter given with
% numerator b and denumerator a.


Hzfilter.ident = 'LWDF';
Hzfilter.poly_fz = b;
Hzfilter.poly_gz = a;

Hsfilter = Hz2Hs(Hzfilter);
LWDF = Hs2LWDF(Hsfilter,0);


Hz_LWDF = LWDF2Hz(LWDF);
[num1, num2] = Hz_LWDF.poly_fz;
[denum1, denum2] = Hz_LWDF.poly_gz;

order = max(length(b) - 1, length(a) - 1);
R = LWDF2SIF(LWDF, order, 'LPF');
[R, ~ ] = simplify2(R);

R = struct(R);
end
