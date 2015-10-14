%Purpose:
% Compute the open-loop transfer function error $\sigma_{\Delta H}^2$)
%
%Syntax:
% [e, eZ]  = sigma_tf(R)
%
%Parameters:
% e: transfer function error
% e: transfer function error matrix
% R: FWR object
%
%
% $Id$


function [e, eZ] = sigma_tf( R)

% intermediate matrices
M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
M2 = [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ];
N1 = [ inv(R.J)*R.M; eye(R.n); zeros(R.m,R.n) ];
N2 = [ inv(R.J)*R.N; zeros(R.n,R.m); eye(R.m) ];
Te = 1;

% is FPIS set ?
if isempty(R.FPIS)
	error('the FPIS is required - used function ''error_tf'' instead')
end

% transfer function error and transfer function error matrix
sigmaZ = 2/sqrt(3)* 2.^-R.FPIS.betaZ .* 2.^floor(log2(abs(R.Z))) .* R.WZ;
sigmaZ( R.WZ==0 .* isnan(sigmaZ) ) = 0;	% remove NaN (where R.WZ==0)
[e, eZ] = w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, sigmaZ );


%Description:
% 	The open-loop transfer function error is defined by
%	\begin{equation}
%		\sigma_{\Delta H}^2 \triangleq \frac{1}{2\pi} \int_0^{2\pi} E\left\{ \abs{\Delta H \pa{ e^{j\omega} }}^2 \right\} d\omega
%	\end{equation}
% 	where $E\{.\}$ is the mean operator.



%See also: <@FWR/MsensH>,<@FWR/error_tf>


