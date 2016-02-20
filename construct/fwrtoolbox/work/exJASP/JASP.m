function JASP

H=tf(100,[1 -0.8],-1)

S=ss(H);


display('balanced')
Sb=balreal(S);
dispfp(Sb)

display('scaling')
T=0.015;
Ssc=ss(S.a,S.b/T,S.c*T,0,-1);
dispfp(Ssc)


display('L2-scaled')
T=sqrt(gram(S,'c'));
Ss=ss(S.a,S.b/T,S.c*T,0,-1);
dispfp(Ss)



R1 = SS2FWR(Sb);
R2 = SS2FWR(Ssc);
R3 = SS2FWR(Ss);
Nbbits = 8;

    R1q = setFPIS(R1, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R1q = quantized(R1q);
    R2q = setFPIS(R2, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R2q = quantized(R2q);
    R3q = setFPIS(R3, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R3q = quantized(R3q);

    dispResult( R1, R1q, 'balanced' );
    dispResult( R2, R2q, 'scaling' );
    dispResult( R3, R3q, 'L2-scaled' );   
end



    
function dispResult( R, Rq, name)
    disp( [ name ':']);
    disp([ '     Msens=' num2str(MsensH(R)) ' |h-h''| = ' num2str(norm(tf(Rq)-tf(R))) ]);
end    
    
    


%display fixed-point 8bits
function dispfp(S)
X = [S.A S.B ; S.C S.D];
betaX = 8*ones(size(X));
gammaX = betaX - 2 - floor(log2(abs(X)));
N = floor(X .* (2*ones(size(X))).^gammaX);

R = SS2FWR(S);
R.WZ(2,2)=1;
[M, MZ] = MsensH(R);

gammaX( find(gammaX == Inf) ) = 0;
MZ.*(2.^-gammaX);
M;

N
-gammaX
end