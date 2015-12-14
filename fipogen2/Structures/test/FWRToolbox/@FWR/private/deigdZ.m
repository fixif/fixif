%Purpose:
% Compute $M_1^\top \dd{\lambda}{A} M_2^\top$.
% This function used to compute the pole sensitivity (open-loop and closed-loop)
%
%Syntax:
% [dlambda_dZ, dlk_dZ] = dleigdZ( A, M1, M2, Z, moduli)
%
%Parameters:
% dlambda_dZ: the pole sensitivity matrix
% dlk_dZ: pole sensitivity matrices for each pole
% A: matrix from whom the eigenvalues are taken
% M1,M2: such that $\dd{\lambda}{Z} = M1^\top \dd{\lambda}{A} M2^\top$
% moduli : 1 (default value) : compute $\dd{\abs{\lambda}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
%        : 0 : compute $\dd{\lambda}{Z}$ (without the moduli)
%
% $Id$


function [dlambda_dZ, dlk_dZ] = dleigdZ( A, M1, M2, sizeZ, moduli)

% args
if nargin<5
	moduli=1;
end


[Mx,Dlambda] = eig(A);
My = inv(Mx)';
lambda=diag(Dlambda)';


% sensitivity matrix
dlk_dZ = zeros( sizeZ(1), sizeZ(2), size(Dlambda,1) );
for k=1:size(Dlambda,1)
    if (moduli==1)
        % MAYBE A PROBLEM HERE BECAUSE ALL VALUES BUT FIRST ARE ALWAYS ZERO
        dlk_dZ(:,:,k) = M1' * ( 1/abs(lambda(k)) * real(conj( lambda(k) * conj(My(:,k))*transpose(Mx(:,k)) )) ) * M2';
    else
        dlk_dZ(:,:,k) = M1' * ( conj(My(:,k))*transpose(Mx(:,k)) ) * M2';
    end
end

% dlambda_dZ
for i=1:sizeZ(1)
    for j=1:sizeZ(2)
        huhu(1:size(Dlambda,1)) = dlk_dZ(i,j,:);
        dlambda_dZ(i,j) = norm( huhu, 'fro');
    end
end


%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function computes
% 	\begin{equation}
% 		M_1^\top \dd{\lambda_k}{A} M_2^\top
% 	\end{equation}
% 	where the $\lambda_k$ are the eigenvalues of $A$.\\
% 	This is done by the followin lemma\cite{Wu01}:
% 	\begin{lemma}
% 		Let $M\in\Rbb{n}{n}$ be diagonalisable. Let $\pa{\lambda_{k}}_{1 \leq k \leq n}$ be its eigenvalues, and $\pa{x_{k}}_{1 \leq k \leq n}$ the corresponding right eigenvectors. Denote $M_{x} \triangleq \begin{pmatrix}x_{1}, x_{2}, \hdots, x_{n}\end{pmatrix}$ and $M_{y} = \begin{pmatrix}y_{1}, y_{2}, \hdots, y_{n}\end{pmatrix} \triangleq M_{x}^{-H}$. Then
% 		\begin{equation}\label{eq:dlambda}
% 			\dd{\lambda_{k}}{M} = y^\ast_{k}x_{k}^\top \hspace{3mm} \forall k=1,\hdots,n
% 		\end{equation}
% 			and
% 			\begin{equation}\label{eq:dmodulilambda}
% 				\dd{\abs{\lambda_{k}}}{M} = \frac{1}{\abs{\lambda_{k}}}Re\pa{\lambda_{k}^\ast\dd{\lambda_{k}}{M}}
% 			\end{equation}
% 	where $\cdot^\ast$ denotes the conjugate operation, $Re(\cdot)$ the real part and $\cdot^H$ the transpose conjugate operator.
% 	\end{lemma}


%See also: <@FWR/MsensPole>, <@FWR/MsensPole_cl>, <@FWR/Mstability>
