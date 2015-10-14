%Purpose:
% Transform a $\delta$-state-space realization into a FWR object
%
%Syntax:
% R = SSdelta2FWR( Ad,Bd,Cd,Dd, Delta, isDeltaExact )
% R = SSdeltas2FWR( Sysq, Delta, isDeltaExact )
%
%Parameters:
% R: FWR object
% Ad,Bd,Cd,Dd: State-space (delta-operator) matrices
% Sysq: initial $q$-state-space system, to be converted in $\delta$-state-space
% Delta: $\Delta$ parameter of the $\delta$-realization
% isDeltaExact: 1 (default value) if $\Delta$ is exactly implemented
%			  : 0 else
%
% $Id: SSdelta2FWR.m 188 2008-12-18 16:05:13Z hilaire $


function R = SSdelta2FWR( Ad,Bd,Cd,Dd, Delta, isDeltaExact)

% if "R = deltasys2FWR( Sysq, Delta, isDeltaExact )"
if (nargin==2) | (nargin==3)
    Sysq=Ad;
    Delta=Bd;
    if nargin==2
        isDeltaExact=1;
    else
        isDeltaExact=Cd;
    end
    % compute equivalent Ad,Bd,Cd,Dd
    Ad = ( Sysq.A - eye(size(Sysq.A)) ) / Delta;
    Bd = Sysq.B / Delta;
    Cd = Sysq.C;
    Dd = Sysq.D;
else if nargin==5
        isDeltaExact=1;
    end
end

n=size(Ad,1);m=size(Cd,1);

% build FWR object
R = FWR( eye(n), Delta*eye(n), zeros(m,n), Ad, Bd, eye(n), zeros(size(Bd)), Cd, Dd);
if isDeltaExact
    R.WK = zeros(size(R.K));
end



%Description:
% The system considered is described by the equations
% \begin{equation}
% 	\left\lbrace\begin{array}{rcl}
% 		\delta[X(k)] &=& A_\delta X(k) + B_\delta U(k) \\
% 		Y(k) &=& C_\delta X(k) + D_\delta U(k)
% 	\end{array}\right.
% \end{equation}
% where the $\delta$-operator is defined by
% \begin{equation}
% 	\delta \triangleq \frac{q-1}{\Delta}
% \end{equation}
% and $\Delta$ is a strictly positive constant\footnote{In \cite{Midd90a}, $\Delta$ corresponds to the sampling period, but this constraint is removed in \cite{Geve93}}.\\
% The (finite precision) equivalent system, in the implicit state-space formalism, is given by
% \begin{equation}\label{eq:SSdetla2FWR:implicit_delta2}
% 	\begin{pmatrix}
% 		I_{n} & 0 & 0\\
% 		-\Delta I_{n} & I_{n} & 0\\
% 		0 & 0 & I_{p}
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k+1)\\
% 		X(k+1)\\
% 		Y(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmatrix}
% 		0 & A_\delta & B_\delta\\
% 		0 & I_{n} & 0\\
% 		0 & C_\delta & D_\delta\\
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k)\\
% 		X(k)\\
% 		U(k)
% 	\end{pmatrix}
% \end{equation}
% %		or
% %		\begin{equation}
% %			Z = 
% %			\begin{pmatrix}
% %				-I_n & A_\delta & B_\delta \\
% %				\Delta I_{n} & I_n & 0 \\
% %				0 & C_\delta & D_\delta
% %			\end{pmatrix}
% %		\end{equation}
% 
% If the system is given in classical state-space (\matlab{ss} object), the equivalent $\delta$-realization is obtained with :
% \begin{equation}
% 	A_\delta = \frac{A_q-I_n}{\Delta}, \quad B_\delta = \frac{B_q}{\Delta}, \quad C_\delta=C_q, \quad D_\delta = D_q
% \end{equation}
% The \matlab{isDeltaExact} parameter determines $W_K$.
% 
%See also: <SSdelta2FWS>
% 
%References:
% \cite{Midd90a} R.~Middleton and G.~Goodwin, Digital Control and
% Estimation, a unified approach, Prentice-Hall International Editions, 1990.
