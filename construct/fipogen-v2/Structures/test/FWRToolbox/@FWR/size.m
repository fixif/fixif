%Purpose:
% Return the size of the FW Realization
%
%Syntax:
% lmnp = size(R)
% [l,m,n,p] = size(R)
%
%Parameters:
% lmnp: vector [l,m,n,p]
% l: nb of intermediate variables
% m: nb of inputs
% n: nb of states
% p: nb of outputs
% R: FWR object
%
% $Id: size.m 201 2009-01-03 22:31:50Z hilaire $


function [lmnp,m,n,p] = size(R)

if nargout<2
    lmnp = [ R.l R.m R.n R.p ];
else
    lmnp = R.l;
    m = R.m;
    n = R.n;
    p = R.p;
end


%Description:
%	Overload of the classical \matlab{size} function.