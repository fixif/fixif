%Purpose:
% Compute the $Z$ and $W_Z$  of a FWR object from its parameters $J$, ..., $S$, $W_J$, ..., $W_S$.
%
%Syntax:
% R = updateZ(R)
%
%Parameters:
% R: FWR object
%
%
% $Id: computeZ.m 203 2009-01-04 14:03:56Z hilaire $


function R=computeZ(R)

R.Z = [ -R.J R.M R.N; R.K R.P R.Q; R.L R.R R.S];
R.WZ = [ R.WJ R.WM R.WN; R.WK R.WP R.WQ; R.WL R.WR R.WS];


%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function updates the matrices $Z$ and $W_Z$ from the matrices $J$, $K$, $L$, $M$, $N$, $P$, $Q$, $R$, $Q$, $W_J$, $W_K$, $W_L$, 
% 	$W_M$, $W_N$, $W_P$, $W_Q$, $W_R$ and $W_S$.\\
% 	It is called when a new value for one of these matrices is given.
%See also: <@FWR/computeJtoS>