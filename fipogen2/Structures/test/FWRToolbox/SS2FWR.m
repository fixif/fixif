%Purpose:
% Transform a classical state-space system ('ss' object) into a FWR object
%
%Syntax:
% R = SS2FWR( Aq,Bq,Cq,Dq )
% R = SS2FWR( Sys)
%
%Parameters:
% R: realization (FWR object)
% Aq,Bq,Cq,Dq: (classical) state-space matrices
% Sys: state-space system ('ss' object)
%
% $Id: SS2FWR.m 197 2008-12-23 15:16:19Z hilaire $

function R = SS2FWR(Aq,Bq,Cq,Dq)

if (nargin==1)
    S=Aq;
    Aq=S.A;
    Bq=S.B;
    Cq=S.C;
    Dq=S.D;
end

% dimensions of Aq,Bq,Cq,Dq
n=size(Aq,1);	p=size(Bq,2);
m=size(Cq,1);   l=0;	

% FWR
R = FWR( eye(l), zeros(n,l), zeros(m,l), zeros(l,n), zeros(l,p), Aq, Bq, Cq, Dq);



%Description:
% The system considered is described by the equations
% \begin{equation}
% 	\left\lbrace\begin{array}{rcl}
% 		X(k+1) &=& A_qX(k) + B_qU(k) \\
% 		Y(k) &=& C_qX(k) + D_qU(k)
% 	\end{array}\right.
% \end{equation}
% The (finite precision) equivalent system, in the implicit state-space formalism, is given by
% \begin{equation}
% 	\begin{pmatrix}
% 		. & . & .\\
% 		. & I_{n} & 0\\
% 		. & 0 & I_m
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k+1)\\
% 		X(k+1)\\
% 		Y(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmatrix}
% 		. & . & .\\
% 		. & A_q & B_q\\
% 		. & C_q & D_q\\
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k)\\
% 		X(k)\\
% 		U(k)
% 	\end{pmatrix}
% \end{equation}
% or
% \begin{equation}
% 	Z = 
% 	\begin{pmatrix}
% 		. & . & . \\
% 		. & A_q & B_q \\
% 		. & C_q & D_q
% 	\end{pmatrix}
% \end{equation}
% This is a particular case without any intermediate variables ($l=0$).
%
%See also: <SS2FWS>
