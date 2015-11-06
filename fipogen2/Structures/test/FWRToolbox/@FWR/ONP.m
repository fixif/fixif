%Purpose:
% Compute the Output Noise Power for a FWR object with Roundoff Before
% Multiplication (RBM) computational scheme
%
%Syntax:
% M = ONP( R, roundingMode)
%
%Parameters:
% M: output noise power measure
% R: FWR object
% mode: indicates the truncation mode: "truncation" (default) or "nearest"
%
% $Id$


function M = ONP( R, roundingMode, mXi, pXi)

if nargin<4

    % args
    if nargin==1
        roundingMode=1;
    elseif roundingMode=='nearest'
        roundingMode=0;
    else
        roundingMode=1;
    end

    % realization with FPIS
    if isempty(R.FPIS)
        error('the realization must have a FPIS defined');
    end

    % only on RBM scheme
    if R.FPIS.method~=1
        error('FPIS.method must be RBM (Roundoff Before Multiplication)');
    end

    % psi_xi and mu_xi
    gammabar = [ R.FPIS.gammaT; R.FPIS.gammaX; R.FPIS.gammaY ];

    if roundingMode==1
        mXi = .5*2.^-gammabar;
    else
        mXi = .5*2.^(-gammabar-R.FPIS.shiftADD);
    end
    mXi = mXi .* (R.FPIS.shiftADD>0);

    pXi = diag( 2.^(-2*gammabar).*(ones(size(gammabar))-2.^-R.FPIS.shiftADD)/12 .* (R.FPIS.shiftADD>0) );

end

% output noise power
M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
M2 = [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ];
Te=1;
Hxi = ss(R.AZ,M1,R.CZ,M2,Te);
H0mXi = dcgain(Hxi) * mXi;

M = trace( pXi * ( M2'*M2 + M1'*R.Wo*M1 ) ) + H0mXi' * H0mXi;



