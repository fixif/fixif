%Purpose:
% Simplify (if possible) a FWR, by removing the non-necessary intermediate variables and states
%
%Syntax:
% Rs = simplify( R, level, tol)
%
%Parameters:
% Rs: simplified FWR object
% R: FWR to be simplified
% level	: level of simplification
%			: 0 : simplify only null terms
%			: 1(default) : simplify lines with only one term (substitution)
%           : 2 : simplify lines with 2 terms, etc...
%			: level $>1$ may increase the complexity
% tol: tolerance (default=1e-14)
%
% $Id: simplify.m 208 2009-01-05 13:52:19Z fengyu $


function R = simplify( R, level, tol)

% args
if nargin<3
	tol=1e-14;
	if nargin<2
		level=1;
	end
end

% simplify null terms
R.Z(find(abs(R.Z)<tol))= 0;

% find states/intermediate variables to simplify
Zbis = R.Z;
Zbis(1:R.l,1:R.l) = Zbis(1:R.l,1:R.l)+eye(R.l);
if issparse(Zbis)
	Row = sum(spones(Zbis)' )';
else
	ZbisUnit=Zbis;
	ZbisUnit( find(Zbis) ) = 1;
	Row = sum(ZbisUnit')';
end


%======================================================
% loop to simplify null states or intermediate variables
nbo=1;
ind = find(Row==0)';
changed=0;
while ~isempty( ind(nbo:end) )

	i=ind(nbo);
		
	if i<=R.l+R.n
		% remove a state or intermediate variable
		R.Z(i,:)=[];
		R.Z(:,i)=[];
		% update l and n
		if i<=R.l
			R.l=R.l-1;
		else
			R.n=R.n-1;
			warning('1 state removed. Please check!');
		end
		changed=1;

	else
		% null output
		warning([ 'output y[' num2str(i-R.l-R.n-1) '] is detected to be null']);
		nbo=nbo+1;
	end
	
	% find new states/intermediate variables to simplify
	Zbis = R.Z;
	Zbis(1:R.l,1:R.l) = Zbis(1:R.l,1:R.l)+eye(R.l);
	if issparse(Zbis)
		Row = sum( spones(Zbis)' )';
	else
		ZbisUnit=Zbis;
		ZbisUnit( find(Zbis) ) = 1;
		Row = sum(ZbisUnit')';
	end
	ind = find(Row==0)';
end


%=================================================================
% loop to simplify row without any computations (only level terms)
ind = find(Row<=level)';
warn=0;
while ~isempty( ind )

	i=ind(1);
	j=find(Zbis(i,:));			 % we have T(i) = coef1 * T(j1) + coef2 * T(j2)

	l = find( Zbis(:,i)~=0 );	% where T(i) is used
	% l different de i ??
	k = find( Zbis(l,j) );		% where T(i) and T(j) are used in the same operation
	if isempty(k) & ( all(abs(Zbis(i,j)))==1 | all(abs(Zbis(l,i))==1) )

		if length(j)>=2 & length(l)>=2
			warn=1;
		end

		if i<=R.l+R.n
			% substitutions
			for indl=l'
				for indj=j
					negli = -2*((indl<=R.l) & (i<=R.l))+1;		% sign correction if (l,i) is a coefficient of J
					negij = -2*((i<=R.l) & (indj<=R.l))+1;
					neglj = -2*((indl<=R.l) & (indj<=R.l))+1;
					R.Z(indl,indj) = - negli*R.Z(indl,i) * negij.*R.Z(i,indj) * neglj;
					%R.Z(indl,indj) = R.Z(indl,i) * R.Z(i,indj);

				end
			end
			% remove a state or intermediate variable
			R.Z(i,:)=[];
			R.Z(:,i)=[];
			% update l and n
			if i<=R.l
				R.l=R.l-1;
			else
				R.n=R.n-1;
			end
			changed=1;
		else
			break
		end
	end


	% find new states/intermediate variables to simplify
	Zbis = R.Z;
	Zbis(1:R.l,1:R.l) = Zbis(1:R.l,1:R.l)+eye(R.l);
	if issparse(Zbis)
		Row = sum( spones(Zbis)' )';
	else
		ZbisUnit=Zbis;
		ZbisUnit( find(Zbis) ) = 1;
		Row = sum(ZbisUnit')';
	end
	ind = find(Row<=level)';
end



% warning
if warn==1
	warning('The complexity has been increased');
end

% changed?
if changed==0
	warning('The realization is unchanged');
end


% build simplified FWR
R = computeJtoS( R);
R = FWR( R.J, R.K, R.L, R.M, R.N, R.P, R.Q, R.R, R.S);


%Description:
% 	Due to the sparsity of some realizations (for example, the FFT ones created by \funcName{FFT2FWR}), 
% 	some simplifications in the realization can be provided. Null intermediate variables can appear and must be propagated,
% 	and intermediate variables that are sometimes set equal to an other value (without any other computations) must be removed.
% 
% 	Let consider a realization $\mathcal{R}:=(Z,l,m,n,p)$. Computing $T(k+1)$, $X(k+1)$ and $Y(k)$ for each step according 
% 	to the associated algorithm is equivalent to compute
% 	\begin{equation}
% 		Z' .\begin{pmatrix} T(k+1)\\ X(k)\\ U(k)\end{pmatrix} \text{\ with\ } Z' \triangleq Z + \begin{pmatrix}I_l \\ &0 \end{pmatrix}
% 	\end{equation}
% 
% 	This function simplifies (if possible) the realization by applying two transformations.\\
% 	The first transform removes the intermediate variables that are null (they could appear for the FFT realization,
% 	because of the real or imaginary parts that are null). It can be
% 	described by the following algorithm:\\
% 
% 	\begin{algorithm}[H]
% 		\caption{\label{algo:null_values}Remove the null values}
% 		\SetLine
% 		%\While{ $\exists i\leq l+n$ such as $Z'_{i,j}=0 \ \forall 1 \leq j \leq l+n+m$}
% 		\While{ it exists $i\leq l+n$ such as $Z'_{i,\bullet}$ is a null vector }
% 		{
% 			\tcp{\I{Remove $i$-th intermediate variable or state}}		
% 			remove $i$-th row and $i$-th column of $Z'$\;
% 			decrease $l$ or $n$\;
% 		}
% 	\end{algorithm}
% 
% 	In some cases, various intermediate variables are only equal  to another intermediate variable.\\ For example, 
% 	if $T_2 \leftarrow aT_1$ and $T_3 \leftarrow bT_2$, when it is possible to substitute $T_3$ to $T_2$ if $a$ or
% 	$b$ $\in\{-1,1\}$ (in order to preserve the parametrization).\\
% 	The algorithm \ref{algo:substitution} allows the substitution of an intermediate variable by an other one.\\
% 
% 	\begin{algorithm}[H]
% 		\caption{\label{algo:substitution}Substitute the intermediate variables}
% 		\SetLine
% 		%\While{ $\exists i\leq l$ such as $\exists!j$ such as $Z'_{i,k}=\delta_{j,k}Z'_{i,j} \forall 1 \leq k \leq l+n+m$}
% 		\While{ it exists $i \leq l$ such as $Z'_{i,\bullet}$ has only one non-null element $Z'_{i,j}$}
% 		{
% 			\tcp{\I{then we have something like $T_i\leftarrow aT_j$}}
% 			%\If{$\forall l \neq i$, $Z'_{l,i}\neq0 \Rightarrow \pa{Z'_{l,j}=0 \text{\ and\ } \pa{ Z'_{i,j}=\pm1 \text{\ or\ } Z'_{l,i}=\pm1 } }$}
% 			\If{ for all $k \neq i$, $Z'_{k,i}\neq0$ implies $\pa{Z'_{k,j}=0 \text{\ and\ } \pa{ Z'_{i,j}=\pm1 \text{\ or\ } Z'_{k,i}=\pm1 } }$}
% 			{
% 				\tcp{\I{Substitution}}
% 				\For{$1\leq k \leq l+n+p$ such as $Z'_{k,i}\neq0$}
% 				{
% 					$Z'_{k,j} \leftarrow \varepsilon Z'_{k,i}. Z'_{i,j}$\\
% 					with $\varepsilon = \text{sign}(k,i).\text{sign}(i,j).\text{sign}(k,j)$\\
% 					and $\text{sign}(p,q)=\begin{cases}-1 & \text{if\ } p \leq l \text{\ and\ } q \leq l \\ 1 & \text{otherwise}\end{cases}$ 
% 				}
% 				\tcp{\I{Remove $i$-th intermediate variable}}		
% 				remove $i$-th row and $i$-th column of $Z'$\;
% 				decrease $l$\;
% 			}
% 		}
% 	\end{algorithm}
% 		The term $\varepsilon$ in that algorithm is introduced to taking in consideration the $-J$ in the definition of $Z$
% 		(eq. \eqref{eq:def_Z})(this $-J$ was introduced in \cite{Hila07b} in order to simplify the sensitivities and 
% 		roundoff measure).
% 	\begin{remark}
% 		It is also possible to consider the substitution when $T_i$ is composed various terms. For example, $T_3 
% 		\leftarrow aT_1 + bT_2$ and $T_4 \leftarrow cT_3$ become $T_4 \leftarrow acT_1+bcT_2$ if $c=\pm1$ or 
% 		$(a=\pm1 \text{\ and\ }b=\pm1)$. In that case, this transformation can increase the complexity of the computations
% 		(since an intermediate variable that is substituted is used twice or more).
% 	\end{remark}
% 	The input \matlab{level} can set the level of the substitution. \matlab{0} means that only the null terms are removed, and \matlab{1}
% 	only the terms like $T_2 \leftarrow T_3$ are removed. With a greater value, the function considers the substitution if an
% 	intermediate variable is composed from various terms, and \matlab{level} gives the maximum number of terms.

%Example:
% 	The $FFT_4$ transform first corresponds to the following algorithm (see \funcName{FFT2FWR})
% 	\begin{algorithm}[h]
% 		\caption{$FFT_4$ without any simplification\label{algo:FFT4_1}}
% 		\KwIn{$u$: array [1..4] of reals}
% 		\KwOut{$y$: array [1..8] of reals}
% 		\KwData{$T$: array [1..16] of reals}
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$T_{ 1} \leftarrow u(1)   + u(3)  $\;
% 		$T_{ 2} \leftarrow 0$\;
% 		$T_{ 3} \leftarrow u(1)   + -u(3)  $\;
% 		$T_{ 4} \leftarrow 0$\;
% 		$T_{ 5} \leftarrow u(2)   + u(4)  $\;
% 		$T_{ 6} \leftarrow 0$\;
% 		$T_{ 7} \leftarrow u(2)   + -u(4)  $\;
% 		$T_{ 8} \leftarrow 0$\;
% 		$T_{ 9} \leftarrow T_{ 1}$\;
% 		$T_{10} \leftarrow T_{ 2}$\;
% 		$T_{11} \leftarrow T_{ 3}$\;
% 		$T_{12} \leftarrow T_{ 4}$\;
% 		$T_{13} \leftarrow T_{ 5}$\;
% 		$T_{14} \leftarrow T_{ 6}$\;
% 		$T_{15} \leftarrow T_{ 8}$\;
% 		$T_{16} \leftarrow -T_{ 7}$\;
% 		\tcp{\emph{Outputs}}
% 		$y(1)   \leftarrow T_{ 9} + T_{13}$\;
% 		$y(2)   \leftarrow T_{10} + T_{14}$\;
% 		$y(3)   \leftarrow T_{11} + T_{15}$\;
% 		$y(4)   \leftarrow T_{12} + T_{16}$\;
% 		$y(5)   \leftarrow T_{ 9} + -T_{13}$\;
% 		$y(6)   \leftarrow T_{10} + -T_{14}$\;
% 		$y(7)   \leftarrow T_{11} + -T_{15}$\;
% 		$y(8)   \leftarrow T_{12} + -T_{16}$\;
% 	}
% 	\end{algorithm}
% 
% 	When only the null terms are removed (with \matlab{level}=0), the algorithm becomes:
% 
% 	\begin{algorithm}[h]
% 		\caption{$FFT_4$ with null terms removed\label{algo:FFT4_2}}
% 		\KwIn{$u$: array [1..4] of reals}
% 		\KwOut{$y$: array [1..8] of reals}
% 		\KwData{$T$: array [1..8] of reals}
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$T_{1} \leftarrow u(1)  + u(3) $\;
% 		$T_{2} \leftarrow u(1)  + -u(3) $\;
% 		$T_{3} \leftarrow u(2)  + u(4) $\;
% 		$T_{4} \leftarrow u(2)  + -u(4) $\;
% 		$T_{5} \leftarrow T_{1}$\;
% 		$T_{6} \leftarrow T_{2}$\;
% 		$T_{7} \leftarrow T_{3}$\;
% 		$T_{8} \leftarrow -T_{4}$\;
% 		\tcp{\emph{Outputs}}
% 		$y(1)  \leftarrow T_{5} + T_{7}$\;
% 		$y(2)  \leftarrow 0$\;
% 		$y(3)  \leftarrow T_{6}$\;
% 		$y(4)  \leftarrow T_{8}$\;
% 		$y(5)  \leftarrow T_{5} + -T_{7}$\;
% 		$y(6)  \leftarrow 0$\;
% 		$y(7)  \leftarrow T_{6}$\;
% 		$y(8)  \leftarrow -T_{8}$\;
% 	}
% 	\end{algorithm}
% 
% 	Then, with a complete substitution (\matlab{level}=1), the final algorithm is: 
% 
% 
% 	\begin{algorithm}[h]
% 		\caption{$FFT_4$ with substitutions (1 term)\label{algo:FFT4_3}}
% 		\KwIn{$u$: array [1..4] of reals}
% 		\KwOut{$y$: array [1..8] of reals}
% 		\KwData{$T$: array [1..5] of reals}
% 
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$T_{1} \leftarrow u(1)  + u(3) $\;
% 		$T_{2} \leftarrow u(1)  + -u(3) $\;
% 		$T_{3} \leftarrow u(2)  + u(4) $\;
% 		$T_{4} \leftarrow u(2)  + -u(4) $\;
% 		\tcp{\emph{Outputs}}
% 		$y(1)  \leftarrow T_{1} + T_{3}$\;
% 		$y(2)  \leftarrow 0$\;
% 		$y(3)  \leftarrow T_{2}$\;
% 		$y(4)  \leftarrow -T_{4}$\;
% 		$y(5)  \leftarrow T_{1} + -T_{3}$\;
% 		$y(6)  \leftarrow 0$\;
% 		$y(7)  \leftarrow T_{2}$\;
% 		$y(8)  \leftarrow T_{4}$\;
% 
% 	}
% 	\end{algorithm}




%See also: <FFT2FWR>
