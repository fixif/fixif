%Purpose:
% Transform a $\delta$-state-space realization into a FWS object
%
%Syntax:
% S = SSdelta2FWR( Ad,Bd,Cd,Dd, Delta, isDeltaExact )
% S = SSdeltas2FWR( Sysq, Delta, isDeltaExact )
%
%Parameters:
% S: FWR object (structuration)
% Ad,Bd,Cd,Dd: State-space ($\delta$-operator) matrices
% Sysq: initial $q$-state-space system, to be converted in $\delta$-state-space
% Delta: $\Delta$ parameter of the $\delta$-realization
% isDeltaExact: 1 (default value) if $\Delta$ is exactly implemented
%			  : 0 else
%
% $Id: SSdelta2FWS.m 203 2009-01-04 14:03:56Z hilaire $


function S = SSdelta2FWS( varargin)

R = SSdelta2FWR( varargin{:} );

S = FWS( R, @UYW_SSdelta, [], [], 'T', eye(R.n));



% UYW function for the classical state-space structuration
function [U,Y,W,cost_flag] = UYW_SSdelta( Rini, paramsValue, dataFWS)

%test if T is singular    
if (cond(paramsValue{1})>1e10)
    cost_flag=0;
    paramsValue{1} = eye(size(paramsValue{1}));
else
    cost_flag=1;
end

% compute U,W,Y
Y = inv(paramsValue{1});
W = paramsValue{1};
U = paramsValue{1};



%Description:
% The $\delta$-based state-space structure is presented in \funcName[@FWR/SSdelta2FWR]{SSdelta2FWR} (see details therein).
% 
% All the $\delta$-state-space equivalent realizations (with same size) are given by the $\delta$-state-space systems $$(T^{-1}A_\delta T,T^{-1}B_\delta,C_\delta T,D_\delta),$$ where $T$ is a nonsingular matrix.
% 
% So there is one parameter in the structuration's definition, named \matlab{T}. The equivalent realizations are obtained with $\mt{U}=\mt{W}=T$, $\mt{Y}=T^{-1}$. If $Z_0$ is the initial realization, the other realizations are obtained with
% \begin{equation}
% 	Z = \begin{pmatrix} T^{-1} \\ & T^{-1} \\ && I_{p} \end{pmatrix} Z_0 \begin{pmatrix} T \\ & T \\ && I_{m} \end{pmatrix}
% \end{equation}
%
%See also: <SSdelta2FWR>