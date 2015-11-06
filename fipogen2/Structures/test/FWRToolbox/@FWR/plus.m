%Purpose:
% add two FWR object (put them in parallel)
%
%Syntax:
% R = R1+R2
% R = plus(R1,R2,generalform)
%
%Parameters:
% R: FWR result
% R1: first FWR
% R2: second FWR
% generalform: (default is true) to use the general form (or a particular form) 
%
% $Id: plus.m 180 2008-12-12 19:13:32Z hilaire $


function R = plus( R1, R2, generalform);

if ( (R1.m~=R2.m) | (R1.p~=R2.p) )
    error('In R1+R2, realizations must have compatible dimensions.');
end

if nargin==2
    generalform=1;
end

if generalform==1
    % general form
    
    % dimensions
    R.l = R1.l+R1.p+R2.l+R2.p;
    R.m = R1.m;
    R.n = R1.n+R2.n;
    R.p = R1.p;

    % J,K,L,M,N,P,Q,R,S?Z
    R.J = [ R1.J zeros(R1.l,R.l-R1.l) ; -R1.L eye(R1.p) zeros(R1.p,R2.l+R2.p) ; zeros(R2.l,R1.l+R1.p) R2.J zeros(R2.l,R2.p) ; zeros(R2.p,R1.l+R1.p) -R2.L eye(R2.p) ];
    R.K = [ R1.K zeros(R1.n,R.l-R1.l) ; zeros(R2.n,R1.l+R1.p) R2.K zeros(R2.n,R2.p) ];
    R.L = [ zeros(R.p,R1.l) eye(R.p) zeros(R.p,R2.l) eye(R.p) ];
    R.M = [ R1.M zeros(R1.l,R2.n) ; R1.R zeros(R1.p,R2.n) ; zeros(R2.l,R1.n) R2.M ; zeros(R2.p,R1.n) R2.R ];
    R.N = [ R1.N ; R1.S ; R2.N ; R2.S ];
    R.P = [ R1.P zeros(R1.n,R2.n) ; zeros(R2.n,R1.n) R2.P ];
    R.Q = [ R1.Q ; R2.Q ];
    R.R = zeros(R.p,R1.n+R2.n);
    R.S = zeros(R.p,R.m);
    R.Z = [];
    
    % WJ,WK,WL,WM,WN,WP,WQ,WR,WS,WZ
    R.WJ = [ R1.WJ zeros(R1.l,R.l-R1.l) ; R1.WL zeros(R1.p) zeros(R1.p,R2.l+R2.p) ; zeros(R2.l,R1.l+R1.p) R2.WJ zeros(R2.l,R2.p) ; zeros(R2.p,R1.l+R1.p) R2.WL zeros(R2.p) ];
    R.WK = [ R1.WK zeros(R1.n,R.l-R1.l) ; zeros(R2.n,R1.l+R1.p) R2.WK zeros(R2.n,R2.p) ];
    R.WL = [ zeros(R.p,R.l)];
    R.WM = [ R1.WM zeros(R1.l,R2.n) ; R1.WR zeros(R1.p,R2.n) ; zeros(R2.l,R1.n) R2.WM ; zeros(R2.p,R1.n) R2.WR ];
    R.WN = [ R1.WN ; R1.WS ; R2.WN ; R2.WS ];
    R.WP = [ R1.WP zeros(R1.n,R2.n) ; zeros(R2.n,R1.n) R2.WP ];
    R.WQ = [ R1.WQ ; R2.WQ ];
    R.WR = zeros(R.p,R1.n+R2.n);
    R.WS = zeros(R.p,R.m);
    R.WZ = [];
    
    % AZ,BZ,CZ,DZ   
    R.AZ=[]; R.BZ=[]; R.CZ=[]; R.DZ=[];
    R.Wc=[]; R.Wo=[];
	
else
    % particular form (the parametrization is changed, the two constants terms are regrouped)
    
    % dimensions
    R.l = R1.l+R2.l;
    R.m = R1.m;
    R.n = R1.n+R2.n;
    R.p = R1.p;

    % J,K,L,M,N,P,Q,R,S?Z
    R.J = [ R1.J zeros(R1.l,R2.l) ; zeros(R2.l,R1.l) R2.J ];
    R.K = [ R1.K zeros(R1.n,R2.l) ; zeros(R2.n,R1.l) R2.K ];
    R.L = [ R1.L R2.L ];
    R.M = [ R1.M zeros(R1.l,R2.n) ; zeros(R2.l,R1.n) R2.M ];
    R.N = [ R1.N ; R2.N ];
    R.P = [ R1.P zeros(R1.n,R2.n) ; zeros(R2.n,R1.n) R2.P ];
    R.Q = [ R1.Q ; R2.Q ];
    R.R = [ R1.R R2.R ];
    R.S = R1.S+R2.S;
    R.Z = [];
    
    % WJ,WK,WL,WM,WN,WP,WQ,WR,WS,WZ
    R.WJ = [ R1.WJ zeros(R1.l,R2.l) ; zeros(R2.l,R1.l) R2.WJ ];
    R.WK = [ R1.WK zeros(R1.n,R2.l) ; zeros(R2.n,R1.l) R2.WK ];
    R.WL = [ R1.WL R2.WL ];
    R.WM = [ R1.WM zeros(R1.l,R2.n) ; zeros(R2.l,R1.n) R2.WM ];
    R.WN = [ R1.WN ; R2.WN ];
    R.WP = [ R1.WP zeros(R1.n,R2.n) ; zeros(R2.n,R1.n) R2.WP ];
    R.WQ = [ R1.WQ ; R2.WQ ];
    R.WR = [ R1.WR R2.WR ];
    R.WS = or( R1.WS, R2.WS);
    R.WZ = [];
   
    % AZ,BZ,CZ,DZ, gramians
    R.AZ=[]; R.BZ=[]; R.CZ=[]; R.DZ=[];
    R.Wc=[]; R.Wo=[];
