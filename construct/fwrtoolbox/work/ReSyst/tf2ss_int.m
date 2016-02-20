% passe de num/den à stat-space (nécessaire pour marcher avec des intervalles)

function [A,B,C,D] = tf2ss_int( num, den)

[numr, numc] = size(num);
[denc] = size(den,2);

% Pad num with zeros if smaller than den
if numc < denc
   num=[zeros(numr,denc-numc) num];
end

if numc > denc
   error('tf2ss_int: numerator of greater order than denominator')
end

ns = denc - 1;
if ns > 0
   num=num/den(1);
   den=den/den(1);
   A = [-den(2:ns+1); eye(ns-1) zeros(ns-1,1)];
   B = [1; zeros(ns-1,1)];
   C = num(:,2:ns+1) -  num(:,1)*den(2:ns+1);
   D = num(:,1);
else
   A = -0.5;
   B = 1;
   C = zeros(size(num,1),1);
   D = num/den;
end

end