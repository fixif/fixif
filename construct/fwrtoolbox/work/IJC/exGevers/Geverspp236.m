% $Id: Geverspp236.m 246 2010-01-14 14:10:37Z hilaire $

% Gevers pp236
[Sysp,Reg]=geversmodel9;
Plant = ss( Sysp.A, [Sysp.B Sysp.B], [Sysp.C; Sysp.C], 0,-1);

% Direct Form II
disp( 'Direct Form II')
R1 = SS2FWR( canon(Reg,'companion') );
displ_cl( R1, Plant);

%%%%%%%%%%%%%%%%%
%% State space %%
%%%%%%%%%%%%%%%%%

load M1_opt  % optimal values

%% Balanced State-space
disp('Balanced ss')
S1 = SS2FWS( balreal(Reg) );
displ_cl( S1.Rini, Plant, M1_Hopt, M1_Popt, M1_RNGopt);

%% MsensH_cl optimal ss
disp('MsensH_cl optimal ss')
load S1_H; %S1_H = optim( S1, {'Display','Iter', 'MaxFunEvals',1e5}, @MsensH_cl, Plant)
displ_cl( S1_H.R, Plant, M1_Hopt, M1_Popt, M1_RNGopt)

%% MsensPole_cl optimal ss
disp('MsensPole_cl optimal ss')
load S1_P; %S1_P = optim( S1, {'Display','Iter', 'MaxFunEvals',1e5,'MaxIter',1e5}, @MsensPole_cl, Plant)
displ_cl( S1_P.R, Plant, M1_Hopt, M1_Popt, M1_RNGopt)

%% (non l2-scaled) RNG_cl optimal ss
disp('(non l2-scaled) RNG_cl optimal ss')
load S1_R; %S1_R = optim( S1, {'Display','Iter', 'MaxFunEvals',1e5,'MaxIter',1e5,'l2scaling','no'}, @RNG_cl, Plant)
displ_cl( S1_R.R, Plant, M1_Hopt, M1_Popt, M1_RNGopt)

%% tradeoff optimal ss
disp('"TradeOff" optimal ss')
% M1_Hopt = MsensH_cl(S1_H.R,Plant);
% M1_Popt = MsensPole_cl(S1_P.R,Plant);
% M1_RNGopt = RNG_cl(S1_R.R,Plant);
% save M1_opt M1_Hopt M1_Popt M1_RNGopt
load S1_opt; %S1_opt = optim( S1, {'Display','Iter', 'MaxFunEvals',1e5,'MaxIter',1e5}, @TradeOffMeasure_cl, Plant, M1_Hopt, M1_Popt, M1_RNGopt)

displ_cl( S1_opt.R, Plant, M1_Hopt, M1_Popt, M1_RNGopt)



%%%%%%%%%%%%%%
%% rhoDFIIt %%
%%%%%%%%%%%%%%

Delta=2^-3;
S2 = rhoDFIIt2FWS( tf(Reg), [0 0 0 0], 1, Delta*ones(1,4), 1);  % Delta and Gamma are exact (we choose them)
load M2_opt

% qDFIIt
disp('qDFIIt')
S2.Gamma = [0 0 0 0]; R2q = S2.R;
disp(['Gamma=[' num2str(S2.Gamma) ']'])
displ_cl( R2q, Plant, M2_Hopt, M2_Popt, M2_RNGopt)

% deltaDFIIt
disp('deltaDFIIt')
S2.Gamma = [1 1 1 1]; R2delta = S2.R;
disp(['Gamma=[' num2str(S2.Gamma) ']'])
displ_cl( R2delta, Plant, M2_Hopt, M2_Popt, M2_RNGopt)

%S2.Gamma=[0.5 0.5 0.5 0.5]; % initial value for optimization

%% MsensH_cl optimal rhoDFIIt
disp('MsensH_cl optimal rhoDFIIt');
load S2_H; %S2_H = optim( S2, {'Display','Iter', 'MaxFunEvals',1e5}, @MsensH_cl, Plant)
disp(['Gamma=[' num2str(S2_H.Gamma) ']'])
displ_cl(S2_H.R,Plant, M2_Hopt, M2_Popt, M2_RNGopt);

%% MsensPole_cl optimal rhoDFIIt
disp('MsensPole_cl optimal rhoDFIIt')
load S2_P; %S2_P = optim( S2, {'Display','Iter', 'MaxFunEvals',1e5,'MaxIter',1e5}, @MsensPole_cl, Plant)
disp(['Gamma=[' num2str(S2_P.Gamma) ']'])
displ_cl( S2_P.R, Plant, M2_Hopt, M2_Popt, M2_RNGopt)

%% (non l2-scaled) RNG_cl optimal rhoDFIIt
disp('(non l2-scaled) RNG_cl optimal rhoDFIIt')
load S2_R; %S2_R = optim( S2, {'Display','Iter', 'MaxFunEvals',1e5,'MaxIter',1e5,'l2scaling','no'}, @RNG_cl, Plant)
disp(['Gamma=[' num2str(S2_R.Gamma) ']'])
displ_cl( S2_R.R, Plant, M2_Hopt, M2_Popt, M2_RNGopt)

%% tradeoff optimal rhoDFIIt
disp('"TradeOff" optimal rhoDFIIt')
% M2_Hopt = MsensH_cl(S2_H.R,Plant);
% M2_Popt = MsensPole_cl(S2_P.R,Plant);
% M2_RNGopt = RNG_cl(S2_R.R,Plant);
% save M2_opt M2_Hopt M2_Popt M2_RNGopt
load S2_opt; %S2_opt = optim( S2, {'Display','Iter', 'MaxFunEvals',1e5,'MaxIter',1e5}, @TradeOffMeasure_cl, Plant, M2_Hopt, M2_Popt, M2_RNGopt)
disp(['Gamma=[' num2str(S2_opt.Gamma) ']'])
displ_cl( S2_opt.R, Plant, M2_Hopt, M2_Popt, M2_RNGopt)




