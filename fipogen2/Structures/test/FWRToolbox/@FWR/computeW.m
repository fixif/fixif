%Purpose:
% Compute (or update) the weighting matrices ($W_J$ to $W_S$, and $W_Z$) of a FWR object
%
%Syntax:
% R = computeW(R,tol)
%
%Parameters:
% R: FWR object
% tol: tolerance (default=1e-8) (maximal distance to 0, -1 or +1)
%
% $Id: computeW.m 29 2007-03-07 15:14:18Z hilaire $


function R=computeW(R, tol)

% compute WX
if (nargin<2)
    tol=1e-8;
end
R.WJ = computeWeight(R.J,tol);
R.WK = computeWeight(R.K,tol);
R.WL = computeWeight(R.L,tol);
R.WM = computeWeight(R.M,tol);
R.WN = computeWeight(R.N,tol);
R.WP = computeWeight(R.P,tol);
R.WQ = computeWeight(R.Q,tol);
R.WR = computeWeight(R.R,tol);
R.WS = computeWeight(R.S,tol);

% compute WZ
R=computeZ(R);
R=compute_rZ(R);

return


% compute the weighting matrix for one matrix
function W = computeWeight(X,tol)

N=size(X);
W=ones(size(X));
i = find( (abs(X-1)<tol) | (abs(X)<tol) | (abs(X+1)<tol) );
W(i)=0;

return


%Description:
% 	For $X$ in $\{J,K,L,M,N,P,Q,R,S\}$ and $X=Z$, the weighting matrices
% 	$W_J$, $W_K$, $W_L$, $W_M$, $W_N$, $W_P$, $W_Q$, $W_R$, $W_S$ and $W_Z$ are computed according to
% 	\begin{equation}
% 		(W_X)_{ij} = \left\{
% 			\begin{array}{ll}
% 			0 & \text{if } \abs{X_{ij}}<\epsilon \text{ or } \abs{X_{ij}+1}<\epsilon \text{ or } \abs{X_{ij}-1}<\epsilon \\
% 			1 & \text{else}
% 			\end{array}\right.
% 	\end{equation}
% 	Where $\epsilon$ is the tolerance ($1e-8$ as default value). Here,
% 	the proximity to $0$ and $\pm1$ are considered (the other power of 2 are not considered).

