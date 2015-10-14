%Purpose:
% Generic cost function for optimization of a FWS.
% Here the measure is computed direclty from the U,Y,W (and
% other values computed one time and stored in data) in order to decrease
% the computational time
% (in 'genCostFunctionR', it's computed from the new realization R)
%
%Syntax:
% [cost_value, cost_flag] = genCostFunctionS( S, x, freeparams, l2scaling, Umax, delta, measureFun, ...)
%
%Parameters:
% cost_value: value of the measure for parameter x
% cost_flag: 0 if parameter x is incorrect
%          : 1 otherwise
% S: FWS object
% x: vector of parameter used by optimiser (ASA, fminsearch, ...)
% freeparams: vector that indicates which parameters are free to be optimized
% l2scaling: boolean - tell if R is $L_2$-scaled
% Umax: magnitude value for the input - used for the $L_2$-scaling
% delta: delta parameter for $L_2$-scaling
% measureFun : handle of the measure function
% ...: the extra parameters are given to the measure function
%
%
% $Id: genCostFunctionS.m 256 2012-03-12 10:43:20Z hilaire $


function [cost_value, cost_flag] = genCostFunctionS( S, x, freeparams, l2scaling,Umax,delta, measureFun, varargin)

% transform x into the parameters of the FWS
S.paramsValue(freeparams) = x(1:length(freeparams));

% transform paramsValue into U,W,Y,cost_flag
[U,Y,W,cost_flag] = feval( S.UYWfun, S.Rini, getValues(S));

% a posteriori l2-scaling
if l2scaling==1
	[MU,MY,MW] = l2scaling(S.R);
    %MU = sqrt( diag(diag( inv(U)*S.Rini.Wc*inv(U)' )) );
	%MW = sqrt( diag(diag( inv(S.Rini.J)*(S.Rini.N*S.Rini.N' + S.Rini.M*S.Rini.Wc*S.Rini.M')*inv(S.Rini.J)' )) );
    U = U*MU;
    W = W*MW;
	Y = Y*MY;
elseif l2scaling==2
	%[MU,MY,MW] = speciall2scaling(S.R);
	[MU,MY,MW] = l2scaling(S.R, x( S.indices(end):S.Rini.l+S.Rini.n+S.indices(end)-1 ));
    U = U*MU;
    W = W*MW;
	Y = Y*MY;
elseif l2scaling==3
	[MU,MY,MW] = relaxedl2scaling( S.R, Umax, delta);
	U = U*MU;
    W = W*MW;
	Y = Y*MY;
end

% don't compute the new realization from the initial realization Rini (non
% usefull here because the measure is computed directly from U,W,Y (and
% other values computed one time and stored in data) in order to decrease
% the computational time
%%S.R = transform( S.Rini, U,Y,W);

% compute the measure
if cost_flag
    cost_value = feval( measureFun, S,U,Y,W, varargin{:} );
else
    cost_value = +Inf;    
end


%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function is a generic cost function. From the vector $x$, it
% 	rebuilds the matrices $\mt{U}$, $\mt{Y}$ and $\mt{W}$ (thanks to the \matlab{UYWfun} function) and then
% 	compute the associated cost value.\\
% 	In \funcName[@FWS/genCostFunctionS]{genCostFunctionS}, a new realization is directly computed from the parameters' value
%	(thanks to the \matlab{Rfun} function), and used to compute the cost value.

%See also: <@FWS/optim>, <@FWS/genCostFunction>, <@FWS/genCostFunctionR>