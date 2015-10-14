%Purpose:
% Compute the closed-loop pole sensitivity measure
% (and the pole sensitivity matrix) for a FWR object 
%
%Syntax:
% [M, dlambdabar_dZ, dlbk_dZ] = MsensPole_cl( R, Sysp, moduli)
%
%Parameters:
% M: pole sensitivity measure
% dlambdabar_dZ: the pole sensitivity matrix
% dlbk_dZ: pole sensitivity matrices for each pole
% R: FWR object
% Sysp: plant system (ss object)
% moduli : 1 (default value) : compute $\dd{\abs{\bar{\lambda}}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
%        : 0 : compute $\dd{\bar{\lambda}}{Z}$ (without the moduli)
%
% $Id: MsensPole.m 29 2007-03-07 15:14:18Z hilaire $


function [ M, dlambdabar_dZ, dlbk_dZ] = MsensPole_cl( R, Sysp, moduli)

% args
if (nargin<3)
    moduli = 1;
end

% sizes
np = size(Sysp.A,1);
m = size(Sysp.C,1);
p = size(Sysp.B,2);
l=R.l; m2=R.m; n=R.n; p2=R.p;
m1=m-m2;
p1=p-p2;
if ( (p1<0) | (m1<=0) )
    error('dimension error - check plant and realization dimension');
end


% plant matrices
B1 = Sysp.B(:,1:p1);
B2 = Sysp.B(:,p1+1:p);
C1 = Sysp.C(1:m1,:);
C2 = Sysp.C(m1+1:m,:);
D11 = Sysp.D(1:p1,1:m1);
D12 = Sysp.D(1:p1,m1+1:m);
D21 = Sysp.D(p1+1:p,1:m1);
D22 = Sysp.D(p1+1:p,m1+1:m);
if (D22~=zeros(size(D22)))
    error('D22 needs to be null')
end

% closedloop related matrices
Abar = [ Sysp.A + B2*R.DZ*C2 B2*R.CZ;
         R.BZ*C2 R.AZ];
% intermediate matrices
M1bar = [ B2*R.L*inv(R.J) zeros(np,n) B2;
          R.K*inv(R.J) eye(n) zeros(n,p2) ];
N1bar = [ inv(R.J)*R.N*C2 inv(R.J)*R.M;
          zeros(n,np) eye(n);
          C2 zeros(m2,n) ];


% measures          
[dlambdabar_dZ, dlbk_dZ] = deigdZ( Abar, M1bar, N1bar, size(R.Z), moduli);          
M = norm( dlambdabar_dZ .* R.rZ, 'fro' )^2;


%Description:
%	This measure is similar to the pole sensitivity measure in
%	open-loop case (see \funcName[@FWR/MsensPole]{MsensPole}), but the closed-loop
%	poles are now considered (the eigenvalues of $\bar{A}$).\\
% 	The pole sensitivity measure of $\mathcal{R}$ is defined by
% 	\begin{equation}
% 		\bar{\Psi} = \sum_{k=1}^n \norm{ \dd{\abs{\bar{\lambda}_k}}{Z} \times r_Z }_F^2.
% 	\end{equation}
% 
% 	This measure can be evaluated with
% 	\begin{equation}
% 		\dd{\abs{\bar{\lambda}_k}}{Z} = \bar{M}_1^top
% 		\dd{\abs{\bar{\lambda}_k}}{A} \bar{N}_1^\top
% 	\end{equation}
% 		with
% 		\begin{eqnarray}
% 			\bar{M}_1 = \begin{pmatrix}
% 				B_2LJ^{-1} & 0 & B_2 \\
% 				KJ^{-1} & I_n & 0
% 				\end{pmatrix} &&
% 			\bar{N}_1 =\begin{pmatrix}
% 				J^{-1}NC_2 & J^{-1}M \\
% 				0 & I_{n} \\
% 				C_2 & 0
% 				\end{pmatrix}
% 		\end{eqnarray}
% 	and the following lemma\cite{Wu01}:
% 	\begin{lemma}\label{prop:MsensPole_cl:dlambda}
% 		Let $M\in\Rbb{n}{n}$ be diagonalizable. Let $\pa{\lambda_{k}}_{1 \leq k \leq n}$ be its eigenvalues, and $\pa{x_{k}}_{1 \leq k \leq n}$ the corresponding right eigenvectors. Denote $M_{x} \triangleq \begin{pmatrix}x_{1} x_{2} \hdots x_{n}\end{pmatrix}$ and $M_{y} = \begin{pmatrix}y_{1} y_{2} \hdots y_{n}\end{pmatrix} \triangleq M_{x}^{-H}$. Then
% 		\begin{equation}\label{eq:MsensPole_cl:dlambda}
% 			\dd{\lambda_{k}}{M} = y_{k}^\ast x_{k}^\top \hspace{3mm} \forall k=1,\hdots,n
% 		\end{equation}
% 			and
% 			\begin{equation}\label{eq:MsensPole_cl:dmodulilambda}
% 				\dd{\abs{\lambda_{k}}}{M} = \frac{1}{\abs{\lambda_{k}}}Re\pa{\lambda_{k}^\ast \dd{\lambda_{k}}{M}}
% 			\end{equation}
% 	where $\cdot^\ast$ denotes the conjugate operation, $Re(\cdot)$ the real part and $\cdot^H$ the transpose conjugate operator.
% 	\end{lemma}
% 
% 	A \I{pole sensitivity matrix} can also be constructed to evaluate the overall impact of each coefficient. Let  $\dede{\abs{\bar{\lambda}}}{Z}$ denote the pole sensitivity matrix defined by
% 	\begin{equation}
% 		\pa{\dede{\abs{\bar{\lambda}}}{Z}}_{i,j} \triangleq \sqrt{ \sum_{k=1}^n \pa{\dd{\abs{\bar{\lambda}_k}}{Z_{i,j}}}^2}.
% 	\end{equation}%
% 
% 	Then, The pole sensitivity measure is then given by:
% 	\begin{equation}
% 		\Psi=\norm{\dede{\abs{\bar{\lambda}}}{Z} \times r_Z}_F^2.
% 	\end{equation}

%See also: <@FWR/MsensPole>, <@FWR/Mstability>, <@FWR/deigdZ>, <@FWS/MsensPole>

%References:
%	\cite{Hila08b} T. Hilaire, P. Chevrel, and J. Whidborne. Finite wordlength
%	controller realizations using the specialized implicit form. Technical Report RR-6759, INRIA, 2008.