%Purpose:
% Build a $\rho$-DFIIt realization
% ($\rho$ Direct Form II transposed, according to Li and Zhao's work).
% This realization can be $L_2$-scaled or not
%
%Syntax:
% [R1, R2] = rhoDFIIt2ndFWRrelaxedL2( H, gamma, isGammaExact, delta, isDeltaExact)
%
%Parameters:
% R1: $\rho$DFIIt realization (FWR object)
% R2: equivalent $q$-state-space (sparse realization) FWR object
% H: 'tf' object
% gamma : vector of parameters $\gamma_k$
% isGammaExact : (default: true) boolean to express if $\gamma$ are exactly represented or not
% delta : vector or parameters $\Delta_k$
%         if they are not given, a $L_2$-scaling is performed ($\Delta_k$ then are induced)
%		  if they are negative, a relaxed-$L2$-scaling is performed ($\Delta_k$ then are induced)	
% isDeltaExact : (default: false) boolean to express if $\Delta_k$ are exactly represented or not
%
%
% $Id: rhoDFIIt2FWR.m 221 2009-03-09 16:56:47Z hilaire $


function [R1,R2] = rhoDFIIt2ndFWRrelaxedL2( num,den, gamma, isGammaExact, delta, isDeltaExact)

% input parameters 
if (nargin<6)
    isDeltaExact=0;
end
if (nargin<5)
    delta=zeros(size(gamma));
end
if (nargin<4)
    isGammaExact=1;
end

[R1,R2] = rhoDFIIt2ndFWR( num,den, gamma, isGammaExact, delta, isDeltaExact);
R = relaxedl2scaling(R1);


R1 = FWR( R.J, R.K, R.L, R.M, R.N, R.P, R.Q, R.R, R.S);

if (isGammaExact)
    R1.WP = zeros(size(R1.WP));
end
if (isDeltaExact)
    R1.WM = zeros(size(R1.WM));
end





%Description:
% The considered system \matlab{H} is re-parameterized as follows:
% \begin{equation}\label{eq:tfrho}
% 	H(z) = \frac{ \beta_0 + \beta_1 \varrho_1^{-1} + \hdots + \beta_{n-1} \varrho^{-1}_{n-1} + \beta_n \varrho^{-1}_{n} }{ 1 + \alpha_1 \varrho^{-1}_{1} + \hdots + \alpha_{n-1} \varrho^{-n+1}_{-1} + \alpha_n \varrho^{-1}_{n} }
% \end{equation}
% where 
% \begin{eqnarray}
% 	\varrho_i(z) &\triangleq& \prod_{j=1}^i \rho_j(z) \hspace{1cm} 1 \leq i \leq n \\
% 	\rho_i(z) &\triangleq& \frac{ z-\gamma_i }{ \Delta_i } \hspace{1cm} 1 \leq i \leq n
% \end{eqnarray}
% and $\pa{\gamma_i}_{1 \leq i \leq n}$ and $\pa{ \Delta_i>0 }_{1 \leq i \leq n}$ are two sets of constants.
% 
% Equation \eqref{eq:tfrho} can be, for example, implemented with a transposed direct form II with operators $\pa{ \rho_i^{-1} }_{1 \leq i \leq n}$, see figures \ref{fig:rhoDFIIt} and \ref{fig:rho_operator}.\\
% \fig[scale=0.4]{rhoDFIIt}{Generalized $\rho$ Direct Form II}
% \fig[scale=0.3]{rho_operator}{realization of operator $\rho_i^{-1}$}	
% Clearly, when $\gamma_i=0, \Delta_i=1\quad (1 \leq i \leq n)$, fig \ref{fig:rhoDFIIt} is the conventional transposed direct form II, and, with $\gamma_i=1, \Delta_i=\Delta\quad (1 \leq i \leq n)$, one gets the $\delta$ transposed direct form II.
%
% 	\subparagraph{$L_2$-scaling}
% 	According to \cite{Li04b}, the scaling is reached iff $d_k^2(W_c)_{kk}=1$, with $d_k$ are the diagonal parameters of the 
% 	transformation matrix, so such that $d_k=\pi_{i=1}^k \Delta_m$.\\
% 	The conditions gives
% 	\begin{equation*}
% 		\left\{\begin{array}{rcl}
% 			\Delta_1 &=& \sqrt{ (W_c)_{1,1} } \\
% 			\Delta_k &=& \sqrt{ \frac{ (W_c)_{k,k} }{ (W_c)_{k-1,k-1} } }, \hspace{5mm} k\geq 2 
% 		\end{array}\right.
% 	\end{equation*}
% 
% 	\subparagraph{$L_2$-scaling}
% 	Now, the conditions are changed in $1 \leq d_k^2(W_c)_{kk}<4$.\\
% 	So, $d_k$ should satisfy
% 	\begin{equation*}
% 		d_k = \frac{2^{\mathscr{F}_2(\sqrt{ (W_c)_{k,k} })}}{\sqrt{ (W_c)_{k,k} }}
% 	\end{equation*}
% 	Since $\Delta_k=\frac{d_{k-1}}{d_k}$, then
% 	\begin{equation*}
% 		\left\{\begin{array}{rcl}
% 			\Delta_1 &=& \sqrt{ (W_c)_{1,1} } 2^{-\mathscr{F}_2 (\sqrt{ (W_c)_{1,1} } ) } \\
% 			\Delta_k &=& \sqrt{ \frac{ (W_c)_{k,k} }{ (W_c)_{k-1,k-1} } } 2^{ \mathscr{F}_2 (\sqrt{ (W_c)_{k-1,k-1} } )-\mathscr{F}_2 (\sqrt{ (W_c)_{k,k} } ) }   , \hspace{5mm} k\geq 2 
% 		\end{array}\right.
% 	\end{equation*}

%See also: <rhoDFIIt2FWS>
%References:
% \cite{Li04b} G. Li and Z. Zhao. On the generalized DFIIt structure
% and its state-space realization in digital filter implementation.
% IEEE Trans. on Circuits and Systems, 51(4):769--778, April 2004

