%Purpose:
% Create a stride permutation matrix (for FFT2FWR)
%
%Syntax:
% L = strideM(r,n)
%
%Parameters:
% L: stride permutation matrix
% r,n: parameters
%
%
% $Id: strideM.m 197 2008-12-23 15:16:19Z hilaire $

function L = strideM(r,n)

if mod( n,r)~=0
	error('r must divide n')
end

if n>16
	L = sparse([],[],[],n,n,n);
else
	L = zeros(n);
end

L(n,n) = 1;
j = 0:n-2;
i = mod( j*r, n-1);
L(i*n+j+1) = 1;


%Description:
% 	Create a stride permutation matrix. This function is used by \funcName{FFT2FWR}.\\
% 	This matrix $\mathscr{L}^n_r$ is the stride permutation matrix that maps the vector elements indices $j$ as:
% 	\begin{equation}
% 		\mathscr{L}^{rs}_{r} : j \mapsto \begin{cases}
% 			jr \mod rs-1 &\text{for\ } 0 \leq j \leq rs - 2 \\
% 			rs-1 & \text{for\ } j=rs-1
% 		\end{cases}
% 	\end{equation}

%See also: <FFT2FWR>