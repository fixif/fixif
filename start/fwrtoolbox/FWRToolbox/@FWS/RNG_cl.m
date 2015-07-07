%Purpose:
% Compute the closed-loop Roundoff Noise Gain for a FWS.
% The computation is based on the UYW-transform
%
%Syntax:
% G = RNG_cl(S,U,Y,W, Plant, tol)
%
%Parameters:
% G: roundoff noise gain
% S: FWS object
% U,Y,W : transformation matrices
% Plant: ss of the plant
% tol: tolerance on trivial parameters (default=1e-8)
%
% $Id$


function G = RNG_cl( S, U,Y,W, Plant, tol)

if nargin==5
    tol=1e-8;
end

if isempty(S.dataMeasure)
    % first launch
    [G, dZ, M1M2Wobar] = RNG_cl( S.Rini, Plant, tol);
    G = RNG_cl( S.R, Plant, tol);
    S.dataMeasure = [ {dZ} {M1M2Wobar} ];
    assignin('caller',inputname(1),S);
else
    % get datas
    dZ = S.dataMeasure{1};
    M1M2Wobar = S.dataMeasure{2};
    
    l=length(Y); n=length(U);
    T1 = eye(l+n+S.R.p);  T1(1:l,1:l)=Y; T1(l+1:l+n,l+1:l+n)=inv(U);
    %T2 = eye(l+n+S.R.m);  T2(1:l,1:l)=W; T2(l+1:l+n,l+1:l+n)=U;

    
    G = trace( inv(T1)*dZ*inv(T1') * M1M2Wobar );
    
end
   

%Description:
% 	This function computes the closed-loop Roundoff Noise Gain for a FWS. The computation is based on the UYW-transform.\\
% 	It is based on the \funcName[@FWR/RNGcl]{RNG\_cl} function.\\
% 	The matrix $d_Z$ is computed once and stored in the
% 	\matlab{dataMeasure} field.

%See also: <@FWS/RNG>, <@FWR/RNG_cl>

%References:
%	\cite{Hila08b} T. Hilaire, P. Chevrel, and J. Whidborne. Finite wordlength controller realizations using the specialized implicit form. Technical Report RR-6759, INRIA, 2008.

