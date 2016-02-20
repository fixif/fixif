%Purpose:
% Compute the open-loop transfer function sensitivity measure (and the
% sensitivity matrix)
%
%Syntax:
% [M MZ]  = MsensH(R)
%
%Parameters:
% M: sensitivity measure
% MZ: sensitivity matrix 
% R: FWR object
%
%
% $Id: MsensH.m 201 2009-01-03 22:31:50Z hilaire $


function [M, MZ] = MsensH( R)

% intermediate matrices
M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
M2 = [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ];
N1 = [ inv(R.J)*R.M; eye(R.n); zeros(R.m,R.n) ];
N2 = [ inv(R.J)*R.N; zeros(R.n,R.m); eye(R.m) ];
Te = 1;

% sensitivity matrix and sensitivity measure
[M, MZ] = w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, R.rZ );

%Description:
% 	The open-loop transfer function sensitivity measure is defined by
% 	\begin{equation}
% 		M_{L_{2}}^W = \norm{\dede{H}{Z} \times r_{Z}}_{F}^2.
% 	\end{equation}
% 	where $\dede{H}{Z}\in\Rbb{l+n+p}{l+n+q}$ is the \I{transfer function sensitivity matrix}.
% 	It is the matrix of the $L_{2}$-norm of the sensitivity of the transfer function $H$ with
% 	respect to each coefficient  $Z_{i,j}$. It is defined by
% 	\begin{equation}
% 		\pa{\dede{H}{Z}}_{i,j} \triangleq \norm{\dd{H}{Z_{i,j}}}_{2},
% 	\end{equation}
% 
% 	In SISO case, the $M_{L_{2}}^W$ measure is equal to 
% 	\begin{equation}
% 		M_{L_{2}}^W = \norm{\dd{H}{Z} \times r_{Z}}_2^2
% 	\end{equation}
% 	and is then an extension to the SIF of the classical state-space sensitivity measure
% 	\begin{equation}
% 		M_{L_2} \triangleq \norm{\dd{H}{A}}_2^2 + \norm{\dd{H}{B}}_2^2 + \norm{\dd{H}{C}}_2^2.
% 	\end{equation}
% 
% 	The $M_{L_2}^W$ measure can be evaluated by the following propositions
% 
% 	\begin{proposition}
% 		\begin{equation}
% 			\dd{H}{Z} =  H_1 \cd H_2
% 		\end{equation}
% 		where $H_1$ and $H_2$ are defined by
% 		\begin{eqnarray}
% 			H_1 : z &\mapsto& C_Z (zI_n-A_Z)^{-1} M_1 + M_2 \\
% 			H_2 : z &\mapsto& N_2 + N_1 (zI_n-A_Z)^{-1} B_Z 
% 		\end{eqnarray}
% 		with
% 		\begin{align}
% 			M_1 &\triangleq  \begin{pmatrix} KJ^{-1} & I_n & 0 \end{pmatrix}, &
% 			M_2 &\triangleq  \begin{pmatrix} LJ^{-1} & 0 & I_{p_2} \end{pmatrix}, \\
% 			N_1 &\triangleq  \begin{pmatrix} J^{-1}M \\ I_n \\ 0 \end{pmatrix}, &
% 			N_2 &\triangleq  \begin{pmatrix} J^{-1}N \\ 0 \\ I_{m_2} \end{pmatrix}.	
% 		\end{align}
% 	\end{proposition}
% 
% 	\begin{proposition}
% 		The transfer function sensitivity matrix $\dede{H}{Z}$ can be computed as
% 		\begin{equation}
% 			\pa{ \dede{H}{Z} }_{i,j} = \norm{ H_1 E_{i,j} H_2 }_2
% 		\end{equation}
% 		with
% 		\begin{equation}
% 			 H_1 E_{i,j} H_2 :=
% 			\left(\begin{array}{cc|c}
% 				A_Z & 0 & B_Z \\
% 				M_1 E_{i,j} N_1 & A & M_1 E_{i,j} N_2 \\
% 				\hline \vspace{-3.5mm}\\
% 				M_2 E_{i,j} N_1 & C_Z & M_2 E_{i,j} N_2
% 			\end{array}\right)
% 		\end{equation}
% 		and $E_{i,j}$ is the matrix of appropriate size with all elements being $0$ except the $(i,j)$th element which is unity.
% 	\end{proposition}
% 
% 	\begin{remark}
% 		In the SISO case, the problem becomes simpler by noting that
% 		\begin{align}
% 			\pa{ \dede{H}{Z} }_{i,j} &=  \norm{ (H_2H_1)_{i,j} }_2 \\
% 			&= \norm{
% 			\left(\begin{array}{cc|c}
% 				A_Z & 0 & B_Z \\
% 				M_1 N_1 & A_Z & M_1 N_2 \\
% 				\hline \vspace{-3.5mm}\\
% 				M_2 N_1 & C_Z & M_2 N_2
% 			\end{array}\right)_{i,j}}_2
% 		\end{align}	
% 		The $(l+n+1)\times(l+n+1)$ $H_2$-norm evaluations here require  only $l+n+1$ Lyapunov equations to be solved .
% 	\end{remark}

%See also: <@FWR/MsensH_cl>, <@FWR/w_prod_norm>
%References:
%	\cite{Hila07d}	T.�Hilaire and P.�Chevrel. On the compact
%	formulation of thederivation of a transfer matrix with respect to
%	another matrix. Technical Report RR-6760, INRIA, 2008.\\
%	\cite{Hila06a} T.�Hilaire, P.�Chevrel, and J.-P. Clauzel. Low
%	parametric sensitivity realization design for FWL implementation
%	of MIMO controllers : Theory and application to the active control of vehicle longitudinal oscillations. In Proc. of Control Applications of Optimisation CAO'O6, April 2006.\\
%	\cite{Hila07b} T.�Hilaire, P.�Chevrel, and J.�Whidborne. A
%	unifying framework for finite wordlength realizations. IEEE Trans.
%	on Circuits and Systems, 8(54), August 2007.\\


