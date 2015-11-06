%Purpose:
% Numerically compute the outputs, states and intermediate variables with a given input U.
% Floating-point is used for the computations.
%
%Syntax:
% [Y, X, T] = realize( R, U, X0)
%
%Parameters:
% Y: outputs
% X: states
% T: intermediate variables
% R: FWR object
% U: inputs
% X0: initial states (default=0)
%
% $Id$


function [Y, X, T] = realize( R, U, X0)

% check dimensions
if size(U,1)==R.m
    N = size(U,2);
elseif size(U,2)==R.m
    N = size(U,1);
    U=U';
else
    error(['U must be a (' num2str(R.m) 'xN) matrix']);
end

% args
if nargin<3
    X0 = zeros(R.n,1);
end

% initial state
T = zeros(R.l,N+1);
X = zeros(R.n,N+1);
Y = zeros(R.p,N);
X(:,1) = zeros(R.n,1);

% use lsim with system H6
H6 = ss(R.AZ,R.BZ, [ inv(R.J)*R.M ; eye(R.n); R.CZ ], [inv(R.J)*R.N; zeros(R.n,R.m); R.DZ],1);
dummy = lsim( H6, U, [], X0 );
Y = dummy(:,R.n+R.l+1:end);
X = dummy(:,R.l+1:R.l+R.n);
T = dummy(:,1:R.l);


%Description:
%	This function could be useful to evaluate the magnitude values of the intermediate variables and the states.\\
%	It could also be useful to compare two different realizations, for example a realization and its quantized one.\\
%	It is important to notice that the computations are done in floating-point (the fixed-point implementation is not considered here).
