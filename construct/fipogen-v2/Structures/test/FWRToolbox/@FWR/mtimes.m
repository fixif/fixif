%Purpose:
% Multiply two FWR (put them in cascade)
%
%Syntax:
% R = R1*R2
% R = mtimes(R1,R2)
%
%Parameters:
% R: FWR result
% R1: first operand (FWR)
% R2: second operand (FWR)
%
% 
% $Id: mtimes.m 201 2009-01-03 22:31:50Z hilaire $


function R = mtimes(R1,R2);

if (R1.p~=R2.m)
    error('In R1*R2, realizations must have compatible dimensions.');
end

% dimensions
R.l = R1.l+R2.l+R1.p;
R.m = R1.m;
R.n = R1.n+R2.n;
R.p = R2.p;

% J,K,L,M,N,P,Q,R,S,Z
R.J = [ R1.J zeros(R1.l,R1.p) zeros(R1.l,R2.l); -R1.L eye(R1.p) zeros(R1.p,R2.l); zeros(R2.l,R1.l) -R2.N R2.J ];
R.K = [ R1.K zeros(R1.n,R1.p+R2.l); zeros(R2.n,R1.l) R2.Q R2.K ];
R.L = [ zeros(R2.p,R1.l) R2.S R2.L ];
R.M = [ R1.M zeros(R1.l,R2.n); R1.R zeros(R1.p,R2.n); zeros(R2.l,R1.n) R2.M ];
R.N = [ R1.N ; R1.S; zeros(R2.l,R1.m) ];
R.P = [ R1.P zeros(R1.n,R2.n); zeros(R2.n,R1.n) R2.P ];
R.Q = [ R1.Q; zeros(R2.n,R1.m) ];
R.R = [ zeros(R2.p,R1.n) R2.R ];
R.S = zeros(R2.p,R1.m);
R.Z = [];

% WJ,WK,WL,WM,WN,WP,WQ,WR,WS,WZ
R.WJ = [ R1.WJ zeros(R1.l,R1.p) zeros(R1.l,R2.l); R1.WL zeros(R1.p) zeros(R1.p,R2.l); zeros(R2.l,R1.l) R2.WN R2.WJ ];
R.WK = [ R1.WK zeros(R1.n,R1.p+R2.l); zeros(R2.n,R1.l) R2.WQ R2.WK ];
R.WL = [ zeros(R2.p,R1.l) R2.WS R2.WL ];
R.WM = [ R1.WM zeros(R1.l,R2.n); R1.WR zeros(R1.p,R2.n); zeros(R2.l,R1.n) R2.WM ];
R.WN = [ R1.WN ; R1.WS; zeros(R2.l,R1.m) ];
R.WP = [ R1.WP zeros(R1.n,R2.n); zeros(R2.n,R1.n) R2.WP ];
R.WQ = [ R1.WQ; zeros(R2.n,R1.m) ];
R.WR = [ zeros(R2.p,R1.n) R2.WR ];
R.WS = zeros(R2.p,R1.m);
R.WZ = [];

% AZ,BZ,CZ,DZ, gramians
R.AZ=[]; R.BZ=[]; R.CZ=[]; R.DZ=[];
R.Wc=[]; R.Wo=[];

R.FPIS=[];
warning('TODO: mettre ˆ jour le FPIS en fonction du FPIS de R1 et R2');

% fp,block
if (R1.fp~=R2.fp) | (R1.block~=R2.block) 
    R.fp=1; R.block=2; R.rZ=[];
else
    R.fp=R1.fp; R.block=R1.block; R.rZ=[];
end


% build class and complete the other values
R = class(R,'FWR');
R = computeAZBZCZDZWcWo(R);
R = computeZ(R);
R = compute_rZ(R);

%Description:
% \fig[scale=0.3]{cascade}{Two realizations in cascade}
% Put two realization in cascade (see figure \ref{fig:cascade}).\\
% We consider two realizations $\mathcal{R}_1:=(J_1,K_1,L_1,M_1,N_1,P_1,Q_1,R_1,S_1)$
%and $\mathcal{R}_2:=(J_2,K_2,L_2,M_2,N_2,P_2,Q_2,R_2,S_2)$ (with compatible size,
%\I{i.e.} $p_1=m_2$).\\
% By introducing an intermediate variable $T$ equal to the output of $\mathcal{R}_1$,
%the resulting realization $\mathcal{R}$ can be expressed in the implicit form by :
% \begin{footnotesize}
% \begin{equation*}
% 	\begin{pmat}({..|.|})
% 		J_1 & 0 & 0 & 0 & 0 & 0 \cr
% 		-L_1 & I & 0 & 0 &0 & 0 \cr
% 		0 & -N_2 & J_2 & 0 & 0 & 0 \cr\-
% 		-K_1 & 0 & 0 & I & 0 & 0 \cr
% 		0 & -Q_2 & -K_2 & 0 & I & 0 \cr\-
% 		0 & -S_2 & -L_2 & 0 & 0 & I \cr
% 	\end{pmat}
% 	\begin{pmatrix}
% 		T_1(k+1) \\
% 		T(k+1) \\
% 		T_2(k+1) \\
% 		X_1(k+1) \\
% 		X_2(k+1) \\
% 		Y_2(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmat}({..|.|})
% 		0 & 0 & 0 & M_1 & 0 & N_1 \cr
% 		0 & 0 & 0 & R_1 & 0 & S_1 \cr
% 		0 & 0 & 0 & 0 & M_2 & 0 \cr\-
% 		0 & 0 & 0 & P_1 & 0 & Q_1 \cr
% 		0 & 0 & 0 & 0 & P_2 & 0 \cr\-
% 		0 & 0 & 0 & 0 & R_2 & 0 \cr
% 	\end{pmat}
% 	\begin{pmatrix}
% 		T_1(k) \\
% 		T(k) \\
% 		T_2(k) \\
% 		X_1(k) \\
% 		X_2(k) \\
% 		U_1(k)
% 	\end{pmatrix}
% \end{equation*}
% \end{footnotesize}

%See also: <@FWR/plus>
