%Purpose:
% Build Fast Fourier Transform (size $n$) with a FWR object
%
%Syntax: 
% R = FFT2FWR(n)
% R = FFT2FWR(n, toSimplify)
%
%Parameters:
% R: FWR object to represent the algorithm
% n: size of the FFT
% toSimplify: 1 (default) to make the simplification (level=1)
%			: 0 to avoid simplifications	
%
% $Id: FFT2FWR.m 199 2008-12-24 17:08:01Z fengyu $


function R = FFT2FWR(n, toSimplify)

% args
if nargin<2
	toSimplify=1;
end

[J,L,N,S] = complexFFT(n, toSimplify);

l=size(J,1);
Ll = strideM(l,2*l);
Ln = strideM(n,2*n);

JJ = Ll * [real(J), -imag(J) ; imag(J) real(J)] * Ll';
LL = Ln * [real(L), -imag(L) ; imag(L) real(L)] * Ll';
NN = Ll * [real(N); imag(N)];
SS = Ln * [real(S); imag(S)];

% build FWR
R = FWR( JJ, zeros(0,2*l), LL, zeros(2*l,0), NN, zeros(0,0), zeros(0,n), zeros(2*n,0), SS);

% simplify (level=1) if required
if toSimplify
	R = simplify(R);
end


