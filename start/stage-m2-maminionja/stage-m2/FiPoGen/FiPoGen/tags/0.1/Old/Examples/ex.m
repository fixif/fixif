[num,den]=butter(4,0.166);

%Forme directe I
R1=DFIq2FWR(num,den);
R1q = setFPIS(R1,'DSP16',10);
algorithmLaTeX(R1q);

% forme d'état balancée
S=balreal(ss(tf(num,den,-1)));
R2 = SS2FWR(S);
R2q = setFPIS(R2,'DSP16',10);

% rho DFIIt
R3 = rhoDFIIt2FWR(num,den, [0.893649530913534   0.057891304784269   0.352868132217001   0.813166497303758],1,[1 1 1 1]/32,0) ;
R3q = setFPIS(R3,'DSP16',10);