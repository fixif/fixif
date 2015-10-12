%Purpose:
% Create a diagonal matrix of twiddle factors (for FFT2FWR)
%
%Syntax:
% T = twiddleM(r,n)
%
%Parameters:
%T: twiddle factors matrix
%r,n: $n$ decomposition : $n=rs$
%
% $Id: twiddleM.m 199 2008-12-24 17:08:01Z fengyu $


function T = twiddleM(r,n)

if mod( n,r)~=0
	error('r must divide n')
end

i = 0:n-1;
k = floor(i/r);
l = i-k*r;

if n>16
	T =sparse([],[],[],n,n,n);
else
	T = zeros(n,n);
end

T(i*n+i+1) = exp( -j*2*pi/n*(k(i+1).*l(i+1)) );



%Description:
% 	Create a diagonal matrix of twiddle factors. This function is used
% 	by \funcName{FFT2FWR}.\\
%	This matrix $\mathscr{T}^n_s$ is defined by
%	\begin{equation}
%		\mathscr{T}^{rs}_{s} \triangleq \bigoplus_{j=0}^{r-1} \text{diag}\pa{ \omega_n^0, \hdots, \omega_n^{s-1} }^{-j} \\
%	\end{equation}

%See also: <FFT2FWR>