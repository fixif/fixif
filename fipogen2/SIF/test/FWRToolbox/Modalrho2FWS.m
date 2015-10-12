%Purpose: 
%Transform a $\rho$-modal realization into a FWS object, where the parameter $\Delta$ is reserved for relaxed $L_{2}$-scaling
%
%Syntax:
% S = Modalrho2FWS( SYS, Gamma,  Gamma, isGammaExact )
% S = Modalrho2FWS( Aq, Bq, Cq, Dq,  Gamma, isGammaExact )
%
%Parameters:
% S: FWS object
% SYS : Initial classical $q$-state-space system to be converted
% Aq,Bq,Cq,Dq : State-space ($q$-operator) matrices
% Gamma : Vector of $gamma_i$ parameters
% isGammaExact : 1 (default value) if we consider that the vector of $\gamma_i$ is exactly implemented
%              : 0 else
%
% $Id: Modalrho2FWS.m 83 2008-09-28 15:30:31Z feng $

function S = Modalrho2FWS( Aq, Bq, Cq, Dq,  Gamma, isGammaExact )

% if "S = Modalrho2FWS( SYS,  Gamma, isGammaExact )"

if (nargin==2) | (nargin==3)
    S=Aq;
    Gamma=Bq;
    if nargin==2
        isGammaExact=1;
    else
        isGammaExact=Cq;
    end
    Aq=S.A;
    Bq=S.B;
    Cq=S.C;
    Dq=S.D;
else if nargin==5
        isGammaExact=1;
    end
end
    
R = Modalrho2FWR( Aq, Bq, Cq, Dq,  Gamma, isGammaExact );
S = FWS(R, [], @RfunModalrho, { Aq, Bq, Cq, Dq, isGammaExact }, 'Gamma', Gamma);

function [R, cost_flag] = RfunModalrho( Rini, paramsValue, dataFWS )
    R = Modalrho2FWR ( ss( dataFWS{1}, dataFWS{2}, dataFWS{3}, dataFWS{4},1), paramsValue{1}, dataFWS{5} );
    cost_flag=1;

    
%Description:
%% The modal representation applied here is the same as that used in
% \funcName[@FWR/Modaldelta2FWR]{Modaldelta2FWR} (see the details therein),
% while $\Delta$ is reserved for relaxed $L_2$-scaling.
%
% Define the following series of $1^{st}$ polynomial operators, named $\rho$-operators:
% \begin{equation}\label{eq:Modalrho2FWS:rho_operator}
%     \rho_{i}=\frac{q-\gamma_{i}}{\Delta_{i}},\quad\forall i=1,2,\cdots,n
% \end{equation}
% with $\alpha_{i}$ and $\Delta_{i}>0$ are two sets of constants to determine. The particular choice $\alpha_{i}=0$ and $\Delta_{i}=1$ (resp. $\alpha_{i}=1$) leads to the shift operator (resp. the $\delta$-operator). The specialized implicit form related to the $\rho$-operator has the particular structure:
% \begin{equation}\label{eq:Modalrho2FWS:rho_implicit}
% \begin{pmatrix}
% 		I & 0 & 0 \\
% 		-\Delta & I & 0 \\
% 		0 & 0 & I \\
% 	\end{pmatrix}
% 	\begin{pmatrix}
%            T_{k+1} \\
%            X_{k+1} \\
%            Y_{k}
%          \end{pmatrix}
% 	=
%         \begin{pmatrix}
%         0 & A_{\rho} & B_{\rho} \\
%         0 & \gamma & 0 \\
%         0 & C_{\rho} & D_{\rho} \\
%         \end{pmatrix}
% 	\begin{pmatrix}
% 		T_{k} \\
% 		X_{k} \\
% 		U_{k}
% 	\end{pmatrix}
% \end{equation}
% 
% The condition of keeping equivalece is given as below:
% \begin{eqnarray}
% \label{eq:Modalrho2FWS:rho_state}A_{\rho}=\Delta^{-1}(\Lambda-1), B_{\rho}=\Delta^{-1}B, C_{\rho}=C~\hbox{and}~D_{\rho}=D\\
% \label{eq:Modalrho2FWS:Delta_gamma}\Delta=\hbox{diag}(\Delta_{1}~\cdots~\Delta_{n}),\quad\gamma=\hbox{diag}(\gamma_{1}~\cdots~\gamma_{n})
% \end{eqnarray}
% The \matlab{isGammaExact} parameters determines $W_P$.
%
%All equivalent $\delta$-state-space realizations (with same size) can be obtained by modification of operator which is achieved by choosing different $\gamma_{i}$. So there are only one parameter in the structuration's definition, namely \matlab{$\gamma$}. \\
%
%See also: <Modalrho2FWR>

%References:
% \cite{Feng09a} Y. Feng, P. Chevrel, and T. Hilaire. A practival strategy of an efficient and sparse FWL implementation of LTI filters. Submitted to ECC'09, 2009.\\

