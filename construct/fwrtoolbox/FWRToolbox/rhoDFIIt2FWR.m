%Purpose:
% Build a $\rho$-DFIIt realization
% ($\rho$ Direct Form II transposed, according to Li and Zhao's work).
% This realization can be $L_2$-scaled or not
%
%Syntax:
% [R1, R2 flag] = rhoDFIIt2FWR( H, gamma, isGammaExact, delta, isDeltaExact)
%
%Parameters:
% R1: $\rho$DFIIt realization (FWR object)
% R2: equivalent $q$-state-space (sparse realization) FWR object
% flag: indicates if the rhoDFIIt can be computed (1=> ok)
% H: 'tf' object
% gamma : vector of parameters $\gamma_k$
% isGammaExact : (default: true) boolean to express if $\gamma$ are exactly represented or not
% delta : vector or parameters $\Delta_k$
%         if they are not given, a $L_2$-scaling is performed ($\Delta_k$ then are induced)
%		  if they are negative, a relaxed-$L2$-scaling is performed ($\Delta_k$ then are induced)	
% isDeltaExact : (default: false) boolean to express if $\Delta_k$ are exactly represented or not
%
%
% $Id: rhoDFIIt2FWR.m 259 2013-04-24 16:49:11Z hilaire $


function [R1,R2, flag] = rhoDFIIt2FWR( H, gamma, isGammaExact, delta, isDeltaExact)

% input parameters 
if (nargin<5)
    isDeltaExact=0;
end
if (nargin<4)
    delta=zeros(size(gamma));
end
if (nargin<3)
    isGammaExact=1;
end

num = H.num{1};
den = H.den{1};
Va = den'/den(1);
Vb = num'/den(1);
p1=length(Va)-1;
p2=length(Vb)-1;
p3=length(gamma);
p4=length(delta);

if ( all([p2 p3 p4]==p1) )
    p=p1;
else
    error('errors in dimensions')
end

    
%=====================================
% step 1 : build Valpha_bar, Vbeta_bar
% by considering Delta_k=1 forall k

% build Tbar
Tbar=zeros(p+1,p+1);
Tbar(p+1,p+1)=1;
for i=p:-1:1
    Tbar(i,i:p+1) = poly( gamma(i:p) );
end

if cond(Tbar)>1e20
	flag = 0;
    R1=[];
    R2=[];
	return
end;

% Valpha_bar and Vbeta_bar
Valpha_bar = inv(Tbar)'*Va;
Vbeta_bar = inv(Tbar)'*Vb;

% equivalent state-space (Abar,Bbar,Cbar,Dbar)
A0 = diag(ones(p-1,1),1);
A0(1:end,1) = -Valpha_bar(2:end);
Abar = diag(gamma) + A0;
Bbar = Vbeta_bar(2:end) - Vbeta_bar(1)*Valpha_bar(2:end);
Cbar = zeros(1,p); Cbar(1,1) = 1;
Dbar = Vbeta_bar(1);


%====================
% step 2 : l2-scaling

% compute delta (leading to a l2-scaled realization) 
% when delta is not given (or null)
Sbar = ss(Abar,Bbar,Cbar, Dbar,1);
Wc = gram(Sbar,'c');

if (delta==zeros(size(gamma)))

    delta(1) = sqrt( Wc(1,1) );
    for i=2:p
		delta(i) = sqrt( Wc(i,i) / Wc(i-1,i-1) );
	end
	
elseif (delta(1)<0)	% relaxed L2-scaling wanted	

    delta(1) = sqrt( Wc(1,1) ) * 2^-F2(sqrt( Wc(1,1) ));
    for i=2:p
		delta(i) = sqrt( Wc(i,i) / Wc(i-1,i-1) ) * 2^( F2(sqrt(Wc(i-1,i-1))) - F2(sqrt(Wc(i,i))) );
	end
	
end


% compute Valpha and Vbeta
Tbar=zeros(p+1,p+1);
Tbar(p+1,p+1)=1;
for i=p:-1:1
    Tbar(i,i:p+1) = poly( gamma(i:p) ) / prod( delta(i:p) );
end
Ka = prod(delta(:));
Valpha = inv(Ka*Tbar)'*Va;
Vbeta = inv(Ka*Tbar)'*Vb;


% equivalent l2-scaled state-space
d=zeros(p,1);
for i=1:p
    d(i) = inv( prod(delta(1:i)) );
end
Tsc = diag(d);
A = Tsc*Abar*inv(Tsc);
B = Tsc*Bbar;
C = Cbar*inv(Tsc);
D = Dbar;   % can also be computed from Valpha and Vbeta
S = ss(A,B,C,D,1);
A0 = diag(ones(p-1,1),1);
A0(1:end,1) = -Valpha(2:end);


%================================
% step 3 : build FWR object
R2 = SS2FWR(S); 
if (isGammaExact)
    for i=2:p
        R2.WP(i,i)=0;
    end
end
if (isDeltaExact)
    for i=2:p
        R2.WP(i-1,i)=0;
    end
end

% old version, with Delta multiplication before the add...
% R1 = FWR( eye(p+1), zeros(p,p+1), zeros(1,p+1), zeros(p+1,p), zeros(p+1,1), diag( gamma(p:-1:1) ), zeros(p,1), zeros(1,p), zeros(1,1) );
% R1.J(2:p+1) = Valpha(p+1:-1:2);
% R1.K(1:p,2:p+1) = diag( delta(end:-1:1) );
% R1.L(1) = 1;
% R1.M(1,p) = 1; R1.M(2:p+1,1:p) = diag( ones(p-1,1), -1);
% R1.N(1) = Vbeta(1); R1.N(2:p+1) = Vbeta(p+1:-1:2);

%second version
K=diag( ones(1,p-1),1);
K(:,1) = -Valpha(2:p+1);
R1 = FWR( eye(p), K, [1 zeros(1,p-1)], diag(delta), [Vbeta(1); zeros(p-1,1)], diag( gamma ), Vbeta(2:p+1), zeros(1,p), 0);

if (isGammaExact)
    R1.WP = zeros(size(R1.WP));
end
if (isDeltaExact)
    R1.WM = zeros(size(R1.WM));
end

flag = 1;







function y=F2(x)
y=log2(x)-floor(log2(x));



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