%Description:
% 	The general factorization of DFT matrices are given by the Cooley-Tukey algorithm \cite{Cool65,Egne01}, also known as Fast Fourier Transform (FFT):
% 	\begin{equation}\label{eq:Cooley-Tukey}
% 		DFT_n = \pa{DFT_r \otimes I_s} \mathscr{T}^n_s \pa{ I_r \otimes DFT_s} \mathscr{L}^n_r%, \hspace{.5cm} \text{for\ } n=rs
% 	\end{equation}
% 	where 
% 	\begin{itemize}
% 		\item $n$ is factorized in $n=rs$,
% 		\item $\otimes$ denotes the Kronecker product of matrices defined by $A \otimes B \triangleq \pa{ A_{k,l} B}$,
% 		\item $\mathscr{T}^n_s$ is the twiddle matrix with
% 			\begin{equation}
% 				\mathscr{T}^{rs}_{s} \triangleq \bigoplus_{j=0}^{r-1} \text{diag}\pa{ \omega_n^0, \hdots, \omega_n^{s-1} }^{-j} \\
% 		\end{equation}
% 		\item $A \oplus B$ is the direct sum of $A$ and $B$: 
% 		\begin{equation}
% 			A \oplus B \triangleq \begin{pmatrix} A \\ & B \end{pmatrix}
% 			\end{equation}
% 		\item and $\mathscr{L}^n_r$ is the stride permutation matrix that maps the vector elements indices $j$ as:
% 			\begin{equation}
% 				\mathscr{L}^{rs}_{r} : j \mapsto \begin{cases}
% 					jr \mod rs-1 &\text{for\ } 0 \leq j \leq rs - 2 \\
% 					rs-1 & \text{for\ } j=rs-1
% 				\end{cases}
% 			\end{equation}
% 	\end{itemize}
% 	Equation \eqref{eq:Cooley-Tukey} depends on the factorization $n=rs$, and should be applied recursively until $n$ is a prime number.
% 
% 
% 	Since DFT is a linear transform, it is possible to express it with the SIF. Let us find the SIF realization $\mathcal{R}:=(J,K,L,M,N,P,Q,R,S)$ that realizes
% 	\begin{equation}
% 		Y(k)=DFT_n U(k)
% 	\end{equation}
% 	with $U(k)\in\Rbb{n}{1}$ and $Y(k)\in\Cbb{n}{1}$.\\
% 
% 	The following proposition allows to express such a realization by applying Cooley-Tukey factorization.
% 
% 	\begin{proposition}\label{prop:Cooley-Tukey}
% 	Let suppose that $\mathcal{R}_1:=(J_1,.,L_1,.,N_1,.,.,.,S_1)$ and $\mathcal{R}_2:=(J_2,.,L_2,.,N_2,.,.,.,S_2)$ respectively realize $\text{DFT}_r$ and $\text{DFT}_s$, \I{i.e.}:
% 	\begin{eqnarray}\label{eq:SIF-DFT_r}
% 		DFT_r: &&\left\{ \begin{array}{rcl}
% 			J_1 T_1 &=& N_1 U_1(k) \\
% 			Y_1(k) &=& L_1 T_1 + S_1U_1(k)
% 		\end{array}\right.\\ \label{eq:SIF-DFT_s}
% 		DFT_s: &&\left\{ \begin{array}{rcl}
% 			J_2 T_2 &=& N_2 U_2(k) \\
% 			Y_2(k) &=& L_2 T_2 + S_2U_2(k)
% 		\end{array}\right.
% 	\end{eqnarray}
% 	Remark that no states are needed and that $S_1$ (and $S_2$) are only required if $r=2$ ($s=2$).
% 
% 	$\mathcal{R}$ is given by $\mathcal{R}:=(J,,L,,N,,,,)$ with
% 	\begin{align}\label{eq:Cooley-Tukey-SIF1}
% 		J&=\begin{pmatrix}
% 			\pa{I_r \otimes J_2} & 0 & 0 & 0 \\
% 			-\pa{I_r \otimes L_2} & I_n & 0 & 0 \\
% 			0 & -\mathscr{T}_s^n & I_n & 0 \\
% 			0 & 0 & -\pa{N_1 \otimes I_s} & \pa{J_1 \otimes I_s} \\
% 		\end{pmatrix}\\
% 		L&=\begin{pmatrix}
% 			0 & 0 & -\pa{S_1 \otimes I_s} & -\pa{L_1 \otimes I_s}\\
% 		\end{pmatrix}\\
% 		N&=\begin{pmatrix}
% 			\pa{I_r \otimes N_2}\mathscr{L}_r^n \\
% 			 \pa{I_r \otimes S_2}\mathscr{L}_r^n \\
% 			 0 \\ 0
% 		\end{pmatrix} \label{eq:Cooley-Tukey-SIF2}
% 	\end{align}
% 
% 	\end{proposition}
% 	This proposition is realized with \funcName{complexFFT}, that returns a FFT realization with complex coefficients.
% 
% 	Considering that $DFT_2$ can be realized with $\mathcal{R}:=(,,,,,,,,\begin{pmatrix}1&1\\1&-1\end{pmatrix})$, the proposition \ref{prop:Cooley-Tukey} can be recursively applied to obtain the SIF of $DFT_{2^l}$ (for example, with $r=s=2^{\frac{l}{2}}$ if $l$ is even and with $r=2^{\frac{l-1}{2}}$ and $s=2$ to obtain $DFT_{2^\frac{l+1}{2}}$ and with $r=2^{\frac{l-1}{2}}$ and $s=2^{\frac{l=11}{2}}$ is $l$ is odd).
% 
% 
% 	Since the proposition \ref{prop:Cooley-Tukey} provides rules for $DFT_n$ realization with complex coefficients, a transformation is then required in order to obtain the DFT algorithm with real coefficients. The output will now represent the real and imaginary parts of the complex DFT outputs.
% 
% 	\begin{proposition}\label{prop:complex2real}
% 		Let suppose realization $\mathcal{R}':=(J',,L',,N',,,,S')$ realizes $DFT_n$ with complex coefficients ($J'\in\Cbb{l}{l}$, $L'\in\Cbb{n}{l}$, $N\in\Cbb{l}{n}$ and $S\in\Cbb{n}{n}$) and real inputs. Then the realization $\mathcal{R}:=(J,,L,,N,,,,S)$ with 
% 		\begin{align}
% 			J &= \mathscr{L}_l^{2l} \begin{pmatrix} \Re{J'} & -\Im{J'} \\ \Im{J'} & \Re{J'} \end{pmatrix} \tr{\mathscr{L}_{l}^{2l}} \label{eq:com2real-1}\\
% 			L &= \mathscr{L}_n^{2n} \begin{pmatrix} \Re{L'} & -\Im{L'} \\ \Im{L'} & \Re{L'} \end{pmatrix} \tr{\mathscr{L}_{l}^{2l}} \\
% 			N &= \mathscr{L}_l^{2l} \begin{pmatrix}  \Re{N'} & \Im{N'} \end{pmatrix} \\
% 			S &=\mathscr{L}_n^{2n} \begin{pmatrix}  \Re{S'} & \Im{S'} \end{pmatrix} \label{eq:com2real-4}
% 		\end{align}
% 		realize the $DFT_n$ with real coefficients and real outputs (the $2n$ outputs alternate real and imaginary parts of the $n$ complex outputs of $\mathcal{R}'$).\\
% 		%$J\in\Rbb{2l}{2l}$, $L\in\Rbb{2n}{2l}$, $N\in\Rbb{2l}{n}$, $S\in\Rbb{2n}{n}$ and 
% 		$\Re{.}$ and $\Im{.}$ denote respectively the real and imaginary parts.
% 	\end{proposition}

%Example:
%	The $FFT_4$ is given by the following realization (after simplification):
% 	$$Z=\begin{pmat}({...||...})              
% 		-1 & 0 & 0 & 0 & 1 & 0 & 1 & 0 \cr   
% 		0 & -1 & 0 & 0 & 1 & 0 & -1 & 0 \cr  
% 		0 & 0 & -1 & 0 & 0 & 1 & 0 & 1 \cr   
% 		0 & 0 & 0 & -1 & 0 & 1 & 0 & -1 \cr\-
% 		1 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \cr    
% 		0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \cr    
% 		0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \cr    
% 		0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 \cr   
% 		1 & 0 & -1 & 0 & 0 & 0 & 0 & 0 \cr   
% 		0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \cr    
% 		0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \cr    
% 		0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \cr    
% 	\end{pmat}$$ 

%See also: <@FWR/simplify>, <complexFFT>, <strideM>, <twiddleM>

%References: