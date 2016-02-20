%Purpose:
% G	eneric cost function for optimization of a FWS
%
%Syntax:
% [cost_value, cost_flag] = genCostFunction( x, S, freeparams, isaFWSMethod, l2scaling,Umax,delta, measureFun, ...)
%
%Parameters:
% cost_value: value of the measure for parameter x
% cost_flag: 0 if parameter x is incorrect
%          : 1 otherwise
% x: vector of parameter used by optimization (ASA, fminsearch, ...)
% S: FWS object
% freeparams: vector that indicates which parameters are free to be optimized
% isaFWSMethod : boolean that indicates that if the measure is a FWS's method
% l2scaling: boolean - tell if R is $L_2$-scaled
% Umax: magnitude value for the input - used for the $L_2$-scaling
% delta: $\delta$ parameter for $L_2$-scaling
% measureFun : handle of the measure function
% ...: the extra parameters are given to the measure function
%
% $Id$


function [cost_value, cost_flag] = genCostFunction( x, S, freeparams, isaFWSMethod, l2scaling,Umax,delta, measureFun, varargin)

if isaFWSMethod
    [cost_value, cost_flag] = genCostFunctionS( S, x, freeparams, l2scaling,Umax,delta, measureFun, varargin{:});
else
    [cost_value, cost_flag] = genCostFunctionR( S, x, freeparams, l2scaling,Umax,delta, measureFun, varargin{:});
end


%Description:
%	This function is used internally only, \I{but} should be visible for fminsearch, ASA, ...\\
%	It just calls \matlab{genCostFunctionS} (or
%	\matlab{genCostFunctionR}) that are real FWS's methods (fminsearch or ASA needs a cost function with x as
%	first argument, but we wanted this function to be a FWS's method).

%See also: <@FWS/optim>, <@FWS/genCostFunctionR>, <@FWS/genCostFunctionS>