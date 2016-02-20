%Purpose:
% Compute the open-loop pole sensitivity measure
% (and the pole sensitivity matrix) for a FWR object 
% 
%Syntax:
% [M, dlambda_dZ, dlk_dZ] = MsensPole( R, moduli)
%
%Parameters:
% M: pole sensitivity measure
% dlambda_dZ: the pole sensitivity matrix
% dlk_dZ: pole sensitivity matrices for each pole
% R: FWR object
% moduli : 1 (default value) : compute $\dd{\abs{\lambda}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
%        : 0 : compute $\dd{\lambda}{Z}$ (without the moduli)
%
% $Id: MsensPole.m 207 2009-01-05 13:03:51Z fengyu $


function [ M, dlambda_dZ, dlk_dZ] = MsensPole( R, moduli)

% args
if (nargin<2)
    moduli = 1;
end


M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
N1 = [ inv(R.J)*R.M; eye(R.n); zeros(R.m,R.n) ];

% measures
[dlambda_dZ, dlk_dZ] = deigdZ( R.AZ, M1, N1, size(R.Z) );

M = norm( dlambda_dZ .* R.rZ, 'fro' )^2;


%Description:
% 	The pole sensitivity measure of $\mathcal{R}$ is defined by
% 	\begin{equation}
% 		\Psi = \sum_{k=1}^n \norm{ \dd{\abs{\lambda_k}}{Z} \times r_Z }_F^2.
% 	\end{equation}
%	(it is also possible to only consider the sensitivity of $\lambda_k$ instead of the sensitivity of $\abs{\lambda_k}$. 
%
% 	This measure can be evaluated with
% 	\begin{equation}
% 		\dd{\abs{\lambda_k}}{Z} =
% 		\begin{pmatrix}	KJ^{-1} & I & 0 	\end{pmatrix}^\top
% 		\dd{\abs{\lambda_k}}{A}
% 		\begin{pmatrix} J^{-1}M \\ I \\ 0 \end{pmatrix}^\top
% 	\end{equation}
% 	and the following lemma\cite{Wu01}:
% 	\begin{lemma}\label{prop:MsensPole:dlambda}
% 		Let $M\in\Rbb{n}{n}$ be diagonalizable. Let $\pa{\lambda_{k}}_{1 \leq k \leq n}$ be its eigenvalues, and $\pa{x_{k}}_{1 \leq k \leq n}$ the corresponding right eigenvectors. Denote $M_{x} \triangleq \begin{pmatrix}x_{1} x_{2} \hdots x_{n}\end{pmatrix}$ and $M_{y} = \begin{pmatrix}y_{1} y_{2} \hdots y_{n}\end{pmatrix} \triangleq M_{x}^{-H}$. Then
% 		\begin{equation}\label{eq:MsensPole:dlambda}
% 			\dd{\lambda_{k}}{M} = y_{k}^\ast x_{k}^\top \hspace{3mm} \forall k=1,\hdots,n
% 		\end{equation}
% 			and
% 			\begin{equation}\label{eq:MsensPole:dmodulilambda}
% 				\dd{\abs{\lambda_{k}}}{M} = \frac{1}{\abs{\lambda_{k}}}Re\pa{\lambda_{k}^\ast \dd{\lambda_{k}}{M}}
% 			\end{equation}
% 	where $\cdot^\ast$ denotes the conjugate operation, $Re(\cdot)$ the real part and $\cdot^H$ the transpose conjugate operator.
% 	\end{lemma}
% 
% 	A \I{pole sensitivity matrix} can also be constructed to evaluate the overall impact of each coefficient. Let  $\dede{\abs{\lambda}}{Z}$ denote the pole sensitivity matrix defined by
% 	\begin{equation}
% 		\pa{\dede{\abs{\lambda}}{Z}}_{i,j} \triangleq \sqrt{ \sum_{k=1}^n \pa{\dd{\abs{\lambda_k}}{Z_{i,j}}}^2}.
% 	\end{equation}%
% 
% 	Then, The pole sensitivity measure is then given by:
% 	\begin{equation}
% 		\Psi=\norm{\dede{\abs{\lambda}}{Z} \times r_Z}_F^2.
% 	\end{equation}

%See also: <@FWR/MsensPole_cl>, <@FWR/Mstability>, <@FWR/deigdZ>, <@FWS/MsensPole>

%References:
%	\cite{Hila06b}	T.�Hilaire, P.�Chevrel, and J.-P. Clauzel. Pole
%	sensitivity stability related measure of FWL realization with the
%	implicit state-space formalism. In 5th IFAC Symposium on Robust Control Design (ROCOND'06), July 2006.\\
%	\cite{Hila07b}	T.�Hilaire, P.�Chevrel, and J.�Whidborne. A unifying framework for finite wordlength realizations. IEEE Trans. on Circuits and Systems, 8(54), August 2007.
