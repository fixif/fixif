%Purpose:
% Perform a relaxed-$L_2$-scaling on the FWR.
% The wordlength are deduced from the FPIS if it is defined.
%
%Syntax:
% R = lrelaxedl2scaling(R,Umax,delta)
% [U,Y,W] = relaxedl2scaling(R,Umax,delta)
%
%Parameters:
% R: FWR object
% U,Y,W: transformation matrices applied on R
% Umax: input maximum magnitude (default: Umax = a power of 2)
% delta: security parameter (default: delta=1)
%
% $Id: relaxedl2scaling.m 257 2012-03-12 19:37:49Z hilaire $


function [R,Y,W] = relaxedl2scaling(R,Umax,delta)

% args
if nargin<2
	if isempty(R.FPIS)
		Umax=1;	% any power of 2
	else
		Umax=R.FPIS.Umax;
	end
end
if nargin<3
	delta=1;
end

% SISO test
if (R.m~=1) | (R.p~=1)
	error('the system must be SISO!');
end

% alpha
if isempty(R.FPIS)
	alphaX = - ( log2(Umax) - floor(log2(Umax)) )*ones(R.n,1);
	alphaT = - ( log2(Umax) - floor(log2(Umax)) )*ones(R.l,1);
else
	alphaX = R.FPIS.betaX - ( R.FPIS.betaU + log2(Umax) - floor(log2(Umax)) )*ones(R.n,1);
	alphaT = R.FPIS.betaT - ( R.FPIS.betaU + log2(Umax) - floor(log2(Umax)) )*ones(R.l,1); 
end

% U,Y,W transformation matrices
U = toto( R.Wc, alphaX, delta );
W = toto( inv(R.J)*(R.N*R.N' + R.M*R.Wc*R.M')*inv(R.J)' , alphaT, delta);
%Y = eye(R.l);
Y= inv(W);

% ind where U or W is null
indU=find(diag( R.Wc )==0);
if ~isempty(indU)
	for i=indU
		U(i,i) = toto( norm(ss(R))/sqrt(R.Wo(i,i)), alphaX(i), delta);
	end
end
indW=find(diag( inv(R.J)*(R.N*R.N' + R.M*R.Wc*R.M')*inv(R.J)' )==0);
if ~isempty(indW)
	for i=indW
		Woii=inv(R.J)'*(R.L'*R.L + R.K'*R.Wo*R.K)*inv(R.J);
		W(i,i) = toto( norm(ss(R))/sqrt( Woii ), alphaT(i), delta);
	end
end


% if new realization needed
if nargout==1
	R = transform(R, U,Y,W);
else
	R = U;
end


% complicated formula... :-)
function V = toto (M, alpha, delta)

if ~isempty(alpha)
	d = delta*sqrt(diag(M));
	if isintval(d)==1
		V = diag(d) .* diag( 2.^-( log2(d) - floor(log2(mid(d))) + alpha ) );
		disp(V)
	else
	
		V = diag(d) .* diag( 2.^-( log2(d) - floor(log2(d)) + alpha ) );
	end
else
	V=[];
end


%Description:
% 	Perform a relaxed-$L_2$-scaling.\\
% 	The scaling forces the transfer functions from the inputs to the states and the intermediates variables to have a $L_2$-norm between 1 and 4. Theses norms are given by the diagonal terms of $W_c$ and $J^{-1}\pa{NN^\top+MW_cM^\top}J^{-\top}$.\\
% 
% 	Denote $W_{cX}$ the controllability gramian of the realization ($W_c$) and $W_{cT}$ the controllability gramian related to the intermediate variables. It is given by
% 	\begin{equation}
% 		W_{cX} = \sqrt{\pa{J^{-1}\pa{NN^\top+M W_{cX} M^\top}J^{-\top}}}
% 	\end{equation}
% 
% 	The relaxed-$L_2$-scaling is a transformation that make the realization satisfy the constraints ($\forall 1 \leq i \leq n$)
% 
% 	\begin{eqnarray}
% 		\frac{2^{2{\alpha_X}_i}}{\delta^2} \leq &\pa{W_{cX}}_{i,i}& < 4 \frac{2^{2{\alpha_X}_i}}{\delta^2} \\
% 		\frac{2^{2{\alpha_T}_i}}{\delta^2} \leq &\pa{W_{cT}}_{i,i}& < 4 \frac{2^{2{\alpha_T}_i}}{\delta^2}	
% 	\end{eqnarray}
% 	where
% 	\begin{eqnarray}
% 		{\alpha_X}_i &\triangleq& \beta_{X_i}-\beta_U-\mathscr{F}_2\pa{\overset{\max}{U}} \\
% 		{\alpha_T}_i &\triangleq& \beta_{T_i}-\beta_U-\mathscr{F}_2\pa{\overset{\max}{U}}
% 	\end{eqnarray}
% 	and $\mathscr{F}_2(x)$ is defined as the fractional value of $\log_2(x)$: 
% 	\begin{equation}
% 		\mathscr{F}_2(x)\triangleq \log_2(x) - \left\lfloor \log_2(x) \right\rfloor
% 	\end{equation}
% 	If the wordlength $\beta_X$ and $\beta_T$ are not defined by the FPIS, they are also supposed to be equal. Moreover, if $\delta=1$ (default case) and $\overset{\max}{U}$ is
% 	a power of $2$, then the realization satisfies the following constraints
% 	\begin{equation}
% 		1 \leq (W_{cX})_{ii} < 4, \hspace{1cm} 1 \leq (W_{cT})_{ii} < 4, \hspace{1cm} \forall 1\leq i \leq n
% 	\end{equation}
% 
% 	The $L_2$-scaling is achieved by a $\mt{U}\mt{Y}\mt{W}$-transformation where $\mt{U}$ and $\mt{W}$ are diagonal with:
% 	\begin{eqnarray}
% 		\pa{\mt{U}}_{ii} &=& \delta \sqrt{\pa{W_{cX}}_{i,i}} 2^{-\mathscr{F}_2(\delta\sqrt{\pa{W_{cX}}_{i,i}})-{\alpha_X}_i} \\
% 		\pa{\mt{W}}_{ii} &=& \delta \sqrt{\pa{W_{cT}}_{i,i}} 2^{-\mathscr{F}_2(\delta\sqrt{\pa{W_{cT}}_{i,i}})-{\alpha_T}_i}
% 	\end{eqnarray}

%See also: <@FWR/l2scaling>

%References:
%	\cite{Feng09a} Y. Feng, P. Chevrel, and T. Hilaire. A practical strategy of an efficient and sparse fwl implementation of lti filters. In submitted to ECC?09, 2009.\\
%	\cite{Hila09a}	T. Hilaire. Low parametric sensitivity realizations with relaxed l2-dynamic-range-scaling constraints. submitted to IEEE Trans. on Circuits \& Systems II, 2009.