end

% FPIS
if (R1.FPIS==R2.FPIS)
	R.FPIS=R1.FPIS;
else
	R.FPIS=[];
end

% fp, block
if (R1.fp~=R2.fp) | (R1.block~=R2.block) 
    R.fp=1; R.block=2; R.rZ=[];
else
    R.fp=R1.fp; R.block=R1.block; R.rZ=[];
end

% build the class and complete the over values
R = class(R,'FWR');
R = computeAZBZCZDZWcWo(R);
R = computeZ(R);
R = compute_rZ(R);


%Description:
%\fig[scale=0.3]{parallel}{Two realizations in parallel}
%Put two realization in parallel (see figure \ref{fig:parallel}).\\
%We consider two realizations $\mathcal{R}_1:=(J_1,K_1,L_1,M_1,N_1,P_1,Q_1,R_1,S_1)$
%and $\mathcal{R}_2:=(J_2,K_2,L_2,M_2,N_2,P_2,Q_2,R_2,S_2)$ (with compatible size, \I{i.e.}
%$m_1=m_2$ and $p_1=p_2$).\\
%By introducing the intermediate variables $T_1'$ and $T_2'$ equal to the output
%of the two realizations, the resulting realization $\mathcal{R}$ (\I{general} form)
%can be expressed in the implicit form by
% \begin{footnotesize}
% \begin{equation*}
% 	\begin{pmat}({...|.|})
% 		J_1 & 0 & 0 &0 & 0 & 0 & 0 \cr
% 		-L_1 & I_{p_1} & 0 & 0 & 0 &0 & 0 \cr
% 		0 & 0 & J_2 & 0 & 0 &0 & 0 \cr
% 		0 & 0 & -L_2 & I_{p_2} & 0 & 0 & 0 \cr\-
% 		-K_1 & 0 & 0 & 0 & I_{n_1} & 0 & 0 \cr
% 		0 & 0 & -K_2 & 0 & 0 & I_{n_2} & 0 \cr\-
% 		0 & -I_{p} & 0 & -I_{p} & 0 & 0 & I_{p} \cr
% 	\end{pmat}
% 	\begin{pmatrix}
% 		T_1(k+1) \\
% 		T_1'(k+1) \\
% 		T_2(k+1) \\
% 		T_2'(k+1) \\
% 		X_1(k+1) \\
% 		X_2(k+1) \\
% 		Y_2(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmat}({...|.|})
% 		0 & 0 & 0 & 0 & M_1 & 0 & N_1 \cr
% 		0 & 0 & 0 & 0 & R_1 & 0 & S_1 \cr
% 		0 & 0 & 0 & 0 & 0 & M_2 & N_2 \cr
% 		0 & 0 & 0 & 0 & 0 & R_2 & S_2 \cr\- 
% 		0 & 0 & 0 & 0 & P_1 & 0 & Q_1 \cr
% 		0 & 0 & 0 & 0 & 0 & P_2 & Q_2 \cr\-
% 		0 & 0 & 0 & 0 & 0 & 0 & 0 \cr
% 	\end{pmat}
% 	\begin{pmatrix}
% 		T_1(k) \\
% 		T_1'(k) \\
% 		T_2(k) \\
% 		T_2'(k) \\
% 		X_1(k) \\
% 		X_2(k) \\
% 		U_1(k)
% 	\end{pmatrix}
% \end{equation*}
% \end{footnotesize}
% If we allow to regroup $S_1$ and $S_2$ in one term $S$ (and changing a bit
% the parametrization if $S_1$ and $S_2$ are both non-zero), the resulting 
% realization can be expressed in a \I{compact} form :
% \begin{footnotesize}
% \begin{equation*}
% 	\begin{pmat}({.|.|})
% 		J_1 & 0  & 0 & 0 & 0 \cr
% 		0 &  J_2  & 0 &0 & 0 \cr\-
% 		-K_1 & 0 & I_{n_1} & 0 & 0 \cr
% 		0 & -K_2 & 0 & I_{n_2} & 0 \cr\-
% 		-L_1 & -L_2 & 0 & 0 & I_{p} \cr
% 	\end{pmat}
% 	\begin{pmatrix}
% 		T_1(k+1) \\
% 		T_2(k+1) \\
% 		X_1(k+1) \\
% 		X_2(k+1) \\
% 		Y_2(k)
% 	\end{pmatrix}
% 	=
% 	\begin{pmat}({.|.|})
% 		0 & 0 & M_1 & 0 & N_1 \cr
% 		0 & 0 & 0 & M_2 & N_2 \cr\-
% 		0 & 0 & P_1 & 0 & Q_1 \cr
% 		0 & 0 & 0 & P_2 & Q_2 \cr\-
% 		0 & 0 & R_1 & R_2 & \pa{S_1+S_2} \cr
% 	\end{pmat}
% 	\begin{pmatrix}
% 		T_1(k) \\
% 		T_1'(k) \\
% 		T_2(k) \\
% 		T_2'(k) \\
% 		X_1(k) \\
% 		X_2(k) \\
% 		U_1(k)
% 	\end{pmatrix}
% \end{equation*}
% \end{footnotesize}	
% If $S_1$ and/or $S_2$ are null, the two forms are equivalent (in finite precision).

%See also: <@FWR/mtimes>