%Description:
% 	This function computes the Output Noise Power.\\
% 	Let us consider a realization $\mathcal{R}$ described with the implicit form�\eqref{eq:def_implicit}, with transfer function $H$.
% 	When implemented, the steps (i) to (iii) are modified by the add of noises $\xi_T(k)$, $\xi_X(k)$ and $\xi_Y(k)$:
% 	\begin{equation}\label{eq:ONP:implemented_sys}
% 		\begin{array}{r>{\hspace{-3mm}}c<{\hspace{-3mm}}l}
% 			J.T(k+1)  &\leftarrow&  M.X(k) + N.U(k) + \xi_T(k) \\
% 			X(k+1)  &\leftarrow&  K.T(k+1) + P.X(k) + Q.U(k) + \xi_X(k) \\
% 			Y(k)  &\leftarrow&  L.T(k+1) + R.X(k) + S.U(k) + \xi_Y(k)
% 		\end{array}
% 	\end{equation}
% 	%(the noise $J^{-1}\xi_T(k)$ is added on $T(k+1)$).\\
% 	These noises added depend on:
% 	\begin{itemize}
% 		\item the way the computations are organized (the order of the sums) and done,
% 		\item the fixed-point representation of the inputs, the outputs,
% 		\item and the fixed-point representation chosen for the states, the intermediate variables and the coefficients.
% 	\end{itemize}
% 	%They are determined by their first ($\mu$) and second ($\Psi$, $\sigma$) order moments.
% 	They are modeled as independent white noise, characterized by their first and second order moments.
% 	Denote $\xi$ the vector with all the added noise sources:
% 	\begin{equation}
% 		\xi(k) \triangleq \begin{pmatrix} \xi_T(k) \\ \xi_X(k) \\ \xi_Y(k) \end{pmatrix}
% 	\end{equation}	
% 
% 
% 	\begin{proposition}
% 	It is then possible to express the implemented system as the initial system with a noise $\xi'(k)$ added on the output(s) (see figure \ref{fig:equivalent_system}).
% 	\fig[scale=0.4]{equivalent_system}{Equivalent system, with noises extracted}\\
% 	$\xi'(k)$ is the noise $\xi(k)$ through the transfer function $H_\xi$ defined by:
% 	\begin{equation}
% 		H_\xi : z \to C_Z \pa{ zI_{n}-A_Z}^{-1} M_1 + M_2
% 	\end{equation}
% 	with
% 	\begin{eqnarray}
% 		M_1 &\triangleq  \begin{pmatrix} KJ^{-1} & I_n & 0 \end{pmatrix} \\
% 		M_2 &\triangleq  \begin{pmatrix} LJ^{-1} & 0 & I_{p_2} \end{pmatrix}
% 	\end{eqnarray}
% 	\end{proposition}
% 
% 
% 
% 
% 
% 
% 
% 	The Output Noise Power is defined as the power of the noises added on the output
% 	\begin{equation}
% 		P \triangleq E{ \xi'(k)\xi'(k)^\top }
% 	\end{equation}
% 	where the $E{.}$ is the mean operator.\\
% 	It is evaluated by \cite{Hila08c}:
% 	\begin{equation}\label{eq:RNP}
% 		P = tr\pa{ \psi_\xi \pa{ M_2^\top M_2 + M_1^\top W_o M_1 } } +  \mu_{\xi'}^\top \mu_{\xi'}
% 	\end{equation}
% 	where $\mu_{\xi'} = (C_Z(I-A_Z)^{-1}M_1+M_2)\mu_\xi$ and $W_o$ is the observability gramian of the system $\mathcal{R}$.
% 
% 
% 
% 
% 
% 
% 
% 	Then, in \I{Roundoff Before Multiplication} (RBM) scheme, the quantizations only occur at the end of the additions, when the accumulator result is stored in intermediate variables, states or output, and a right-shift of $d_{ADD}$ bits is applied.
% 
% 	The lemma \ref{prop:quantization_noise} recalls the noise produced during shift:
% 	\begin{lemma}\label{prop:quantization_noise}
% 		Let $x(k)$ be a signal with fixed-point format $(\beta+d,\alpha+d)$. Right shifting $x(k)$ of $d$ bits is similar to add to $x(k)$ the independent white noise $e(k)$.\\% (see figure \ref{fig:quantization_noise}).
% 	%	\fig[scale=0.4]{quantization_noise}{Quantized a signal is similar to add a noise}\\
% 	The right shift could round $x(k)$ towards $-\infty$ (truncation: default behaviour) or toward the nearest integer (nearest rounding: possible with some additional hardware/software operations \cite{Laps96}). If $d>0$, the moments of $e(k)$ are given by:
% 	\begin{equation}
% 		\begin{array}{|c|c|c|}
% 			\hline & \text{truncation} & \text{best roundoff}\\
% 			\hline \mu_e & 2^{-\gamma-1}(1-2^{-d}) & 2^{-\gamma-d-1} \\
% 			\hline \sigma_e^2 & \frac{2^{-2\gamma}}{12}(1-2^{-2d}) & \frac{2^{-2\gamma}}{12}(1-2^{-2d}) \\
% 			\hline
% 		\end{array}
% 	\end{equation}
% 	else ($d\leq0$) $e(k)$ is null.
%	\end{lemma}
% 
% 	It is now possible to define the moments of $\xi(k)$:
% 
% 	Denote $\bar{\gamma} \triangleq \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_Y \end{pmatrix}$ and define $s$ by
% 	\begin{equation}
% 		s_i \triangleq \begin{cases}
% 			1 & \text{if } d_{ADDi} > 0 \\
% 			0 & \text{otherwise}
% 		\end{cases}
% 	\end{equation}
% 
% 	Then $\mu_\xi$ is given by:
% 	\begin{equation}
% 		\pa{\mu_\xi}_{i} = \begin{cases}
% 			s_i 2^{-\bar{\gamma}_i-1}  & \text{truncation}\\
% 			s_i 2^{-\bar{\gamma}_i-1-d_{ADD}} & \text{nearest rounding}
% 		\end{cases}
% 	\end{equation}
% 	and, since these noises are independent, $\psi_\xi$ is diagonal with:
% 	\begin{equation}
% 		\pa{\psi_\xi}_{i,i} = s_i\frac{2^{-2\bar{\gamma}_i}}{12} \pa{ 1 - 2^{-d_{ADD}}  }
% 	\end{equation}


%See also: <@FWR/setFPIS>, <@FWR/RNG>

%References:
%	\cite{Hila08c} T.�Hilaire, D.�M�nard, and O.�Sentieys. Bit
%	accurate roundoff noise analysis of fixed-point linear controllers. In Proc. IEEE International Symposium on Computer-Aided Control System Design (CACSD'08), September 2008.