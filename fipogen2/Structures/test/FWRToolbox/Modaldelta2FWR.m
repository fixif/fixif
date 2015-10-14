%Purpose:
% Transform a $\delta$-based modal realization into a FWR object
% , and this realization can be relaxed $L_{2}$-scaled or not.
%
%Syntax:
% R = Modaldelta2FWR( SYS, Delta, isDeltaExact )
% R = Modaldelta2FWR( Aq, Bq, Cq, Dq, Delta, isDeltaExact )
%
%Parameters:
% R: FWR object
% SYS : 'ss' object
% Aq,Bq,Cq,Dq : State-space ($q$-operator) matrices
% Delta : Vector of $\Delta_i$. If they are not given, a relaxed $L_2$-scaling is performed ($\Delta_k$ then are induced)
% isDeltaExact : 1 if the vector of $\Delta_i$ is exactly implemented
%              : 0 (default value) else
%
% $Id: Modaldelta2FWR.m 83 2008-09-26 16:00:31Z feng $

function R = Modaldelta2FWR( Aq, Bq, Cq, Dq, Delta, isDeltaExact )

% if "R = Modaldelta2FWR( SYS, Delta, isDeltaExact )"

if (nargin==1)
    S=Aq;
    Aq=S.A;
    Bq=S.B;
    Cq=S.C;
    Dq=S.D;
    Delta=zeros(1, size(Aq,1));
     isDeltaExact=1;
%     isDeltaExact=0;
end
if (nargin==2)
    S=Aq;
    Delta=Bq;
    Aq=S.A;
    Bq=S.B;
    Cq=S.C;
    Dq=S.D; 
%     isDeltaExact=1;
    isDeltaExact=0;
end
if (nargin==3)
    S=Aq;
    Delta=Bq
    isDeltaExact=Cq;
    Aq=S.A;
    Bq=S.B;
    Cq=S.C;
    Dq=S.D; 
end

if (nargin==4)
    Delta=zeros(1, size(Aq,1))
%     isDeltaExact=1;
    isDeltaExact=0;
end
if (nargin==5)
%     isDeltaExact=1;
    isDeltaExact=0;
end

n=size(Aq,1);
% Construct q-based modal realisation
[A B C D] = canon_modal(  Aq, Bq, Cq, Dq);
R_modale = SS2FWR( A, B, C, D);

% compute delta (leading to a L_2-scaled realization) 
% when delta is not given (or null)
if (Delta==zeros(1,size(Aq,1)))
 R_modale = relaxedl2scaling(R_modale);
%R_modale = l2scaling(R_modale);
R_modale = computeW(R_modale);
    
%L2-scaling on Tk
R_modale.Wc ;
Wt = R_modale.BZ*R_modale.BZ' + ( R_modale.AZ-eye(n) )* R_modale.Wc * ( R_modale.AZ-eye(n) )';
    
  for i=1:n
      Delta(i) = 2^( floor( log2( sqrt( Wt( i, i ) ) ) ) );
     % Delta(i) =  sqrt( Wt( i, i ) ) ;
  end   
end   
% compute equivalent Ad, Bd, Cd, Dd
Ad = inv(diag(Delta)) * ( R_modale.AZ-eye(n) );
Bd = inv(diag(Delta)) * R_modale.BZ;
Cd = R_modale.CZ;
Dd = R_modale.DZ;

%Wt = Bd*Bd' + Ad* R_modale.Wc * Ad'

m=size(Cd,1);

% build FWR object
R = FWR( eye(n), diag(Delta), zeros(m,n), Ad, Bd, eye(n), zeros(size(Bd)), Cd, Dd);
if (isDeltaExact)
    R.WK = zeros(size(R.K));
end



%Description:
% Let consider the following transfer function given and its related modal realization $(\Lambda, B, C, D)$:
% \begin{equation}\label{eq:Modaldelta2FWR:modal_transfer_function}
% \begin{split}
%   H(z) & =D+C(zI-\Lambda)^{-1}B \\
%     & =D+\sum_{i=1}^{n}\frac{c_{i}b{i}}{1-\lambda_{i}z^{-1}}
% \end{split}
% \end{equation}
% with $\lambda_{i}\neq\lambda_{j}$ for all $i\neq j$ so that $\Lambda$ may be chosen as a diagonal matrix.\\
% 
% The modal representation is not unique since $B$ and $C$ may be scaled and the diagonal elements of $\Lambda$ may be permuted in different ways so as to to produce the same transfer function. One invariant however is that is decouples the dynamic modes $\lambda_{i}$ and is closely related to partial-fraction expansion of $H(z)$. Rather to diagonalize the $A$-matrix, it is preferred in the sequel to combine the complex-conjugate pole-pairs to form a real ``block-diagonal'' section in which $\Lambda$ has two-by-two real matrices along its diagonal as follows:
% \begin{equation}\label{eq:Modaldelta2FWR:modal_representation}
%     \Lambda=\begin{pmatrix}
%                 \alpha_{1} & \beta_{1} &  &  &  &  &  \\
%                 \beta_{2} & \alpha_{2} &  &  &  &  &  \\
%                  &  & \alpha_{3} & \beta_{3} &  &  &  \\
%                  &  & \beta_{4} & \alpha_{4} &  &  &  \\
%                  &  &  &  & \ddots &  &  \\
%                  &  &  &  &  & \alpha_{n-1} & \beta_{n-1} \\
%                  &  &  &  &  & \beta_{n} & \alpha_{n} \\
%             \end{pmatrix}
% \end{equation}
% where $\alpha_{i}$ and $\beta_{i}$ are linked to the real part and the
% imaginary part of the $i^{th}$ pole, respectively. If the $i^{th}$ pole is real, then $\beta_{i}=0$; if the $i^{th}$ and $(i+1)^{th}$ poles are complex-conjugate, then $\alpha_{i}=\alpha_{i+1}$ and $\beta_{i}=-\beta_{i+1}=Im(\lambda_{i})$.\\
% 
% The system considered is described by the equations
% \begin{equation}
% 	\left\lbrace\begin{array}{rcl}
% 		\delta[X(k)] &=& A_\delta X(k) + B_\delta U(k) \\
% 		Y(k) &=& C_\delta X(k) + D_\delta U(k)
% 	\end{array}\right.
% \end{equation}
% where the $\delta$-operator is defined by
% \begin{equation}
% 	\delta_i \triangleq \frac{q-1}{\Delta_i}
% \end{equation}
% and $\Delta_i$ is a strictly positive constant.\\
% The (finite precision) equivalent system, in the implicit state-space formalism, is given by
% \begin{equation}\label{eq:modaldelta2FWR:implicit_delta2}
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
% where
% \begin{equation*}
% \Delta=\hbox{diag}(\Delta_{1}~\cdots~\Delta_{n})
% \end{equation*}
% If the system is given in classical state-space (\matlab{ss} object), the equivalent $\delta$-realization is obtained with :
% \begin{equation}
% 	A_\delta = \Delta^{-1}(\Lambda-I_n), \quad B_\delta = \Delta^{-1}B,
% 	\quad C_\delta=C, \quad D_\delta = D
% \end{equation}
% The \matlab{isDeltaExact} parameter determines $W_K$.
% 
%See also: <Modalrho2FWR>
% 
%References:
% \cite{Midd90a} R.~Middleton and G.~Goodwin, Digital Control and Estimation, a unified approach, Prentice-Hall International Editions, 1990.\\
%  \cite{Feng09a} Y. Feng, P. Chevrel, and T. Hilaire. A practival strategy of an efficient and sparse fwl implementation of lti filters. In submitted to ECC'09, 2009.\\
