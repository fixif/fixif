function JASP

H=tf(100,[1 -0.8],-1)

S=ss(H);


display('balanced')
Sb=balreal(S);
dispfp(Sb)

display('scaling')
T=0.15;
Ssc=ss(S.a,S.b/T,S.c*T,0,-1);
dispfp(Ssc)


display('L2-scaled')
T=sqrt(gram(S,'c'));
Ss=ss(S.a,S.b/T,S.c*T,0,-1);
dispfp(Ss)



%display fixed-point 8bits
function dispfp(S)
X = [S.A S.B ; S.C S.D];
betaX = 8*ones(size(X));
gammaX = betaX - 2 - floor(log2(abs(X)));
N = floor(X .* (2*ones(size(X))).^gammaX);

N
-gammaX
