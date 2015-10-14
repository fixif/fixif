%Purpose:
% Convert FWR object to double (return Z matrix)
%
%Syntax:
% d = double(R)
%
%Parameters:
% d: double
% R: FWR object
%
%Description:
% return the $Z$ matrix.
%
%See also: <@FWR/display>
%
%$Id: double.m 201 2009-01-03 22:31:50Z hilaire $


function d = double(R)

d = R.Z;