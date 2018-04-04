%Purpose:
% Set the Fixed-Point Implementation Scheme (FPIS) of an FWR object
% (the wordlength may be matrices or scalar. The scalar case is used to set all the wordlength to the same length)
% 
%Syntax:
% R = setFPIS( R, betaU, Umax, betaZ, betaT, betaX, betaY, betaADD, betaG, method )
% R = setFPIS( R, FPIS)
% R = setFPIS( R, FPISname,Umax)
%
%Parameters:
% R: FWR object
% FPIS: an other Fixed-Point Implementation Scheme (a structure with betaU, Umax, betaZ, betaT, betaX, betaY, betaADD, betaG and method)
% FPISname : "DSP8" or "DSP16"
% betaU: wordlength of U (inputs)
% Umax: maximum value of U (necessary to set $\gamma_U$)
% betaZ: wordlength of the coefficients
% betaT, betaX, betaY: wordlength of the intermediate variables T, the states X and the outputs
% betaADD: wordlength of the accumulators
% betaG: nb of guard bits in the accumulators
% method: "RBM" (default) Roundoff Before Multiplication
%       : "RAM" Roundoff After Multiplication
%       : "qRBM" quasi Roundoff Before Mult. (Roundoff befor mult, except where the quantization produces underflow) 
%
% $Id: setFPIS.m 261 2015-01-26 13:04:13Z hilaire $


function R = setFPIS( R, betaU, Umax, betaZ, betaT, betaX, betaY, betaADD, betaG, method )

warning off MATLAB:log:logOfZero

% args : 'RBM' (default) => method=1; 'RAM' => method=2; 'qRBM' => method=3
if nargin==2
    if isempty(betaU)
        R.FPIS = [];
        return
    end
    try
        FPIS = betaU;
        betaU = FPIS.betaU;
        Umax = FPIS.Umax;
        betaZ = FPIS.betaZ;
        betaT = FPIS.betaT;
        betaX = FPIS.betaX;
        betaY = FPIS.betaY;
        betaADD = FPIS.betaADD;
        betaG = FPIS.betaG;
        method = FPIS.method;
    catch
        error([ 'R = setFPIS( R, FPIS); where FPIS is structure with ''betaU'', ''Umax'', ''betaZ'', ''betaT'', ''betaX'', ''betaY'', ''betaADD'', ''betaG'' and ''method''' ....
                'For example R1 = setFPIS(R1, R2.FPIS)' ]);
    end
elseif nargin==3
    if strcmp(betaU,'DSP8')
        betaU=8;
        betaZ=8;
        betaT=8;
        betaX=8;
        betaY=8;
        betaADD=16;
        betaG=0;
        method=2;
    elseif strcmp(betaU,'DSP16')
        betaU=16;
        betaZ=16;
        betaT=16;
        betaX=16;
        betaY=16;
        betaADD=32;
        betaG=0;
        method=2;
    else
        error( 'R = setFPIS( R, FPISname,Umax);   FPISname must be ''DSP8'' or ''DSP16''');
    end
elseif nargin<10
    method='RBM';
end

if strcmp(method,'RAM') | method==2
    method=2;
elseif strcmp(method,'qRBM') | method==3
    method=3;
else
    method=1;
end

% change args if they are scalar
if prod( size(betaZ) )==1
    betaZ = betaZ * ones(size(R.Z));
end
if prod( size(betaU) )==1
    betaU = betaU * ones(R.m,1);
end
if prod( size(betaT) )==1
    betaT = betaT * ones( R.l,1);
end
if prod( size(betaX) )==1
    betaX = betaX * ones( R.n,1);
end
if prod( size(betaY) )==1
    betaY = betaY * ones( R.p,1);
end
if prod( size(betaADD) )==1
    betaADD = betaADD * ones( size(R.Z,1), 1);
end
if prod( size(betaG) )==1
    betaG = betaG * ones( size(R.Z,1), 1);
end
if prod( size(Umax) )==1
	Umax = Umax*ones(R.m,1);
end
betaTXY = [ betaT; betaX; betaY ];
betaTXU = [ betaT; betaX; betaU ];

