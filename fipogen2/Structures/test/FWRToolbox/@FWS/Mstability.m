%Purpose:
% Compute the closed-loop pole sensitivity stability related measure for a FWS object.
% The computation is based on the UYW-transform
%
%Syntax:
% M = Mstability( S, U,Y,W, Sysp, moduli)
%
%Parameters:
% M: pole sensitivity measure
% S: FWS object
% U,Y,W : transformation matrices
% Sysp: plant system (ss object)
% moduli : 1 (default value) : compute $\dd{\abs{\bar\lambda}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
%        : 0 : compute $\dd{\bar\lambda}{Z}$ (without the moduli)
%
% $Id$



function M = Mstability( S, U,Y,W, Sysp, moduli)

% args
if (nargin<6)
    moduli = 1;
end


if isempty(S.dataMeasure)
    % first launch
    [M, dlambdabar_dZ, dlbk_dZ ] = MsensPole_cl( S.Rini, Sysp, moduli);
    M = MsensPole_cl( S.R, Sysp, moduli);
    S.dataMeasure = {dlbk_dZ};
    assignin('caller',inputname(1),S);
    % measure
    for k=1:size(dlbk_dZ,3)
        Psi(k) = norm( R.WZ, 'fro') * norm( dlbk_dZ(:,:,k) .* Z.rZ, 'fro');
    end
    M = min( (1-abs(lambda)) ./ Psi );
else
    % transform dlk_dZ
    dlbk_dZ = S.dataMeasure{1};
    k = size(dlk_dZ,3);
    l=length(Y); n=length(U);
    T1 = eye(l+n+S.R.p);  T1(1:l,1:l)=Y; T1(l+1:l+n,l+1:l+n)=inv(U);
    T2 = eye(l+n+S.R.m);  T2(1:l,1:l)=W; T2(l+1:l+n,l+1:l+n)=U;
    for i=1:k
        dlbk_dZ(:,:,i) = inv(T1)' * dlk_dZ(:,:,i) * inv(T2)';
    end
    
    % measure
    for k=1:size(dlbk_dZ,3)
        Psi(k) = norm( R.WZ, 'fro') * norm( dlbk_dZ(:,:,k) .* Z.rZ, 'fro');
    end
    M = min( (1-abs(lambda)) ./ Psi );
end


%Description:
% 	This function computes the closed-loop pole sensitivity stability
% 	related measure for a FWS object. It is based on the
% 	UYW-transform.\\
% 	If we consider $\mt{T}_1$ and $\mt{T}_2$ such that
% 	\begin{equation}
% 			Z_1 = \mt{T}_1	Z_0 \mt{T}_2
% 	\end{equation}
% 	\begin{equation}
% 		\mt{T}_1 = \begin{pmatrix}
% 			\mt{Y}\\
% 			&\mt{U}^{-1}\\
% 			&&I_{p}
% 		\end{pmatrix}, \hspace{5mm}
% 		\mt{T}_2 = \begin{pmatrix}
% 			\mt{W}\\
% 			&\mt{U}\\
% 			&&I_{m}
% 	\end{pmatrix}
%	\end{equation}
% 	then the sensitivity measure for $Z_1$ can be computed from the sensitivity for $Z_0$ with
% 	\begin{equation}
% 			\en{ \dd{\abs{\bar\lambda_k}}{Z} }_{Z_1} =  \mt{T}_1^{-\top} \en{ \dd{\abs{\bar\lambda_k}}{Z} }_{Z_0} \mt{T}_2^{-\top}
% 	\end{equation}
% 	These matrix $\en{ \dd{\abs{\bar\lambda_k}}{Z} }_{Z_0}$ are stored in the \matlab{dataMeasure} field.

%See also: <@FWR/Mstability>, <@FWS/MsensPole_cl>

%References:
%	\cite{Hila08b} T. Hilaire, P. Chevrel, and J. Whidborne. Finite wordlength controller realizations using the specialized implicit form. Technical Report RR-6759, INRIA, 2008.

