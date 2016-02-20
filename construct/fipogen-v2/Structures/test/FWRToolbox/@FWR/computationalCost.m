%Purpose:
% Give the number of additions and multiplications implied in the realization
%
%Syntax:
% [add, mul] = computationalCost( R, tol)
%
%Parameters:
% add: number of additions
% mul: number of multiplications
% R: FWR object
% tol: tolerance (default value = 1e-8)
%
%
% $Id: computationalCost.m 201 2009-01-03 22:31:50Z hilaire $


function [add, mul] = computationalCost(R, tol)

% args
if (nargin==1)
    tol = 1e-8;
end

% null (n0) and trivial (n1) elements of R
% (only coefficients such W=0 are considered)
n0 = length( find( R.WZ==0 & abs(R.Z)<tol ) );
n1 = length( find( R.WZ==0 & (abs(R.Z)<tol | abs(R.Z-1)<tol | abs(R.Z+1)<tol) ) );

% add & mul
add = (R.l+R.p+R.n)*(R.l+R.n+R.m-1) - R.l -n0;
mul = (R.l+R.p+R.n)*(R.l+R.n+R.m) - n1;


%Description:
% 	The number of additions and multiplications is based on the number of trivial parameters
%	and null parameters.\\
% 	The evaluation is based on the following proposition, applied on the three steps [i],
%	[ii] and [iii] of algorithm \eqref{eq:def_implicit} :
% 	\begin{proposition}
% 	Let $Y\in\Rbb{a}{b}$ be a constant, and $V\in\Rbb{b}{1}$ a variable.\\
% 	The calculus $YV$ needs $a(b-1)-n^0_Y$ additions and $ab-n^1_Y$ multiplications, where
%	$n^0_Y$ is the number of null elements of $Y$ and $n^1_Y$ is the number of trivial elements
%	($0$,$1$,$-1$) of $Y$ (these elements don't imply a multiplication)
%	\end{proposition}
% 	Then, the algorithm requires $(l+n+p)(l+m+n-1)-l-n^0_Z$ additions and $(l+n+p)(l+m+n)-n^1_Z$
%	multiplications.
	