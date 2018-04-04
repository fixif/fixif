% Exemple DASIP

N=3

[num,den] = butter(N,0.166);
h = tf(num,den,-1)
h_xi=tf(1,den,-1);

mXi = 12;
pXi = 25;

%papier
p = norm(h_xi,2)^2 * pXi + (dcgain(h_xi)*mXi)^2;


% FWR Toolbox
R = DFIq2FWR(num,den);
mXiVec = [mXi;zeros(2*N+1,1)];
pXiVec = zeros(2*N+2); pXiVec(1,1)=pXi;
ONP(R,0,mXiVec,pXiVec);

% classic bad imple
num16 = 2^(-13) * round(num*2^13);
den16 = 2^(-13) * round(den*2^13);
Nnum16 = round(num*2^13)
Nden16 = round(den*2^13)

h_d = tf(num16,den16,-1);

norm(h-h_d)

%
for bits=[8 16]
    bits
    alphaNum = floor( log2(abs(num)) ) +2;
    gammaNum = bits*ones(1,N+1) - alphaNum;
    alphaDen = floor( log2(abs(den)) ) +2;
    gammaDen = bits*ones(1,N+1) - alphaDen;
    
   
    numD = 2.^(-gammaNum) .* round( num.*2.^gammaNum)
    denD = 2.^(-gammaDen) .* round( den.*2.^gammaDen)

    h_d = tf(numD,denD,-1);
    norm(h-h_d)
end
