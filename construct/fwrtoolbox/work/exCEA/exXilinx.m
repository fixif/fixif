
% filtre
load NumDen
Te=1/50e3;
H=tf(Num,Den,Te)

%
Umax = 10;
beta = 16;

% forme directe I
R1 = DFIq2FWR(H);
cd 'src'; implementCdouble( R1, 'filtre1double'); cd '..'

% forme rhoDFIIt
S = rhoDFIIt
