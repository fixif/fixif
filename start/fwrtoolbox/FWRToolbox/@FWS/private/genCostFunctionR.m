%Purpose:
% Generic cost function for optimization of a FWS.
% Here the measure is computed from the new realization R
%
%Syntax:
% [cost_value, cost_flag] = genCostFunctionR( S, x, freeparams, l2scaling, Umax, delta, measureFun, ...)
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
% $Id: genCostFunctionR.m 13 2007-01-19 22:13:51Z hilaire $


function [cost_value, cost_flag] = genCostFunctionR( S, x, freeparams, l2scaled,Umax,delta, measureFun, varargin)

% transform x into the parameters of the FWS
S.paramsValue(freeparams) = x(1:length(freeparams));

% update R
[S.R, cost_flag] = updateR(S);

% a posteriori l2-scaling
if cost_flag
    if l2scaled==1
        S.R = l2scaling(S.R);
    	%disp('l2scaling');
    elseif l2scaled==2
        S.R = l2scaling(S.R, x( S.indices(end):S.Rini.l+S.Rini.n+S.indices(end)-1 ));
    elseif l2scaled==3
        S.R = relaxedl2scaling( S.R, Umax, delta);
    end
end

% compute the measure
if cost_flag
    cost_value = feval( measureFun, S.R, varargin{:} );
else
    cost_value = +Inf;
end


%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function is a generic cost function. From the vector $x$, it rebuilds the parameters' value, a new realization 
% 	(with the \funcName[@FWS/updateR]{updateR} method), and then compute the associated cost value.\\
% 	In \funcName[@FWS/genCostFunctionS]{genCostFunctionS}, a new realization is not directly computed, only the $\mt{U}$, $\mt{Y}$ and $\mt{W}$
% 	matrices are used to compute the cost value.

%See also: <@FWS/optim>, <@FWS/genCostFunction>, <@FWS/genCostFunctionS>, <@FWS/updateR>
