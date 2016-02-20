% exemple Thèse Benoit

ordre=8;
%rng(3)% dernière version
rng(1234)%1ère version
inputU = [-237, 162]

% random system
sys = drss(ordre,1,1);


% Forme directe I
R_DFI = DFIq2FWR(tf(sys) );
gen_Benoit( R_DFI, inputU, 'BL/DFI.mat')


% Forme directe II tr
S_rhoDFIIt = rhoDFIIt2FWS( tf(sys), ones(1,ordre), ones(1,ordre) );
S_rhoDFIIt = optim( S_rhoDFIIt, {}, @MsensH);
gen_Benoit( S_rhoDFIIt.R, inputU, 'BL/rhoDFIIt.mat')


% state-space

% balanced
R1_ss = SS2FWR( balreal(sys ) )
gen_Benoit( R1_ss, inputU, 'BL/ss1.mat')

Sss = SS2FWS( ss(R1_ss) );
Sb = ss(R1_ss);
A=Sb.A; B=Sb.B; C=Sb.C; D=Sb.D;
save('BL/ABCD.mat', 'A','B','C','D');


% random
Sss.T = [ 10*rand(2,ordre); rand(ordre-2,ordre)];
gen_Benoit( Sss.R, inputU, 'BL/ss2.mat');
% optim
Sssopt1 = optim( Sss, {}, @MsensH);
gen_Benoit( Sssopt1.R, inputU, 'BL/ss3.mat');

Sssopt2 = optim( Sss, {}, @error_tf);
gen_Benoit( Sssopt2.R, inputU, 'BL/ss4.mat');

Sssopt3 = optim( Sss, {}, @error_pole);
gen_Benoit( Sssopt3.R, inputU, 'BL/ss5.mat');

Sssopt4 = optim( Sss, {}, @tradeoffMeasureError, error_tf(Sssopt2.R), error_pole(Sssopt3.R) );
gen_Benoit( Sssopt4.R, inputU, 'BL/ss6.mat');

