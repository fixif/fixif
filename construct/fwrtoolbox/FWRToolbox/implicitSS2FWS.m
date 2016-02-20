%Purpose:
% Transform an implicit State-space system into a FWS object
%
%Syntax:
% S = implicitSS2FWS( Aq,Bq,Cq,Dq,Eq )
% S = implicitSS2FWS( Sys, Eq)
%
%Parameters:
% S: FWR object
% Aq,Bq,Cq,Dq : State-space ($q$-operator) matrices
% Eq: lower triangular matrix (default = identity)
% Sys: state-space system ('ss' object)
%
% $Id$


function S = implicitSS2FWS( Aq,Bq,Cq,Dq, Eq )

% args
switch nargin
    case 1
        S=Aq; Aq=S.A; Bq=S.B; Cq=S.C; Dq=S.D; Eq=eye(size(Aq));
    case 2
        S=Aq; Eq=Bq; Aq=S.A; Bq=S.B; Cq=S.C; Dq=S.D;
    case 4
        Eq=eye(size(Aq));
    otherwise
        error ('invalid number or arguments');
end

% dimensions of Aq,Bq,Cq,Dq
n=size(Aq,1);	p=size(Bq,2);
m=size(Cq,1);   l=n;	

% FWR / FWS
R = FWR( -Eq, eye(n), zeros(p,l), Aq, Bq, zeros(n,n), zeros(n,m), Cq, Dq);
S = FWS( R, @UYW_SSwithE, [], [], 'T', eye(R.n), 'E', zeros(1,(n*n-n)/2) );



% UYW function for the classical state-space structuration
function [U,Y,W,cost_flag] = UYW_SSwithE( Rini, paramsValue, dataFWS)

% build U,W    
if (cond(paramsValue{1})>1e10)
    cost_flag=0;
    paramsValue{1} = eye(size(paramsValue{1}));
else
    cost_flag=1;
end
U = paramsValue{1};
W = U;

% re-build E, build Y
E = paramsValue{2}';
d=1;
n=Rini.n;
for i=1:n
    E = [ E(1:(i-1)*n) ; d ; E((i-1)*n+1:end) ];
    d=[0; d];
end
Jtilde=reshape(E,[n  n]);
if (cond(Jtilde)>1e14)
    cost_flag=0;
    Jtilde=eye(size(Jtilde));
end
Y = Jtilde*inv(U)*inv(Rini.J);
   

%Description:
% 	The system considered is described by the equations:
% 	\begin{equation}
% 		\left\lbrace\begin{array}{rcl}
% 			E X(k+1) &=& A_qX(k) + B_qU(k) \\
% 			Y(k) &=& C_qX(k) + D_qU(k)
% 		\end{array}\right.
% 	\end{equation}
% 	where $E$ is a lower triangular matrix, with $1$ on the diagonal
% 	(like the $J$ matrix).\\
% 	The (finite precision) equivalent system, in the implicit
% 	state-space formalism, is given by
% 	\begin{equation}
% 		Z_0 = \begin{pmat}({||})
% 			-E & A & B \cr\-
% 			I_{n} & 0 & 0 \cr\-
% 			0 & C & D \cr
% 		\end{pmat}
% 	\end{equation}
% 	and equivalent realizations can be searched with the similarity
% 	\begin{equation}
% 		Z = \begin{pmat}({||})
% 			\mt{Y}^{-1} \cr\-
% 			& \mt{U}^{-1} \cr\-
% 			&& I_{p} \cr
% 		\end{pmat}
% 		Z_0
% 		\begin{pmat}({||})
% 			\mt{U}\cr\-
% 			& \mt{U} \cr\-
% 			&& I_{p} \cr
% 		\end{pmat}
% 	\end{equation}
% 	where $\mt{U}$ is a non-singular matrix and $\mt{Y}$ is chosen so that $\mt{Y}E\mt{U}$ is still lower triangular
% 	(in practice, the coefficients of the new matrix $E$ are chosen by the optimization algorithm, and $\mt{Y}$ 
% 	is then deduced).



%See also: <SS2FWS>

%References:
%	\cite{Hila07b} : T. Hilaire, P. Chevrel, and J. Whidborne. A unifying framework for finite wordlength realizations. IEEE Trans. on Circuits and Systems, 8(54), August 2007.
