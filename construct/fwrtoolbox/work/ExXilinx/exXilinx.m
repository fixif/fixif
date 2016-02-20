% modèle
load NumDen

Te=1/50e3;
H=tf(Num,Den,Te)
display('poles')
abs(roots(H.den{1}))

%paramètres
Umax=1;

% Forme directe I
R1 = DFIq2FWR(H);
poles=zeros(5,64);
for nb=16:64
    R1 = setFPIS(R1,nb,Umax,nb,nb,nb,nb,2*nb,0,'RAM');
    R1q = quantized(R1);
    nb
    Hq=tf(R1q);
	toto = abs(roots(Hq.den{1}))
    poles(:,nb) = toto(6:10);
end

% Forme delta
Delta=2^-5;
R2 = rhoDFIIt2FWR( H, ones(1,5),1,Delta*ones(1,5),1);
nb=8;
R2 = setFPIS(R2,nb,Umax,nb,nb,nb,nb,2*nb,0,'RAM');
R2q = quantized(R2);
Hq=tf(R2q);
abs(roots(Hq.den{1}))