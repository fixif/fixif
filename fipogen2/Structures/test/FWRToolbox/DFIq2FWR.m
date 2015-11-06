 %Purpose:
% Transform a transfer function ('tf' object) into a FWR object with the Direct Form I scheme
%
%Syntax:
% R = DFIq2FWR( H )
%
%Parameters:
% R: FWR object
% H: tf object
%
%% $Id: DFIq2FWR.m 258 2012-04-18 20:47:13Z hilaire $


function R = DFIq2FWR( numq,denq )

if nargin==1
	% dimensions
	H = numq;
	numq = H.num{1};
	denq = H.den{1};
end
nnum = length(numq) - 1;
nden = length(denq) - 1;
	

% Gammas
Gamma1 = [ numq(2:nnum+1) -denq(2:nden+1) ];
Gamma2 = [ diag(ones([1 nnum-1]),-1) zeros([nnum nden]); zeros([nden nnum]) diag(ones([1 nden-1]),-1)];
Gamma3 = [ 1; zeros([nnum+nden-1 1]) ];
Gamma4 = [ zeros(nnum,1); 1; zeros(nden-1,1) ];

% transformation to 'optimize' the code
T=rot90(eye(2*nnum));

% build FWR object
%R = FWR( denq(1), Gamma4, 1, Gamma1, numq(1), Gamma2, Gamma3, [ zeros([1 nnum+nden]) ], 0);
R = FWR( denq(1), inv(T)*Gamma4, 1, Gamma1*T, numq(1), inv(T)*Gamma2*T, inv(T)*Gamma3, zeros([1 nnum+nden]), 0);


%Description:
% The system considered is described by the transfer function
% \begin{equation}
% 	H(z) = \frac{ \sum\limits_{i=0}^n b_{i} z^{-i} }{ \sum\limits_{i=0}^n a_{i}z^{-i} }
% \end{equation}
% and implemented with the recurrent equation
% \begin{equation}
% 	Y(k) = \frac{1}{a_{0}} \pa{ \sum_{i=0}^n b_{i}U(k-i) - \sum_{i=1}^n a_{i}Y(k-i) } \hspace{1cm} \forall k>n
% \end{equation}
% This could be described by the figure \ref{fig:DFIq}.\\
% \fig[scale=0.3]{DFIq}{Direct Form I with $q$-operator}
% 
% 
% The (finite precision) equivalent system, in the implicit state-space formalism, is given by
% \begin{equation}
% 	\begin{pmatrix}
% 		a_0 & 0 & 0\\
% 		-\Gamma_4 & I_{n} & 0\\
% 		-1 & 0 & 1
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k+1)\\
% 		X(k+1)\\
% 		Y(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmatrix}
% 		0 & \Gamma_1 & b_0\\
% 		0 & \Gamma_2 & \Gamma_3\\
% 		0 & 0 & 0\\
% 	\end{pmatrix}
% 	\begin{pmatrix}
% 		T(k)\\
% 		X(k)\\
% 		U(k)
% 	\end{pmatrix}
% \end{equation}
% where
% \begin{eqnarray}
% 	\Gamma_1 &=& 
% 		\left(\begin{array}{cccc|cccc}
% 			b_1&\cdots&\cdots&b_n&-a_1&\cdots&\cdots&-a_n
% 		\end{array}\right) \\
% 	\Gamma_2 &=& 		
% 		\left(\begin{array}{cccc|cccc}
% 			0 &&&\\
% 			1 & \ddots &&\\
% 			& \ddots & \ddots &\\
% 			&& 1 & 0 \\
% 			\hline &&&& 0 \\
% 			&&&& 1 & \ddots \\
% 			&&&& & \ddots & \ddots \\
% 			&&&& & & 1 & 0
% 		\end{array}\right)\\
% 	\Gamma_3 &=& 
% 		\left(\begin{array}{cccc|cccc}
% 			1 & 0 & \hdots & 0 & 0 & \hdots & \hdots & 0
% 		\end{array}\right)^\top  \\
% 	\Gamma_4 &=& 
% 		\left(\begin{array}{cccc|cccc}
% 			0 & \hdots & \hdots & 0 & 1 & 0 & \hdots & 0
% 		\end{array}\right)^\top
% \end{eqnarray}
%


