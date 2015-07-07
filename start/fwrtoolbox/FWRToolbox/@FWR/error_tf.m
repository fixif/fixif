%Purpose:
% Compute the open-loop normalized transfer function error $M'_{L_2}$
%
%Syntax:
% [e, eZ]  = error_tf(R)
%
%Parameters:
% e: normalized transfer function error
% e: normalized transfer function error matrix
% R: FWR object
%
%
% $Id$


function [e, eZ] = error_tf( R)

% intermediate matrices
M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
M2 = [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ];
N1 = [ inv(R.J)*R.M; eye(R.n); zeros(R.m,R.n) ];
N2 = [ inv(R.J)*R.N; zeros(R.n,R.m); eye(R.m) ];
Te = 1;


% normalized transfer function error and normalized transfer function error matrix
sigmaZ = 2.^floor(log2(abs(R.Z))) .* R.WZ;
sigmaZ( R.WZ==0 .* isnan(sigmaZ) ) = 0;	% remove NaN (where R.WZ==0)
[e, eZ] = w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, sigmaZ );


%Description:
% 	The open-loop normalized transfer function error is defined by
%	\begin{equation}
%		M'_{L_2} \triangleq \norm{ \dd{H}{Z} \times \left\lfloor Z \right\rfloor_2 \times W_Z }_2^2
%	\end{equation}
% 	where $\left\lfloor x \right\rfloor_2$ is the power of 2
% 	immediately lower than $\abs{x}$
% 	\begin{equation}
% 		\left\lfloor x \right\rfloor_2 \triangleq 2^{\left\lfloor \strut \log_2\abs{x} \right\rfloor }.
% 	\end{equation}



%See also: <@FWR/MsensH>,<@FWR/sigma_tf>


