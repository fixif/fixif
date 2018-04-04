%Purpose:
% Compute the weighting $L_2$-norm of the system composed by $G \cd H = Vec(G).(Vec(H^\top))^\top$
% Each transfer function is weighted by this weighting matrix W.
% $G$ and $H$ are SIMO and MISO state-space system defined by their state-space matrices Ag,Bg,Cg,Dg and Ah,Bh,Ch,Dh.
%
%Syntax:
% [N, MX]= w_prod_normSISO( Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)
%
%Parameters:
% N: weighted norm
% MX: sensibility matrix of $G \cd H$
% Ag,Bg,Cg,Dg: state-space matrices of G
% Ah,Bh,Ch,Dh: state-space matrices of H
% W: weighting matrix
%
%
% $Id$

function [N,MX] = w_prod_norm_SISO( Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)

% \TODO : check size ?

% product matrices
A = [ Ag zeros(size(Ag,1),size(Ah,2)); Bh*Cg Ah ];
B = [ Bg ;  Bh*Dg ];
C = [ Dh*Cg Ch ];
D = [ Dh*Dg ];


% Balance A matrix prior to performing Schur decomposition
%[t,A] = balance(A);
%B = t\B;
%C = C*t;

% Perform schur decomposition on AA (and convert to complex form)
[m,n] = size(A);
AA = (A+eye(m))\(A-eye(m));
[ua,ta] = schur(AA);
[ua,ta] = rsf2csf(ua,ta);


% test
r = eig(A);
if max(abs(r))>=1,
    % Unstable system
    warning('Unstable system: 2-norm is infinite.')
end


% computation of the norm
MX=zeros(size(W));
for i=1:size(W,1)
    
    %P = dlyap(A,B(:,i)*B(:,i)');
    BB = (eye(m)-AA)*B(:,i)*B(:,i)'*(eye(m)-AA')/2;
    P = mylyap( AA,AA',BB, ua, ta);  
    
    for j=1:size(W,2)
       	if (W(i,j)~=0)

            % compute the H2-norm of the system ( A, B(:,i), C(j,:), D(j,i) )
            %MX(i,j) = H2dnorm( A, B(:,i), C(j,:), D(j,i), ua,ta, t );
            
            % || G ||^2 = trace(c*P*c'+d*d') where a*P*a'-P+b*b' = 0
            MX(i,j) = sqrt( trace( C(j,:)*P*C(j,:)'+D(j,i)*D(j,i)') );
            sqrt( trace( C(j,:)*P*C(j,:)'+D(j,i)*D(j,i)') );
            
            %MX(i,j) = norm( ss( A, B(:,i), C(j,:), D(j,i), 1 ) );
            
       	end
   	end
end

MX= MX.*W;

N = norm(MX,'fro')^2;


%Description:
% 	\begin{center}\I{Internal function}\end{center}
%	From two SIMO and MISO state-space system $G$ and $H$, this function compute
%	the weighting $L_2$-norm of the system composed by 
%	\begin{equation}
%		G \cd H = Vec(G).(Vec(H^\top))^\top
%	\end{equation}
%	Each transfer function is weighted by the weighting matrix W
%	$G$ and $H$ are defined by their state-space matrices
%	$G:=(A_G,B_G,C_G,D_G)$ and $H:=(A_H,B_H,C_H,D_H)$
%
%	The results $N$ and $MX$ are given by:
% 	\begin{equation}
% 		MX_{ij} \triangleq \norm{ \pa{ G \cd H }_{ij} W_{ij} }_2
% 	\end{equation}
% 	\begin{eqnarray}
% 		N &\triangleq& \norm{ (G \cd H) \times W }_2^2 \\
% 		&=& \norm{ MX}^2_F
% 	\end{eqnarray}
% 	This function is used by \funcName[@FWR/MsensH]{MsensH} and \funcName[@FWR/MsensHcl]{MsensH\_cl}.
%
% 	In that case, due to the SISO size of the transfer function $(G \cd H)_{ij}$, it is possible to use that
% 	\begin{eqnarray}
% 		MX_{ij} &=&\norm{ (G H)_{i,j} }_2 \\
% 		&=& \norm{
% 		\left(\begin{array}{cc|c}
% 			A_G & 0 & (B_G)_i \\
% 			B_H C_G & A_H & B_H D_G \\
% 			\hline \vspace{-3.5mm}\\
% 			D_H C_G & C_H & D_H D_G
% 		\end{array}\right)_{i,j}}_2
% 	\end{eqnarray}	
% %	The $(l+n+1)\times(l+n+1)$ $L_2$-norm evaluations here require  only $l+n+1$ Lyapunov equations to be solved (instead of the $(l+n+p)\times(l+n+m_2)$ equations in the MIMO case represented by \eqref{eq:expr_dedeHbardZ}), so this expression is preferred.

%See also: <@FWR/MsensH> <@FWR/MsensH_cl>, <@FWR/w_prod_norm>

