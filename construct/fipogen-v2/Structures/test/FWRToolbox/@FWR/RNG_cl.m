%Purpose:
% Compute the closed-loop Roundoff Noise Gain
%
%Syntax:
% G = RNG( R, Sysp)
% [G, dZ] = RNG(R, Sysp, tol)
%
%Parameters:
% G: roundoff noise gain
% dZ: number of non-trivial parameters (used by @FWS/RNG)
% R: FWR object
% Sysp: plant (to be controlled)
% tol: tolerance on trivial parameters (default=1e-8)
%
% $Id$


function [G, dZ, M1M2Wobar] = RNG_cl(R, Sysp, tol)

if nargin==2
    tol=1e-8;
end


% sizes
np = size(Sysp.A,1);
m = size(Sysp.C,1);
p = size(Sysp.B,2);
l=R.l; m2=R.m; n=R.n; p2=R.p;
m1=m-m2;
p1=p-p2;
if ( (p1<=0) | (m1<=0) )
    error('dimension error - check plant and realization dimension');
end


% plant matrices
B1 = Sysp.B(:,1:p1);
B2 = Sysp.B(:,p1+1:p);
C1 = Sysp.C(1:m1,:);
C2 = Sysp.C(m1+1:m,:);

%D11 = Sysp.D(1:p1,1:m1);
%D12 = Sysp.D(1:p1,m1+1:m);
%D21 = Sysp.D(p1+1:p,1:m1);
%D22 = Sysp.D(p1+1:p,m1+1:m);

% JOA bug correction
D11 = Sysp.D(1:m1, 1:p1);
D12 = Sysp.D(1:m1, p1+1:p);
D21 = Sysp.D(m1+1:m, 1:p1);
D22 = Sysp.D(m1+1:m, p1+1:p);


if (D22~=zeros(size(D22)))
    error('D22 needs to be null')
end

% closedloop related matrices
Abar = [ Sysp.A + B2*R.DZ*C2 B2*R.CZ;
         R.BZ*C2 R.AZ];
Bbar = [ B1 + B2*R.DZ*D21; R.BZ*D21 ];
Cbar = [ C1 + D12*R.DZ*C2 D12*R.CZ ];
Dbar = D11 + D12*R.DZ*D21;

% intermediate matrices
M1bar = [ B2*R.L*inv(R.J) zeros(np,n) B2;
          R.K*inv(R.J) eye(n) zeros(n,p2) ];
M2bar = [ D12*R.L*inv(R.J) zeros(m1,R.n) D12 ];      

% RNG
Wobar = gram( ss(Abar,Bbar,Cbar,Dbar,1), 'o');
W01Z = computeWeight(R.Z,tol);
dZ = diag( W01Z*ones(R.l+R.n+R.m,1) );

G = trace( dZ * ( M2bar'*M2bar + M1bar'*Wobar*M1bar ) );

M1M2Wobar = M2bar'*M2bar + M1bar'*Wobar*M1bar;



% compute the weighting matrix for one matrix
function W = computeWeight(X,tol)

N=size(X);
W=ones(size(X));
i = find( (abs(X-1)<tol) | (abs(X)<tol) | (abs(X+1)<tol) );
W(i)=0;



%Description:
% 	This function computes the Roundoff Noise Gain (in closed-loop context).\\
% 	The Roundoff Noise Gain is the output noise power computed in a specific computational scheme : the noises are supposed to
% 	appear only after each multiplication and are modeled by centered white noise statistically independent.\\ Each noise is
% 	supposed to have the same power $\sigma_0^2$ (determined by the wordlength choosen for all the variables and coefficients).\\
% 
% 	The Roundoff Noise Gain is defined by
% 	\begin{equation}
% 		\bar{G} \triangleq \frac{\bar{P}}{\sigma_0^2}
% 	\end{equation}
% 	where $\bar{P}$ is the output roundoff noise power (the global noise added on the output of the plant).
% 
% 	It could be computed by
%	\begin{equation}
%		\bar{G} = tr\pa{ d_Z (\bar{M}_2^\top \bar{M}_2 + \bar{M}_1^\top \bar{W}_o \bar{M}_1) }
%	\end{equation}
% 	with 
%	\begin{eqnarray}
%		\bar{M}_1 &=& \begin{pmatrix}
%			B_2LJ^{-1} & 0 & B_2 \\
%			KJ^{-1} & I_n & 0
%			\end{pmatrix},  \\
%		\bar{M}_2 &=& \begin{pmatrix} D_{12}LJ^{-1} & 0 & D_{12} \end{pmatrix}
%	\end{eqnarray}
%
% 	and the matrix $d_Z$ is a diagonal matrix defined by
% 	\begin{equation}
% 		\pa{d_Z}_{i,i} \triangleq \text{number of non-trivial parameters in the i\textsuperscript{th} row of $Z$}
% 	\end{equation}
% 	The trivial parameters considered are $0$, $1$ and $-1$ because they do not imply a multiplication. 

%See also: <@FWR/RNG>, <@FWS/RNG_cl>

%References:
%	\cite{Hila08b} T.�Hilaire, P.�Chevrel, and J.�Whidborne. Finite wordlength controller realizations using the specialized implicit form. Technical Report RR-6759, INRIA, 2008.



