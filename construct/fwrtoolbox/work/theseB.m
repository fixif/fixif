% exemple Thèse Benoit

ordre=3;
rng(123456)

% random system
sys = drss(ordre,1,1);

% state-space
T = [ 1000*rand(2,ordre); rand(ordre-2,ordre)];
R_ss = SS2FWR( inv(T)*sys.A*T, inv(T)*sys.B, sys.C*T, sys.D)
gen_Benoit( R_ss, [-25,30], 'exT_ss.mat')


% Forme directe I
R_DFI = DFIq2FWR(tf(sys) )
gen_Benoit( R_DFI, [-25,30], 'exT_DFI.mat')

% Forme directe II tr
S_rhoDFIIt = rhoDFIIt2FWS( tf(sys), ones(1,ordre), ones(1,ordre) )
S_rhoDFIIt = optim( S_rhoDFIIt, {}, @MsensH)
gen_Benoit( S_rhoDFIIt.R, [-25,30], 'exT_rhoDFIIt.mat')
