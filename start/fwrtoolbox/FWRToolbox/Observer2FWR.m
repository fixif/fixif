%Purpose:
% Transform an Observer-State-Feedback form in FWR object
%
%Syntax:
% R = Observer2FWR( Sysp, Kc, Kf, Q )
%
%Parameters:
% R: FWR object
% Sysp : plant to be controlled ('ss' object)
% Kf, Kc, Q : observer-state-feedback parameters
%
% $Id$


function R = Observer2FWR( Sysp, Kc,Kf,Q)

% sizes
np = size(Sysp.A,1);
a = size(Sysp.C,1);
b = size(Sysp.B,2);

% FWR
R = FWR( [ eye(a) zeros(a,b) ; -Q eye(b) ], ... %J
         [ Kf Sysp.B ], ... % K
         [ zeros(b,a) eye(b) ], ... % L
         [ -Sysp.C ; -Kc ], ... % M
         [ eye(a) ; zeros(b,a) ], ... % N
         Sysp.A, ... % P
         zeros(np,a), ... % Q
         zeros(b,np), ... % R
         zeros(b,a) ... % S
       );
   
%Description:
% 	The system considered is described by the equations:
% 	\begin{equation}
% 		\left\lbrace\begin{array}{rcl}
% 			X(k+1) &=& A_pX(k) + B_pU(k) + K_f ( Y(k) - C_pX(k) ) \\
% 			U(k) &=& -K_cX(k) + Q( Y(k) - C_pX(k) )
% 		\end{array}\right.
% 	\end{equation}
% 	where $A_p$, $B_p$ and $C_p$ are the state-space matrices of the
% 	plant, $U(k)$ the $p$ input of the plant and $Y(k)$ its $m$ outputs.\\
%	$K_f$, $K_c$ and $Q$ are the parameters of the controller (see
%	\cite{Alaz99a} for more details).\\
% 	The (finite precision) equivalent system, in the implicit
% 	state-space formalism, is given by
% 	\begin{equation}
% 		Z_0 = \begin{pmat}({.||})
% 			I_p & 0 & -C_p & I_p  \cr
%			-Q & I_m & -K_c & 0 \cr\-
% 			K_f & B_p & A_p & 0 \cr\-
% 			0 & I_m & 0 & 0 \cr
% 		\end{pmat}
% 	\end{equation}

%References:
%	\cite{Hila05a} T. Hilaire, P. Chevrel, and Y. Trinquet. Implicit
%	state-space representation : a unifying framework for FWL
%	implementation of LTI systems. Proc. of the 16th IFAC World
%	Congress. Elsevier, July 2005.\\
%	\cite{Alaz99a} D. Alazard, C. Curres, P. Apkarian, M. Gauvrit, and G. Ferreses. Robustesse et Commande Optimale. Cepadues Edition, 1999.
