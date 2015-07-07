%Purpose:
% Transform a $\rho$-state-space realization into a FWS object
%
%Syntax:
% S = SSrho2FWS( Arho, Brho, Crho, Drho, Gamma, isGammaExact, Delta, isDeltaExact )
% S = SSrho2FWS( Sysq, Gamma, isGammaExact, Delta, isDeltaExact )
%
%Parameters:
% S: FWR object (structuration)
% Arho, Brho, Crho, Drho: State-space ($\rho$-operator) matrices
% Sysq : initial classical state-space system, to be converted in $\rho$-operator realization
% Gamma : Vector of $\gamma_i$ parameters
% isGammaExact : 1 (default value) if we consider that the vector of $\gamma_i$ is exactly implemented
%              : 0 else
% Delta : Vector of $\Delta_i$
% isDeltaExact : 1 (default value) if the vector of $\Delta_i$ is exactly implemented
%              : 0 else
%
% $Id: SSrho2FWS.m 83 2008-04-18 13:00:31Z feng $

function S = SSrho2FWS( Arho, Brho, Crho, Drho, Gamma, isGammaExact, Delta, isDeltaExact )

% if "S = dSSrho2FWR( Sysq, Gamma, isGammaExact, Delta, isDeltaExact )"
if nargin==5
    Tem=Gamma;
end 
if (nargin==3) | (nargin==4) | (nargin==5)
    Sysq=Arho;
    Gamma=Brho;   
    if nargin==3
        Delta=Crho;
        isGammaExact=1;
        isDeltaExact=1;
    elseif nargin==4;
        Delta=Drho;
        isGammaExact=Crho;
        isDeltaExact=1;
    else 
        Delta=Drho;
        isGammaExact=Crho;
        isDeltaExact=Tem;
    end
    % compute equivalent Arho, Brho, Crho, Drho
    Arho = inv(diag(Delta))* (Sysq.A - diag(Gamma));
    Brho = inv(diag(Delta))*Sysq.B;
    Crho = Sysq.C;
    Drho = Sysq.D;
else
	Sysq = ss( Arho*diag(Delta)+diag(Gamma), diag(Delta)*Brho, Crho, Drho, 1);
	if nargin==6
        Delta=isGammaExact;
        isGammaExact=1;
        isDeltaExact=1;
	elseif nargin==7
        isDeltaExact=1;
	end
end
% create R and S
R = SSrho2FWR( Arho, Brho, Crho, Drho, Gamma, isGammaExact, Delta, isDeltaExact );
S = FWS(R, [], @RfunSSrho, {Sysq.A, Sysq.B, Sysq.C, Sysq.D,isGammaExact, Delta, isDeltaExact} , 'T', eye(size(Arho)), 'Gamma', Gamma, 'Delta', Delta);



% Rfun associated
function [R, cost_flag] = RfunSSrho( Rini, paramsValue, dataFWS )

%test if T is singular    
if (cond(paramsValue{1})>1e10)
    cost_flag=0;
    paramsValue{1} = eye(size(paramsValue{1}));
else
    cost_flag=1;
end
T=paramsValue{1};

R = SSrho2FWR( ss( inv(T)*dataFWS{1}*T, inv(T)*dataFWS{2}, dataFWS{3}*T, dataFWS{4},1), paramsValue{2}, dataFWS{5:end} );




%Description:
% The $\rho$-based state-space structure is presented in \\funcName[@FWR/SSrho2FWR]{SSrho2FWR} (see details therein).
%
%All equivalent $\delta$-state-space realizations (with same size) can be obtained by two methods, namely, the similarity transformation which is specified by a nonsingular matrix $T$ such that the corresponding $\rho$-state-space systems, after the coordinate transformation, can be described as $(T^{-1}A_\rho T,T^{-1}B_\rho,C_\rho T,D_\rho)$ and the modification of operator which is achieved by choosing different $\Delta_{i}$ and/or $\gamma_{i}$. So there are by consequence three parameters in the structuration's definition, \matlab{T}, \matlab{$\Delta$} and \matlab{$\gamma$}. \\
%
%See also: <SSrho2FWR>
