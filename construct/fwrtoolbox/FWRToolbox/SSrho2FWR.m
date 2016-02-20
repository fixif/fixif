%Purpose:
% Transform a $\rho$-based state-space realization into a FWR object
%
%Syntax:
% R = SSrho2FWR( Arho, Brho, Crho, Drho, Gamma, isGammaExact, Delta, isDeltaExact )
% R = SSrho2FWR( Sysq, Gamma, isGammaExact, Delta, isDeltaExact )
%
%Parameters:
% R: FWR object
% Arho, Brho, Crho, Drho: State-space ($\rho$-operator) matrices
% Sysq : Initial classical $q$-state-space system, to be converted in $\rho$-operator realization
% Gamma : Vector of $\gamma_i$ parameters
% isGammaExact : 1 (default value) if we consider that the vector of $\gamma_i$ is exactly implemented
%              : 0 else
% Delta : Vector of $\Delta_i$
% isDeltaExact : 1 (default value) if the vector of $\Delta_i$ is exactly implemented
%              : 0 else
%
% $Id: SSrho2FWR.m 83 2008-04-16 16:00:31Z feng $

function R = SSrho2FWR( Arho, Brho, Crho, Drho, Gamma, isGammaExact, Delta, isDeltaExact )

% if "R = dSSrho2FWR( Sysq, Gamma, isGammaExact, Delta, isDeltaExact )"
if nargin==5
    Tem=Gamma;
end 
if (nargin==3) | (nargin==4) | (nargin==5)
    Sysq=Arho;
    Gamma=Brho;   
    if nargin==3
        Delta=Crho;
        isGammaExact=1;
        isDeltaExact=1;
    elseif nargin==4;
        Delta=Drho;
        isGammaExact=Crho;
        isDeltaExact=1;
    else 
        Delta=Drho;
        isGammaExact=Crho;
        isDeltaExact=Tem;
    end
    % compute equivalent Arho, Brho, Crho, Drho
    Arho = inv(diag(Delta)) * (Sysq.A - diag(Gamma));
    Brho = inv(diag(Delta)) * Sysq.B;
    Crho = Sysq.C;
    Drho = Sysq.D;
elseif nargin==6
        Delta=isGammaExact;
        isGammaExact=1;
        isDeltaExact=1;
elseif nargin==7
        isDeltaExact=1;
end

n=size(Arho,1);m=size(Crho,1);

% build FWR object
R = FWR( eye(n), diag(Delta), zeros(m,n), Arho, Brho, diag(Gamma), zeros(size(Brho)), Crho, Drho);
R.WP = (~isGammaExact)*ones(size(R.WP));
R.WK = (~isDeltaExact)*ones(size(R.WK));




%Description:
% The system considered is described by the equations as follows:
% \begin{equation}
% 	\left\lbrace\begin{array}{rcl}
% 		\rho[X(k)] &=& A_{\rho} X(k) + B_{\rho} U(k) \\
% 		Y(k) &=& C_{\rho} X(k) + D_{\rho} U(k)
% 	\end{array}\right.
% \end{equation}
% where the $\rho$-operator is defined by
% \begin{equation}
% 	\rho_{i} \triangleq \frac{q-\gamma_{i}}{\Delta_{i}},\quad 1\leq i\leq n
% \end{equation}
% with $\gamma_{i}$ and $\Delta_{i}>0$ are two constants to determine. The particular choice $\gamma_{i}$=0 and $\Delta_{i}=1$ (resp. $\gamma_{i}$=1) leads to the shift operator $q$ (resp. the $\delta$-operator). \\
% The (finite precision) equivalent system, in the implicit state-space formalism, is given by
% \begin{equation}\label{eq:SSrho2FWR:implicit_rho}
% 	\begin{pmatrix}
% 		I_{n} & 0 & 0\\
% 		-\Delta & I_{n} & 0\\
% 		0 & 0 & I_{p}
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k+1)\\
% 		X(k+1)\\
% 		Y(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmatrix}
% 		0 & A_{\rho} & B_{\rho}\\
% 		0 & \gamma & 0\\
% 		0 & C_{\rho} & D_{\rho}\\
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k)\\
% 		X(k)\\
% 		U(k)
% 	\end{pmatrix}
% \end{equation}
% % 		or
% % 		\begin{equation}
% % 			Z = 
% % 		\begin{pmatrix}
% % 				-I_n & A_{\rho} & B_{\rho} \\
% % 				\Delta & \gamma & 0 \\
% % 				0 & C_{\rho} & D_{\rho}
% % 			\end{pmatrix}
% % 		\end{equation}
%where 
%\begin{equation*}
%\Delta=\hbox{diag}(\Delta_{1}~\cdots~\Delta_{n}),\quad\gamma=\hbox{diag}(\gamma_{1}~\cdots~\gamma_{n})
%\end{equation*}
%
% If the system is given in classical state-space (\matlab{ss} object), the equivalent $\rho$-realization is obtained with :
% \begin{equation}
% 	A_{\rho} = \Delta^{-1}(A_q-\gamma), \quad B_{\rho} = \Delta^{-1}B_q, \quad C_{\rho}=C_q, \quad D_{\rho} = D_q
% \end{equation}
% The \matlab{isDeltaExact} and the \matlab{isGammaExact} parameters determine respectively $W_K$ and $W_P$. 
%
%See also: <SSrho2FWS>, <SSdelta2FWR>