%Purpose:
% Compute the weighting $L_2$-norm of the system composed by $G \cd H = Vec(G).(Vec(H^\top))^\top$
% Each transfer function is weighted by the weighting matrix W.
% $G$ and $H$ are defined by their state-space matrices Ag,Bg,Cg,Dg and Ah,Bh,Ch,Dh.
%
%Syntax:
% [N, MX]= w_prod_norm( Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)
%
%Parameters:
% N: weighted norm
% MX: sensibility matrix of $G \cd H$
% Ag,Bg,Cg,Dg: state-space matrices of G
% Ah,Bh,Ch,Dh: state-space matrices of H
% W: weighting matrix
%
%
% $Id: w_prod_norm.m 208 2009-01-05 13:52:19Z fengyu $

function [N,MX] = w_prod_norm( Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W)

if size(Dg,1)*size(Dh,2)==1
    [N,MX] = w_prod_norm_SISO( Ag,Bg,Cg,Dg, Ah,Bh,Ch,Dh, W);
else
    
    % \TODO : check size ?
    Sg=ss(Ag,Bg,Cg,Dg,1);
    Sh=ss(Ah,Bh,Ch,Dh,1);
    
    % computation of the norm
    MX=zeros(size(W));
    for i=1:size(W,1)
        for j=1:size(W,2)
            if (W(i,j)~=0)
                MX(i,j) = norm(  Sg(:,i)*Sh(j,:) );
            end
        end
    end
    
    MX= MX.*W;
    
    N = norm(MX,'fro')^2;
end


%Description:
% 	\begin{center}\I{Internal function}\end{center}
%	From two MIMO state-space system $G$ and $H$, this function computes
%	the weighting $L_2$-norm of the system composed by 
%	\begin{equation}
%		G \cd H = Vec(G).(Vec(H^\top))^\top
%	\end{equation}
%	Each transfer function is weighted by the weighting matrice W
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

%See also: <@FWR/MsensH> <@FWR/MsensH_cl>, <@FWR/w_prod_norm_SISO>
