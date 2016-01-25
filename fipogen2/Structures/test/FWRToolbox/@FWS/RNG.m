%Purpose:
% Compute the open-loop Roundoff Noise Gain for a FWS.
% The computation is based on the UYW-transform
%
%Syntax:
% G = RNG(S,U,Y,W)
%
%Parameters:
% G: roundoff noise gain
% S: FWS object
% U,Y,W : transformation matrices
%
% $Id: RNG.m 204 2009-01-05 09:39:04Z hilaire $


function G = RNG( S, U,Y,W, tol)

if nargin==4
    tol=1e-8;
end

if isempty(S.dataMeasure)
    % first launch
    [G, dZ] = RNG( S.Rini, tol);
    G = RNG( S.R, tol);
    S.dataMeasure = [ {dZ} ];
    assignin('caller',inputname(1),S);
else
    % get datas
    dZ = S.dataMeasure{1};
    % compute the new measure
    % M1 = [ S.R.K*inv(S.R.J) eye(S.R.n) zeros(S.R.n,S.R.m) ]; % JOA maybe there's a problem on this line S.R.m not coherent with previous defs
    M1 = [ S.R.K*inv(S.R.J) eye(S.R.n) zeros(S.R.n,S.R.p) ]; 
    M2 = [ S.R.L*inv(S.R.J) zeros(S.R.p,S.R.n) eye(S.R.p) ];
    G = trace( dZ * ( M2'*M2 + M1'*S.R.Wo*M1 ) );
    
end


%Description:
% 	This function computes the open-loop Roundoff Noise Gain for a FWS. The computation is based on the $\mt{UYW}$-transform.\\
% 	It is based on the \funcName[@FWR/RNG]{RNG} function.\\
% 	The matrix $d_Z$ is computed once and stored in the \matlab{dataMeasure} field.

%See also: <@FWR/RNG>

%References:
%	\cite{Hila07c} T.�Hilaire, D.�M�nard, and O.�Sentieys. Roundoff noise analysis of finite wordlength realizations with the implicit state-space framework. In 15th European Signal Processing Conference (EUSIPOC'07), September 2007.
