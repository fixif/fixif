%Purpose:
% Compute the closed-loop pole sensitivity stability related measure
%  for a FWR object 
%
%Syntax:
% M = Mstability( R, Sysp, moduli)
%
%Parameters:
% M: pole sensitivity measure
% R: FWR object
% Sysp: plant system (ss object)
% moduli : 1 (default value) : compute $\dd{\abs{\bar\lambda}}{Z}$ (the sensitivity of the moduli of the eigenvalues)
%        : 0 : compute $\dd{\bar\lambda}{Z}$ (without the moduli)
%
% $Id$


function M = Mstability( R, Sysp, moduli)

% args
if (nargin<3)
    moduli = 1;
end

% MsensPole_cl
[ M, dlambdabar_dZ, dlbk_dZ] = MsensPole_cl( R, Sysp, moduli);



% sizes
np = size(Sysp.A,1);
m = size(Sysp.C,1);
p = size(Sysp.B,2);
l=R.l; m2=R.m; n=R.n; p2=R.p;
m1=m-m2;
p1=p-p2;
if ( (p1<0) | (m1<=0) )
    error('dimension error - check plant and realization dimension');
end


% plant matrices
B1 = Sysp.B(:,1:p1);
B2 = Sysp.B(:,p1+1:p);
C1 = Sysp.C(1:m1,:);
C2 = Sysp.C(m1+1:m,:);
D11 = Sysp.D(1:p1,1:m1);
D12 = Sysp.D(1:p1,m1+1:m);
D21 = Sysp.D(p1+1:p,1:m1);
D22 = Sysp.D(p1+1:p,m1+1:m);
if (D22~=zeros(size(D22)))
    error('D22 needs to be null')
end

% closedloop related matrices
Abar = [ Sysp.A + B2*R.DZ*C2 B2*R.CZ;
         R.BZ*C2 R.AZ];
lambda = eig(Abar)';



% measure
for k=1:size(dlbk_dZ,3)
    Psi(k) = norm( R.WZ, 'fro') * norm( dlbk_dZ(:,:,k) .* R.rZ, 'fro');
end
M = min( (1-abs(lambda)) ./ Psi );


%Description:
% 	The Pole Sensitivity Stability related Measure (PSSM) is defined by
% 	\begin{equation}
% 		\mu_1(Z) \triangleq \underset{1 \leq k \leq \np+n}{\min} \frac{ 1- \abs{\strut \bar\lambda_k} }{ \norm{W_Z}_F \norm{ \dd{\abs{\bar\lambda_k}}{Z} \times W_Z }_F }.
% 	\end{equation}
% 	This measure evaluates how a perturbation, $\Delta$, of the parameters, $Z$, can cause instability. It is determined by how close  the eigenvalues of $\bar{A}$ are to the unit circle and by how sensitive they are to the controller parameter perturbation.\\
% 	See \funcName[@FWR/MsensPolecl]{MsensPole\_cl} for the
% 	computation of $\dd{\abs{\bar\lambda_k}}{Z}$.

%See also: <@FWR/MsensPole_cl>, <@FWS/Mstability>
%References:
%	\cite{Hila08b} T. Hilaire, P. Chevrel, and J. Whidborne. Finite wordlength
%	controller realizations using the specialized implicit form.
%	Technical Report RR-6759, INRIA, 2008.