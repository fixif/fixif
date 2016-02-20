%Purpose:
% Update the R value from the (new) paramsValue
%
%Syntax:
% [R, cost_flag] = updateR(S)
%
%Parameters:
% R: FWR object
% S: FWS object
%
% $Id: updateR.m 204 2009-01-05 09:39:04Z hilaire $


function [R, cost_flag] = updateR(S)

% are U,Y,W accessible ?
if isempty(S.UYWfun)
   [R, cost_flag] = feval( S.Rfun, S.Rini, getValues(S), S.dataFWS); 
else
    % compute U,Y,W from the params value
    [U,Y,W,cost_flag] = feval( S.UYWfun, S.Rini, getValues(S), S.dataFWS);
    
    % compute the new realization from the initial realization Rini
    if cost_flag
        R = transform( S.Rini, U,Y,W);
    else
        R = S.R;
    end
end

if ~isempty(S.Rini.FPIS)
	R = setFPIS(R, S.Rini.FPIS);
end


%Description:
% 	\begin{center}\I{Internal function}\end{center}
%	This function updates the \matlab{R} value from the (new)
%	parameters' values (\matlab{paramsValue}). This is done via the 
%	$\mt{U}$, $\mt{Y}$ and $\mt{W}$ matrices or directly, depending on
%	the FWS object and the \matlab{UYWfun} and \matlab{Runf}
%	functions.