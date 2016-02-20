%Purpose: 
% Optimal $\rho$-based modal realization under FWR structure
% , in which the parameter $\Delta$ is reserved for relaxed $L_2$-scaling and implemented
% exactly, while the Parameter $\gamma$ is optimized analytically and is supposed to be coded
% exactly
%
%Syntax:
% R = OpModalrho2FWR( SYS, Wcii )
% R = OpModalrho2FWR( Aq, Bq, Cq, Dq, Wcii )
%
%Parameters:
% R: FWR object
% SYS: State-space object
% Aq,Bq,Cq,Dq: State-space ($q$-operator) matrices
% Wcii: diagonal controllabily gramian desired values. If 'Wcii' is empty, no scaling is applied
%
% $Id: OpModalrho2FWR.m 83 2008-09-30 15:00:31Z feng $


function R = OpModalrho2FWR( Aq, Bq, Cq, Dq, Wcii )

% if "R = OpModalrho2FWR( SYS )"

if (nargin<=2)
    S=Aq;
	if nargin==2
		Wcii=Bq;
	end
    Aq=S.A;
    Bq=S.B;
    Cq=S.C;
    Dq=S.D;

end
    
n=size(Aq,1);
% Construct q-based modal realisation with relaxed L2-scaling  
[A B C D] = canon_modal(  Aq, Bq, Cq, Dq );
R_modale = SS2FWR( A, B, C, D);
if (nargin==1 || nargin==4)
	R_modale = relaxedl2scaling(R_modale);
else
	R_modale = l2scaling(R_modale, Wcii);
end
R_modale = computeW(R_modale);

% Optimization of Gamma
for i=1:n
	if rem(i,2)==1
		Gamma(i)=R_modale.P(i,i)+R_modale.P(i,i+1)*R_modale.Wc(i+1,i)/R_modale.Wc(i,i);
	else
		Gamma(i)=R_modale.P(i,i)+R_modale.P(i,i-1)*R_modale.Wc(i,i-1)/R_modale.Wc(i,i);
	end
end



% le code qui suit remplace 
% R = Modalrho2FWR( Aq, Bq, Cq, Dq,  r, 1);
% car il n'est pas besoin du début du code de Modalrho2FWR

%L2-scaling on Tk
delta=zeros(1,n);
R_modale.Wc ;
Wt = R_modale.BZ*R_modale.BZ' + ( R_modale.AZ-diag(Gamma) )* R_modale.Wc * ( R_modale.AZ-diag(Gamma) )';
    
  for i=1:n
      delta(i) = 2^( floor( log2( sqrt( Wt( i, i ) ) ) ) );
      %delta(i) =  sqrt( Wt( i, i ) );
  end   
    
% compute equivalent Arho, Brho, Crho, Drho
Arho = inv(diag(delta)) * ( R_modale.AZ-diag(Gamma) );
Brho = inv(diag(delta)) * R_modale.BZ;
Crho = R_modale.CZ;
Drho = R_modale.DZ;


m=size(Crho,1);

% build FWR object
R = FWR( eye(n), diag(delta), zeros(m,n), Arho, Brho, diag(Gamma), zeros(size(Brho)), Crho, Drho);

R.WK = zeros(size(R.K));
R.WP = zeros(size(R.P));

















%Description:
%The realization's structure applied here is the same as what is used for \funcName[@FWR/Modaldelta2FWR]{Modaldelta2FWR}. $\Delta$ is reserved for relaxed $L_2$-scaling, and the choice of $\gamma$ is given: 
% \begin{equation}\label{eq:choice_gamma}
%   \gamma_{i}=\left\{
%      \begin{array}{ll}
%        \alpha_{i}+\frac{\beta_{i}\big(W_{cX}\big)_{i+1,i}}{\big(W_{cX}\big)_{i,i}}, & \hbox{i is odd;}\\
% \alpha_{i}+\frac{\beta_{i}\big(W_{cX}\big)_{i,i-1}}{\big(W_{cX}\big)_{i,i}}, & \hbox{i is even.}
%       \end{array}
%     \right.
% \end{equation}
% where $W_{cX}$ is the controllability gramian associated with the state such as:
% \begin{equation}\label{eq:calcul_SIF_relaxed_L2}
%         W_{cX}=A_{Z}W_{cX}A_{Z}^{T}\!+\!B_{Z}B_{Z}^{T}
% \end{equation}
%
%See also: <Modalrho2FWR>

%References:
%  \cite{Feng09a} Y. Feng, P. Chevrel, and T. Hilaire. A practival strategy of an efficient and sparse FWL implementation of LTI filters. In submitted to ECC'09, 2009.\\
