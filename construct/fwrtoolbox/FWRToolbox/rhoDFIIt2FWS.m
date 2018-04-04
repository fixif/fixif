%Purpose:
% Build a $\rho$-DFIIt structuration
% ($\rho$ Direct Form II transposed, according to Li and Zhao's work)
% this realization can be $L_2$-scaled or not
%
%Syntax:
% [S1, S2] = rhoDFIIt2FWS( H, gamma, isGammaExact, delta, isDeltaExact)
%
%Parameters:
% R1: $\rho$DFIIt structuration (FWS object)
% R2: equivalent $q$-state-space (sparse realization) FWS object
% H: 'tf' object
% gamma : vector of parameters $\gamma_k$
% isGammaExact : (default: true) boolean to express if $\gamma$ are exactly represented or not
% delta : vector or parameters $\Delta_k$
%         if they are not given, a $L_2$-scaling is performed ($\Delta_k$ then are induced)
% isDeltaExact : (default: false) boolean to express if $\Delta_k$ are exactly represented or not
%
% $Id: rhoDFIIt2FWS.m 235 2009-12-16 15:46:07Z hilaire $


function [S1,S2] = rhoDFIIt2FWS( H, gamma, varargin)

if length(varargin)==0
    varargin={1};
end

[R1,R2, flag] = rhoDFIIt2FWR( H, gamma, varargin{:});

S1 = FWS(R1, [], @RfunDFIIt1, { H, varargin{:} }, 'Gamma', gamma);
S2 = FWS(R2, [], @RfunDFIIt2, { H, varargin{:} }, 'Gamma', gamma);


% two Rfun
function [R, cost_flag] = RfunDFIIt1( Rini, paramsValue, dataFWS )
    [R,R2,cost_flag] = rhoDFIIt2FWR( dataFWS{1}, paramsValue{1}, dataFWS{2:end} );


    
function [R, cost_flag] = RfunDFIIt2( Rini, paramsValue, dataFWS )
    [R1,R,cost_flag] = rhoDFIIt2FWR( dataFWS{1}, paramsValue{1}, dataFWS{2:end} );


	
	
%See also: <rhoDFIIt2FWR>
%References:
% \cite{Li04b} G. Li and Z. Zhao. On the generalized DFIIt structure
% and its state-space realization in digital filter implementation. IEEE Trans. on Circuits and Systems, 51(4):769--778, April 2004