%Purpose:
% Compute the $J$, $K$, $L$, $M$, $N$, $P$, $Q$, $R$, $S$, $W_J$, ..., $W_J$,  of a FWR object
% from the $Z$ and $W_Z$ matrices of this object
%
%Syntax:
% R=computeJtoS(R)
%
%Parameters:
% R: FWR object
%
%
% $Id: computeJtoS.m 203 2009-01-04 14:03:56Z hilaire $


function R = computeJtoS( R)

% J, K, L, M, N, P, Q, R, S
R.J = -R.Z(1:R.l,1:R.l);
R.K = R.Z(R.l+1:R.l+R.n,1:R.l);
R.L = R.Z(R.l+R.n+1:R.l+R.n+R.p,1:R.l);
R.M = R.Z(1:R.l,R.l+1:R.l+R.n);
R.N = R.Z(1:R.l,R.l+R.n+1:R.l+R.n+R.m);
R.P = R.Z(R.l+1:R.l+R.n,R.l+1:R.l+R.n);
R.Q = R.Z(R.l+1:R.l+R.n,R.l+R.n+1:R.l+R.n+R.m);
R.R = R.Z(R.l+R.n+1:R.l+R.n+R.p,R.l+1:R.l+R.n);
R.S = R.Z(R.l+R.n+1:R.l+R.n+R.p,R.l+R.n+1:R.l+R.n+R.m);


%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function updates the matrices $J$, $K$, $L$, $M$, $N$, $P$, $Q$, $R$, $Q$, $W_J$, $W_K$, $W_L$, 
% 	$W_M$, $W_N$, $W_P$, $W_Q$, $W_R$ and $W_S$ from the matrices $Z$ and $W_Z$.\\
% 	It is called when a new value for $Z$ or $W_Z$ is given.

%See also: <@FWR/computeZ>