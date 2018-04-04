%Purpose:
% Compute the open-loop Roundoff Noise Gain
%
%Syntax:
% G = RNG(R)
% [G, dZ] = RNG(R,tol)
%
%Parameters:
% G: roundoff noise gain
% dZ: number of non-trivial parameters (used by @FWS/RNG)
% R: FWR object
% tol: tolerance on trivial parameters (default=1e-8);
%
%
% $Id: RNG.m 208 2009-01-05 13:52:19Z fengyu $


function [G, dZ] = RNG(R,tol)

if nargin==1
    tol=1e-8;
end

M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
M2 = [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ];

W01Z = computeWeight(R.Z,tol);

dZ = diag( W01Z*ones(R.l+R.n+R.m,1) );

G = trace( dZ * ( M2'*M2 + M1'*R.Wo*M1 ) );



% compute the weighting matrix for one matrix
function W = computeWeight(X,tol)

N=size(X);
W=ones(size(X));
i = find ((abs(X)<tol) | (abs(X-1)<tol) | (abs(X+1)<tol));
W(i)=0;

ind = find( abs(W)>tol );
k = size( ind,1 );
for j=1:k
	if ( rem(abs(log2(X(ind(j)))),1)<tol )
		W(ind(j))=0;
	end
end


%Description:
% 	This function computes the Roundoff Noise Gain (in open-loop context).\\
% 	The Roundoff Noise Gain is the output noise power computed in a specific computational scheme : the noises are supposed to
% 	appear only after each multiplication and are modeled by centered white noise statistically independent.\\ Each noise is
% 	supposed to have the same power $\sigma_0^2$ (determined by the wordlength chosen for all the variables and coefficients).\\
% 
% 	The Roundoff Noise Gain is defined by
% 	\begin{equation}
% 		G \triangleq \frac{P}{\sigma_0^2}
% 	\end{equation}
% 	where $P$ is the output roundoff noise power.
% 
% 	It could be computed by
% 	%\begin{eqnarray}
% 	%	G  &=& tr\pa{ \strut  \pa{ d_M + d_N + d_J } J^{-\top} \pa{L^\top L + K^\top W_o K} J^{-1} } \nonumber \\
% 	%			&& + tr\pa{ \strut \pa{ d_K + d_P + d_Q }W_o} +  tr\pa{  d_L + d_R + d_S }
% 	%\end{eqnarray}
% 	\begin{equation}
% 		G = tr\pa{ dZ (M_2^\top M_2 + M_1^\top W_o M_1)}
% 	\end{equation}
% 	with 
% 	\begin{align}
% 		M_1 &\triangleq  \begin{pmatrix} KJ^{-1} & I_n & 0 \end{pmatrix} \\
% 		M_2 &\triangleq  \begin{pmatrix} LJ^{-1} & 0 & I_{p_2} \end{pmatrix}
% 	\end{align}
% 	and the matrix $d_Z$ is a diagonal matrix defined by
% 	\begin{equation}
% 		\pa{d_Z}_{i,i} \triangleq \text{number of non-trivial parameters in the i\textsuperscript{th} row of $Z$}
% 	\end{equation}
% 	The trivial parameters considered are $0$, $1$, $-1$ and powers of $2$ because they do not imply a multiplication. 

%See also: <@FWR/RNG_cl>, <@FWS/RNG>

%References:
%	\cite{Hila07c} T.�Hilaire, D.�M�nard, and O.�Sentieys. Roundoff noise analysis of finite wordlength realizations with the implicit state-space framework. In 15th European Signal Processing Conference (EUSIPOC'07), September 2007.