% magnitude
H6 = ss(R.AZ,R.BZ, [ inv(R.J)*R.M ; eye(R.n); R.CZ ], [inv(R.J)*R.N; zeros(R.n,R.m); R.DZ],1);
[Yimp Timp] = impulse(H6);
L1 = squeeze(sum(abs(Yimp)));
%Zp = R.Z + [ eye(R.l) zeros(R.l,R.n+R.m); zeros(R.n+R.p, R.l+R.n+R.m) ];
Zp = R.Z;
Zp(1:R.l,1:R.l) = Zp(1:R.l,1:R.l) + eye(R.l);


% find coefs where +2^p with p integer
eps=1e-10;
i2=find( Zp>0 & abs(rem(log2(abs(Zp)),1))<eps );
betaZ(i2)=2;


% gammas
gammaU = betaU - 2*ones(size(R.m,1),1) - floor( log2(abs(Umax)) );
gammaTXY = betaTXY - 2*ones(size(R.Z,1),1) - floor( log2( L1*Umax ) )';
gammaT = gammaTXY(1:R.l); gammaX = gammaTXY(R.l+1:R.l+R.n); gammaY = gammaTXY(R.l+R.n+1:end);
gammaTXU = [ gammaTXY(1:(R.l+R.n)); gammaU ];
gammaZ = betaZ - 2*ones(size(Zp)) - floor( log2(abs(Zp)) ); 

