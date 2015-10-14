%Purpose:
% Transform a classical state-space system ('ss' object) into a FWS object
%
%Syntax:
% S = SS2FWS( Aq,Bq,Cq,Dq )
% S = SS2FWS( Sys)
%
%Parameters:
% S: structuration (FWS object)
% Aq,Bq,Cq,Dq: (classical) state-space matrices
% Sys: state-space system ('ss' object)
%
% $Id: SS2FWS.m 197 2008-12-23 15:16:19Z hilaire $


function S = SS2FWS( varargin)

R = SS2FWR( varargin{:} );
S = FWS( R, @UYW_SS, [], [], 'T', eye(R.n));



% UYW function for the classical state-space structuration
function [U,Y,W,cost_flag] = UYW_SS( Rini, paramsValue, dataFWS)

%test if T is singular    
if (cond(paramsValue{1})>1e10)
    cost_flag=0;
    paramsValue{1} = eye(size(paramsValue{1}));
else
    cost_flag=1;
end

% compute U,W,Y
Y = eye(0);
W = eye(0);
U = paramsValue{1};



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
% This is a particular case without any intermediate variables ($l=0$).\\
% All the state-space equivalent realizations (with same size) are given by the state-space systems $(T^{-1}A_qT,T^{-1}B_q,C_qT,D_q)$, where $T$ is a nonsingular matrix.
% So there is one parameter in the structuration's definition, named \matlab{T}. The equivalent realizations are obtained with $\mt{U}=T$, $\mt{Y}=\mt{W}=I_{l}$. If $Z_0$ is the initial realization, the other realizations are obtained with
% \begin{equation}
% 	Z = \begin{pmatrix} I_{l} \\ & T^{-1} \\ && I_{p} \end{pmatrix} Z_0 \begin{pmatrix} I_{l} \\ & T \\ && I_{m} \end{pmatrix}
% \end{equation}

%See also: <SS2FWR>
