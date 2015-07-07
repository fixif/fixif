%Purpose:
% Compute the closed-loop transfer function sensitivity measure (and the
% sensitivity matrix)
%
%Syntax: 
% [M MZ]  = MsensH_cl( R, Sysp)
%
%Parameters:
% M: sensitivity measure
% MZ: sensitivity matrix 
% R: FWR object
% Sysp: plant system (ss object)
%
%
% $Id: MsensH_cl.m 207 2009-01-05 13:03:51Z fengyu $


function [M, MZ] = MsensH_cl( R, Sysp)

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
Bbar = [ B1 + B2*R.DZ*D21; R.BZ*D21 ];
Cbar = [ C1 + D12*R.DZ*C2 D12*R.CZ ];
Dbar = D11 + D12*R.DZ*D21;

% intermediate matrices
M1bar = [ B2*R.L*inv(R.J) zeros(np,n) B2;
          R.K*inv(R.J) eye(n) zeros(n,p2) ];
M2bar = [ D12*R.L*inv(R.J) zeros(m1,R.n) D12 ];      
N1bar = [ inv(R.J)*R.N*C2 inv(R.J)*R.M;
          zeros(n,np) eye(n);
          C2 zeros(m2,n) ];
N2bar = [ inv(R.J)*R.N*D21; zeros(R.n,p1); D21 ];


% sensitivity matrix and sensitivity measure
[M, MZ] = w_prod_norm( Abar,M1bar,Cbar,M2bar, Abar,Bbar,N1bar,N2bar, R.rZ );


%Description:
% 	The closed-loop transfer function sensitivity measure is very similar to the open-loop transfer function sensitivity. It is defined by
% 	\begin{equation}
% 		\bar{M}_{L_{2}}^W = \norm{\dede{\bar{H}}{Z} \times r_{Z}}_{F}^2.
% 	\end{equation}
% 	where $\dede{\bar{H}}{Z}\in\Rbb{l+n+p}{l+n+q}$ is the \I{transfer function sensitivity matrix}.
% 	It is the matrix of the $L_{2}$-norm of the sensitivity of the transfer function $\bar{H}$ with
% 	respect to each coefficient  $Z_{i,j}$. It is defined by
% 	\begin{equation}
% 		\pa{\dede{\bar{H}}{Z}}_{i,j} \triangleq \norm{\dd{\bar{H}}{Z_{i,j}}}_{2},
% 	\end{equation}
% 
% 	In SISO case, the $\bar{M}_{L_{2}}^W$ measure is equal to 
% 	\begin{equation}
% 		\bar{M}_{L_{2}}^W = \norm{\dd{\bar{H}}{Z} \times r_{Z}}_2^2.
% 	\end{equation}
% 
% 	The $M_{L_2}^W$ measure can be evaluated by the following
% 	propositions\cite{Hila07d}
% 
% 	\begin{proposition}
% 		\begin{equation}
% 			\dd{\bar{H}}{Z} =  \bar{H}_1 \cd \bar{H}_2
% 		\end{equation}
% 		where $H_1$ and $H_2$ are defined by
% 		\begin{eqnarray}
% 			\bar{H}_1 : z &\mapsto& \bar{C}\pa{ zI-\bar{A} }^{-1} \bar{M}_1 + \bar{M}_2 \\
% 			\bar{H}_2 : z &\mapsto& \bar{N}_1 \pa{ zI-\bar{A} }^{-1}\bar{B} + \bar{N}_2 
% 		\end{eqnarray}
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
% 				\end{pmatrix}\\
% 			\bar{M}_2 = \begin{pmatrix} D_{12}LJ^{-1} & 0 & D_{12} \end{pmatrix} &&
% 			\bar{N}_2 = \begin{pmatrix} J^{-1}ND_{21} \\ 0 \\ D_{21} \end{pmatrix}
% 		\end{eqnarray}
% 	\end{proposition}
% 

%See also: <@FWR/MsensH>, <@FWR/w_prod_norm>
%References:
%	\cite{Hila07d}	T. Hilaire and P. Chevrel. On the compact
%	formulation of the derivation of a transfer matrix with respect to
%	another matrix. Technical Report RR-6760, INRIA, 2008.\\
%	\cite{Hila07e}	T. Hilaire, P. Chevrel, and J. Whidborne. Low
%	parametric closed-loop sensitivity realizations using fixed-point
%	and floating-point arithmetic. In Proc. European Control Conference (ECC'07), July 2007.\\
%	\cite{Hila08b}	T. Hilaire, P. Chevrel, and J. Whidborne. Finite
%	wordlength controller realizations using the specialized implicit
%	form. Technical Report RR-6759, INRIA, 2008.\\

