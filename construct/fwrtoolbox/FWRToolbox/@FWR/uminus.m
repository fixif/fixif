%Purpose:
% opposed FWR object 
%
%Syntax:
% R = -R
% R = uminus(R)
%
% $Id$


function R = uminus( R)

R.L = -R.L;
R.R = -R.R;
R.S = -R.S;

R = computeAZBZCZDZWcWo(R);