% gammaADD
alpha = max( betaZ - gammaZ + ones(size(Zp,1),1)*((betaTXU-gammaTXU)'),[],2 );
gammaADDmax = betaADD - max( betaTXY-betaG-gammaTXY, alpha); % RAM
gammaADD = min( gammaADDmax, max( (gammaZ + ones(size(Zp,1),1)*(gammaTXU)') .* ~isinf(gammaZ) ,[],2 ) );


% shift on multiplications
shiftZ = ones(size(Zp,1),1)*gammaTXU' + gammaZ - gammaADD*ones(1,size(R.Z,2));
shiftADD = gammaADD - gammaTXY;


% RBM
if method==1
    % underflow
    ind = find( ~isinf(shiftZ) & (betaZ- ones(size(Zp)) - shiftZ) < 0 );
    if ~isempty(ind)
        warning('underflow');
		for i=ind'
			display(['the value ' num2str(R.Z(i)) ' could not be represented']);
		end
    end
    % overflow
    %TODO!
    
    % new gammaZ
    gammaZ = gammaZ - shiftZ;
    shiftZ = zeros(size(Zp));
    gammaZ( find( isnan(gammaZ)) ) = Inf;
elseif method==3
    % underflow
    ind = find( ~ (~isinf(shiftZ) & (betaZ- ones(size(Zp)) - shiftZ) < 0) );
    if ~isempty(ind)
        for i=ind'
         gammaZ(i) = gammaZ(i) - shiftZ(i);
         shiftZ(i) = 0;
        end
        gammaZ( find( isnan(gammaZ)) ) = Inf;
    end
    ind = find( ~isinf(shiftZ) & (betaZ- ones(size(Zp)) - shiftZ) < 0 );
    for i=ind'
        display(['the coefficient ' num2str(R.Z(i)) ' need a Roundoff After Multiplication']);
    end
end

% build FPIS struct
R.FPIS = struct(    'betaU', betaU, ...
                    'Umax', Umax, ...
                    'betaZ', betaZ, ...
                    'betaT', betaT, ...
                    'betaX', betaX, ...
                    'betaY', betaY, ...
                    'betaADD', betaADD, ...
                    'betaG', betaG, ...
                    'method', method, ...
                    'gammaU', gammaU, ...
                    'gammaZ', gammaZ, ...
                    'gammaT', gammaT, ...
                    'gammaX', gammaX, ...
                    'gammaY', gammaY, ...
                    'gammaADD', gammaADD, ...
                    'shiftZ', shiftZ, ...
                    'shiftADD', shiftADD );
				
				
%Description:
% 	This function sets the Fixed-Point Implementation Scheme (FPIS).
% 	This structure is composed by:
% 	\begin{itemize}
% 		\item the fixed-point format of the input $(\beta_U,\gamma_U)$
% 		and its maximum magnitude value $\overset{\max}{U}$
% 		\item the fixed-point format of the intermediate variables $(\beta_T,\gamma_T)$
% 		\item the fixed-point format of the states $(\beta_X,\gamma_X)$
% 		\item the fixed-point format of the output $(\beta_Y,\gamma_Y)$
% 		\item the fixed-point format of the coefficients $(\beta_Z,\gamma_Z)$
% 		\item the fixed-point format of the accumulator $(\beta_{ADD}+\beta_{G},\gamma_{ADD})$ ($\beta_G$ guard bits)
% 		\item the right-shift bits after each scalar product $d_{ADD}$ (\matlab{shiftADD})
% 		\item the right-shift bits after each multiplication by a coefficient $d_Z$ (\matlab{shiftZ})
% 		\item the computational scheme : \I{Roundoff After Multiplication} (RAM) or \I{Roundoff Before Multiplication} (RBM)
% 	\end{itemize}
% 
% 	The algorithm
% 	\begin{align*}
% 		&\text{[i]} & JT(k+1) & \leftarrow MX(k) + NU(k)\\
% 		&\text{[ii]} & X(k+1)  & \leftarrow KT(k+1) + PX(k) + QU(k)\\
% 		&\text{[iii]} & Y(k)    & \leftarrow LT(k+1) + RX(k) + SU(k)
% 	\end{align*}
% 	requires to implement $l+n+p$ scalar products.\\
% 	Each scalar product
% 	\begin{equation}
% 		S = \sum_{i=1}^n P_i E_i
% 	\end{equation}
% 	where $\pa{P_i}_{1 \leq i \leq n}$ are given coefficients and
% 	$\pa{E_i}_{1 \leq i \leq n}$ some bounded variables, can be
% 	implemented according to the algorithms \ref{algo:setFPIS:setFPIS:RAM} and
% 	\ref{algo:setFPIS:setFPIS:RBM}, and where $P'_i$, $E'_i$ and $S'_i$ are the integer representation
% 	(according to their fixed-point format) to $P_i$,$E_i$ and
% 	$S_i$.\\
%	\begin{multicols}{2}{
% 	\begin{algorithm}[H]
%		\caption{\I{Roundoff After Multiplication} (RAM)\label{algo:setFPIS:setFPIS:RAM}}
% 		$Add\leftarrow 0$\\
% 		\For{$i$ from 0 to $n$}{$Add\leftarrow \pa{ P_i' * E_i' } >> d_i$}
% 		$S'_i \leftarrow Add >> d'_i$ 
% 	\end{algorithm} \ \\
% 	\begin{algorithm}[H]
%		\caption{\I{Roundoff Before Multiplication} (RBM)\label{algo:setFPIS:setFPIS:RBM}}
% 		$Add\leftarrow 0$\\
% 		\For{$i$ from 0 to $n$}{$Add\leftarrow \pa{ P_i' >> d_i } * E_i'$}
% 		$S'_i \leftarrow Add >> d_i'$
% 	\end{algorithm}}
%	\end{multicols}
%	Of course, $d_i$ represents the right-shift after each multiplication and $d'_i$ represents the final shift. They respectively correspond to the $d_Z$ and $d_{ADD}$ shift in the SIF algorithm.
% 
% 	The user may specify all the wordlengths ($\beta_U$, $\beta_T$, $\beta_X$, $\beta_Y$, $\beta_{ADD}$, $\beta_g$
% 	and $\beta_Z$) and $\overset{\max}{U}$. The binary-point positions are deduced by:
% 	\begin{equation}
% 		\gamma_U = \beta_U - 2 - \floor{ \log_2 \overset{\max}{U} }
% 	\end{equation}
% 
% 	\begin{equation}
% 			\begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_Y \end{pmatrix} =
% 			\begin{pmatrix} \beta_T \\ \beta_X \\ \beta_Y \end{pmatrix} - 2.\VecOne{l+n+p}{1} -
% 			\floor{ \log_2 \pa{ \norm{H_{\max}}_{l_1} \overset{\max}{\abs{U}} } }
% 	%		\left\lceil \log_2 \begin{pmatrix} \overset{\max}{\abs{T}} \\ \overset{\max}{\abs{X}} \\ \overset{\max}{\abs{Y}} \end{pmatrix} \right\rceil
% 	\end{equation}
% 	where $\VecOne{k}{l}$ represents the matrix of $\Rbb{k}{l}$ with all coefficients set to 1,
% 	$\norm{.}_{l_1}$ the $l_1$-norm and
% 	\begin{equation}
% 		H_{\max} : z \to N_1 \pa{ zI_n-A_Z }^{-1} B_Z + N_2,
% 	\end{equation}
% 	\begin{equation}
% 		N_1 \triangleq \begin{pmatrix}J^{-1}M \\ I_n \\ C_Z \end{pmatrix}, N_2 \triangleq \begin{pmatrix} J^{-1}N \\ 0 \\ D_Z \end{pmatrix}
% 	\end{equation}
% 
% 	The binary point position\footnote{$\pa{\gamma_Z}_{i,j}$ could be $-\infty$ for null coefficients, but it is not a problem because such coefficients are not implemented} $\gamma_Z$ of the coefficients $Z$ are given by:
% 	\begin{equation}\label{eq:gammaZ}
% 		\gamma_Z = \beta_Z - 2.\VecOne{l+n+p}{l+n+m} - \left \lfloor \strut \log_2 \abs{Z} \right\rfloor
% 	\end{equation}
% 	The fixed-point formats of the additions are given by:
% 	\begin{equation}
% 		\gamma_{ADD} = \beta_{ADD} - \underset{row}{\max} \pa{ \begin{pmatrix} \beta_T \\ \beta_X \\ \beta_Y \end{pmatrix} - \beta_g - \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_Y \end{pmatrix} , \alpha }
% 	\end{equation}
% 	where
% 	\begin{equation}
% 		\alpha = \underset{row}{\max} \pa { \beta_Z-\gamma_Z + \VecOne{l+n+p}{1} \pa{ \begin{pmatrix} \beta_T \\ \beta_X \\ \beta_U \end{pmatrix} - \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_U \end{pmatrix} }^{\hspace{-2mm}\top} }
% 	\end{equation}
% 	and $\underset{row}{\max}(M)$ returns a column vector with the maximum value of each row of $M$.\\
% 	The final alignments are right shifts of $d_{ADD}$ bits, with:
% 	\begin{equation}
% 		d_{ADD} = \gamma_{ADD} - \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_Y \end{pmatrix}
% 	\end{equation}
% 	Denote $\tilde\gamma_Z$ the final binary point position of the coefficients $Z$, according to \I{RAM} or \I{RBM} scheme, and $d_Z$ the shifts needed after each multiplication ($\pa{d_Z}_{i,j}$ is the right shift needed after the multiplication by $Z_{i,j}$) in order to align the format after each multiplication. Then:
% 	\begin{equation}
% 		\tilde\gamma_Z = \begin{cases}
% 			\gamma_Z & \text{if \I{RAM}}\\
% 			\gamma_{ADD}.\VecOne{1}{l+n+m} - \VecOne{l+n+p}{1}. \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_U \end{pmatrix}^{\hspace{-2mm}\top} & \text{if \I{RBM}}
% 		\end{cases}
% 	\end{equation}
% 	and
% 	\begin{equation}
% 		d_Z = \tilde\gamma_Z + \VecOne{l+n+p}{1}. \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_U \end{pmatrix}^{\hspace{-2mm}\top} - \gamma_{ADD}.\VecOne{1}{l+n+m}
% 	\end{equation}
% 	($d_Z$ is a null matrix in \I{RBM} case).\\
% 	With $d_Z$, $\tilde\gamma_Z$, $\gamma_{ADD}$, $d_{ADD}$, $\gamma_T$, $\gamma_X$ and $\gamma_Y$, the fixed-point implementation of the controller is entirely defined.

%See also: <@FWR/quantized>, <@FWS/setFPIS>

%References:
%\cite{Hila08c} T. Hilaire, D. Ménard, and O. Sentieys. Bit accurate roundoff noise analysis of fixed-point linear controllers. In Proc. IEEE International Symposium on Computer-Aided Control System Design (CACSD'08), September 2008.


				

