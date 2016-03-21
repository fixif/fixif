function R = tfLWDF2FWR( num, den )
%BUTTERLWDF2FWR Summary of this function goes here
%   Detailed explanation goes here


H = tf(num,den,-1);
ZPK = zpk(H);
z = ZPK.z{1};
p = ZPK.p{1};

Hz.ident = 'LP PROTOTYPE';
Hz.roots_fz = z;
Hz.poly_fz = num;
Hz.roots_gz = p;
Hz.poly_gz = den;

Hs = Hz2Hs(Hz);
LWDF = Hs2LWDF(Hs);


%LWDF2SIF
R = LWDF2SIF(LWDF, length(den), 'LPF');

end

