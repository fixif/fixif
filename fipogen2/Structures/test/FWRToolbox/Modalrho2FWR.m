%Purpose: 
%Transform a $\rho$-modal realization into a FWR object, where the parameter $\Delta$ is reserved for relaxed $L_{2}$-scaling
%
%Syntax:
% R = Modalrho2FWR( SYS, Gamma,  Gamma, isGammaExact )
% R = Modalrho2FWR( Aq, Bq, Cq, Dq,  Gamma, isGammaExact )
%
%Parameters:
% R: FWR object
% SYS : Initial classical $q$-state-space system to be converted
% Aq,Bq,Cq,Dq : State-space ($q$-operator) matrices
% Gamma : Vector of $gamma_i$ parameters
% isGammaExact : 1 (default value) if we consider that the vector of $\gamma_i$ is exactly implemented
%              : 0 else
%
% $Id: Modalrho2FWR.m 83 2008-09-28 15:00:31Z feng $

function R = Modalrho2FWR( Aq, Bq, Cq, Dq,  Gamma, isGammaExact )

% if "R = Modalrho2FWR( SYS,  Gamma, isGammaExact )"

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
    
n=size(Aq,1);
% Construct q-based modal realisation with relaxed L2-scaling  
[A B C D] = canon_modal(  Aq, Bq, Cq, Dq );
R_modale = SS2FWR( A, B, C, D);
R_modale = relaxedl2scaling(R_modale);
%R_modale = l2scaling(R_modale);
R_modale = computeW(R_modale);
    
%L2-scaling on Tk
delta=zeros(1,n);
R_modale.Wc ;
Wt = R_modale.BZ*R_modale.BZ' + ( R_modale.AZ-diag(Gamma) )* R_modale.Wc * ( R_modale.AZ-diag(Gamma) )';
    
  for i=1:n
      delta(i) = 2^( floor( log2( sqrt( Wt( i, i ) ) ) ) );
      %delta(i) =  sqrt( Wt( i, i ) );
  end   
    
% compute equivalent Arho, Brho, Crho, Drho
Arho = inv(diag(delta)) * ( R_modale.AZ-diag(Gamma) );
Brho = inv(diag(delta)) * R_modale.BZ;
Crho = R_modale.CZ;
Drho = R_modale.DZ;


m=size(Crho,1);

% build FWR object
R = FWR( eye(n), diag(delta), zeros(m,n), Arho, Brho, diag(Gamma), zeros(size(Brho)), Crho, Drho);

R.WK = zeros(size(R.K));

if isGammaExact
    R.WP = zeros(size(R.P));
end



%Description:
% The modal representation applied here is the same as that used in
% \funcName[@FWR/Modaldelta2FWR]{Modaldelta2FWR} (see the details therein),
% while $\Delta$ is reserved for relaxed $L_2$-scaling.
%
% Define the following series of $1^{st}$ polynomial operators, named $\rho$-operators:
% \begin{equation}\label{eq:Modalrho2FWR:rho_operator}
%     \rho_{i}=\frac{q-\gamma_{i}}{\Delta_{i}},\quad\forall i=1,2,\cdots,n
% \end{equation}
% with $\alpha_{i}$ and $\Delta_{i}>0$ are two sets of constants to determine. The particular choice $\alpha_{i}=0$ and $\Delta_{i}=1$ (resp. $\alpha_{i}=1$) leads to the shift operator (resp. the $\delta$-operator). The specialized implicit form related to the $\rho$-operator has the particular structure:
% \begin{equation}\label{eq:Modalrho2FWR:rho_implicit}
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
% \label{eq:Modalrho2FWR:rho_state}A_{\rho}=\Delta^{-1}(\Lambda-1), B_{\rho}=\Delta^{-1}B, C_{\rho}=C~\hbox{and}~D_{\rho}=D\\
% \label{eq:Modalrho2FWR:Delta_gamma}\Delta=\hbox{diag}(\Delta_{1}~\cdots~\Delta_{n}),\quad\gamma=\hbox{diag}(\gamma_{1}~\cdots~\gamma_{n})
% \end{eqnarray}
% The \matlab{isGammaExact} parameters determines $W_P$.
%
%See also: <Modalrho2FWS>, <SSrho2FWR>
