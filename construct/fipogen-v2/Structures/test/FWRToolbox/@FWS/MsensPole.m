%Purpose:
% Compute the open-loop pole sensitivity measure for a FWS object.
% The computation is based on the UYW-transform
% 
%Syntax:
% M = MsensPole( S, U,Y,W, moduli)
%
%Parameters:
% M: pole sensitivity measure
% S: FWS object
% U,Y,W : transformation matrices
% moduli : 1 (default value) : compute $\dd{\abs{\lambda}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
%        : 0 : compute $\dd{\lambda}{Z}$ (without the moduli)
%
% $Id: MsensPole.m 204 2009-01-05 09:39:04Z hilaire $


function M = MsensPole( S, U,Y,W, moduli)

% args
if (nargin<5)
    moduli = 1;
end

if isempty(S.dataMeasure)
    % first launch
    [M, dlambda_dZ, dlk_dZ ] = MsensPole( S.Rini, moduli);
    M = MsensPole( S.R, moduli);
    S.dataMeasure = {dlk_dZ};
    assignin('caller',inputname(1),S);
else
    % transform dlk_dZ
    dlk_dZ = S.dataMeasure{1};
    k = size(dlk_dZ,3);
    l=length(Y); n=length(U);
    T1 = eye(l+n+S.R.p);  T1(1:l,1:l)=Y; T1(l+1:l+n,l+1:l+n)=inv(U);
    T2 = eye(l+n+S.R.m);  T2(1:l,1:l)=W; T2(l+1:l+n,l+1:l+n)=U;
    for i=1:k
        dlk_dZ(:,:,i) = inv(T1)' * dlk_dZ(:,:,i) * inv(T2)';
    end
    
    % dlambda_dZ
    for i=1:l+n+S.R.p
        for j=1:l+n+S.R.m
            %huhu = reshape(dlk_dZ(i,j,:), [k 1] );
            huhu(1:k) = dlk_dZ(i,j,:);
            dlambda_dZ(i,j) = norm( huhu, 'fro');
        end
    end
   
    % measure
    M = norm( dlambda_dZ .* S.R.rZ, 'fro' )^2;
end


%Description:
% 	This function computes the open-loop pole sensitivity measure for a FWS object. It is based on the $\mt{UYW}$-transform.
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
% 			\en{ \dd{\abs{\lambda_k}}{Z} }_{Z_1} =  \mt{T}_1^{-\top} \en{ \dd{\abs{\lambda_k}}{Z} }_{Z_0} \mt{T}_2^{-\top}
% 	\end{equation}
% 	These matrix $\en{ \dd{\abs{\lambda_k}}{Z} }_{Z_0}$ are stored in the \matlab{dataMeasure} field.

%See also: <@FWS/MsensPole_cl>, <@FWR/MsensPole>

%References:
%	\cite{Hila06b}	T. Hilaire, P. Chevrel, and J.-P. Clauzel. Pole
%	sensitivity stability related measure of FWL realization with the
%	implicit state-space formalism. In 5th IFAC Symposium on Robust Control Design (ROCOND'06), July 2006.\\
%	\cite{Hila07b}	T. Hilaire, P. Chevrel, and J. Whidborne. A unifying framework for finite wordlength realizations. IEEE Trans. on Circuits and Systems, 8(54), August 2007.
