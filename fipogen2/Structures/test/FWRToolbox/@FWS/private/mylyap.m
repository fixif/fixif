%Purpose:
% Solve the continuous-time Lyapunov equations
% adapted from 'lyap.m' (S.N. Bangert The MathWorks, Inc.)
%
%Syntax:
% X = mylyap(A, B, C, ua, ta)
%
%Parameters:
% X: solution of the continuous-time Lyapunov equation
% A,B,C: parameters of the equation
% ua,ta: precomputed values
%
%% $Id$


function X = mylyap(A, B, C, ua, ta)
%LYAP  Solve continuous-time Lyapunov equations.
% adapted from lyap.m (S.N. Bangert The MathWorks, Inc.)

[ma,na] = size(A);
[mb,nb] = size(B);
[mc,nc] = size(C);


% Schur decomposition of A' can be calculated from that of A.
j = ma:-1:1;
ub = ua(:,j);
tb = ta(j,j)';


% Check all combinations of ta(i,i)+tb(j,j) for zero
p1 = diag(ta).'; % Use .' instead of ' in case A and B are not real
p1 = p1(ones(mb,1),:);
p2 = diag(tb);
p2 = p2(:,ones(ma,1));
sum = abs(p1) + abs(p2);
if any(any(sum == 0)) | any(any(abs(p1 + p2) < 1000*eps*sum))
   error('Solution does not exist or is not unique.');
end

% Transform C
ucu = -ua'*C*ub;

% Solve for first column of transformed solution
y = zeros(ma,mb);
ema = eye(ma);
y(:,1) = (ta+ema*tb(1,1))\ucu(:,1);

% Solve for remaining columns of transformed solution
for k=2:mb,
   km1 = 1:(k-1);
   y(:,k) = (ta+ema*tb(k,k))\(ucu(:,k)-y(:,km1)*tb(km1,k));
end

% Find untransformed solution 
X = ua*y*ub';

% Ignore complex part if real inputs (better be small)
if isreal(A) & isreal(B) & isreal(C),
   X = real(X);
end

% Force X to be symmetric if ni==2 and C is symmetric
if isequal(C,C'),
   X = (X+X')/2;
end
% end lyap


%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function executes the same algorithm described in \matlab{lyap.m} (S.N. Bangert The MathWorks, Inc.), except
% 	that the values \matlab{ua} and \matlab{ta} are already computed. It permits to save some computational time when a lot of
% 	Lyapunov equations have to be solved with the same value $A$.

%See also: <@FWR/w_prod_norm_SISO>

