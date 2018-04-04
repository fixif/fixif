%test script


% filterorder = 5;
% % Wn = 0.4;
% % Hs = Hs_butter(filterorder, Wn);
% Hs = nlpf('cauer',filterorder,0.2,60,'a');
% LWDF = Hs2LWDF(Hs);
% %getting Transfer function of LWDF
% Hz_LWDF = LWDF2Hz(LWDF);
% [num1, num2] = Hz_LWDF.poly_fz;
% [denum1, denum2] = Hz_LWDF.poly_gz;
% % num = {num1; -num2};
% % denum = {denum1; denum2};
% tfLWDF = tf(num1, denum1, -1);
%

clc
clear

filterorder = 5;
Wn = 0.1;

[z,p,k] = butter(filterorder,Wn);
[num,a2] = butter(5,0.1);
A = diag(p);
denum = poly(A); %denumerator for tf
butter_tf = tf(num,denum, -1);

Hzbutter.ident = 'LP PROTOTYPE: butter,5,0.1';
Hzbutter.roots_fz = z;
Hzbutter.poly_fz = num;
Hzbutter.roots_gz = p;
Hzbutter.poly_gz = denum;

Hsbutter = Hz2Hs(Hzbutter);
LWDF = Hs2LWDF(Hsbutter);
Hz_LWDF = LWDF2Hz(LWDF);

[num1, num2] = Hz_LWDF.poly_fz;
[denum1, denum2] = Hz_LWDF.poly_gz;
tfLWDF = tf(num1, denum1, -1);


spectral_radius = max(abs(roots(tfLWDF.den{1})))

%LWDF2SIF
SIF_LWDF = LWDF2SIF(LWDF, filterorder, 'LPF');
tfSIF_LWDF = tf(SIF_LWDF);

[ncoef_LWDF, errortf_LWDF, errorpole_LWDF,...
    MsensH_LWDF, MsensPole_LWDF, RNG_LWDF, NOE_LWDF] = results(SIF_LWDF);


%DFIq
SIF_DFI = DFIq2FWR(tfLWDF);
tfSIF_DFI = tf(SIF_DFI);
tt = error_pole(SIF_DFI);
[ncoef_DFI, errortf_DFI, errorpole_DFI,...
    MsensH_DFI, MsensPole_DFI, RNG_DFI, NOE_DFI]= results(SIF_DFI);


%State space
SIF_SS_noopt = SS2FWS(balreal(ss(tfLWDF)));

SS_Sopt_tf = optim(SIF_SS_noopt, {'method','newton','Display','Iter'}, @error_tf);
%SS_Sopt_NOE = optim(SIF_SS_noopt, {'method','newton','Display','Iter'}, @NOE);
%SS_Sopt_troff = optim(SIF_SS_noopt, {'method','newton','Display','Iter'},...
   % @tradeoff_tf_NOE,  error_tf(SS_Sopt_tf.R), NOE(SS_Sopt_NOE.R));

SIF_SS = SS_Sopt_tf.R;
[ncoef_SS, errortf_SS, errorpole_SS,...
    MsensH_SS, MsensPole_SS, RNG_SS, NOE_SS] = results(SIF_SS);

%rhoDIFII
SIF_rho_noopt = rhoDFIIt2FWS( tfLWDF, ones(1, filterorder), 1, -ones(1, filterorder), 1 );
Sopt_tf = optim(SIF_rho_noopt, {'method','newton','Display','Iter'}, @error_tf);
Sopt_pole = optim(SIF_rho_noopt, {'method','newton','Display','Iter'}, @error_pole);
Sopt_troff = optim(SIF_rho_noopt, {'method','newton','Display','Iter'},...
   @tradeoffMeasureError,  error_tf(Sopt_tf.R), error_pole(Sopt_pole.R));
%Sopt_NOE = optim(SIF_rho_noopt, {'method','newton','Display','Iter'}, @NOE);
%Sopt_troff = optim(SIF_rho_noopt, {'method','newton','Display','Iter'},...
 %   @tradeoff_tf_NOE,  error_tf(Sopt_tf.R), NOE(Sopt_NOE.R));

SIF_rho = Sopt_troff.R;
[ncoef_rho, errortf_rho, errorpole_rho,...
    MsensH_rho, MsensPole_rho, RNG_rho, NOE_rho] = results(SIF_rho);

save('resultsLWDF', 'SIF_LWDF', 'ncoef_LWDF', 'errortf_LWDF',...
     'errorpole_LWDF','MsensH_LWDF', 'MsensPole_LWDF',...
     'RNG_LWDF','NOE_LWDF');
save('resultsDFI', 'SIF_DFI', 'ncoef_DFI', 'errortf_DFI',...
     'errorpole_DFI','MsensH_DFI', 'MsensPole_DFI',...
     'RNG_DFI','NOE_DFI');
save('resultsSS', 'SIF_SS', 'ncoef_SS', 'errortf_SS',...
     'errorpole_SS','MsensH_SS', 'MsensPole_SS',...
     'RNG_SS','NOE_SS');
save('resultsrhoDFIIt', 'SIF_rho', 'ncoef_rho', 'errortf_rho',...
     'errorpole_rho','MsensH_rho', 'MsensPole_rho',...
     'RNG_rho','NOE_rho');
 

% save( 'LWDF_table.mat', 'SIF_LWDF', 'ncoef_LWDF', 'errortf_LWDF',...
%     'errorpole_LWDF','MsensH_LWDF', 'MsensPole_LWDF',...
%     'RNG_LWDF',...
%     'SIF_DFI', 'ncoef_DFI', 'errortf_DFI',...
%     'errorpole_DFI','MsensH_DFI', 'MsensPole_DFI',...
%     'RNG_DFI',...
%     'SIF_SS', 'ncoef_SS', 'errortf_SS',...
%     'errorpole_SS','MsensH_SS', 'MsensPole_SS',...
%     'RNG_SS',...
%     'SIF_rho', 'ncoef_rho', 'errortf_rho',...
%     'errorpole_rho','MsensH_rho', 'MsensPole_rho',...
%     'RNG_rho');
