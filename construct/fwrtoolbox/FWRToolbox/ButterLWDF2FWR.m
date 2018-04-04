function R = ButterLWDF2FWR( order, Wn )
%BUTTERLWDF2FWR Summary of this function goes here
%   Detailed explanation goes here

[z,p,k] = butter( order, Wn);
[num,a2] = butter( order, Wn);
A = diag(p);
denum = poly(A); %denumerator for tf

Hzbutter.ident = 'LP PROTOTYPE: butter,5,0.1';
Hzbutter.roots_fz = z;
Hzbutter.poly_fz = num;
Hzbutter.roots_gz = p;
Hzbutter.poly_gz = denum;

Hsbutter = Hz2Hs(Hzbutter);
LWDF = Hs2LWDF(Hsbutter,0);


%LWDF2SIF
R = LWDF2SIF(LWDF, order, 'LPF');


end

