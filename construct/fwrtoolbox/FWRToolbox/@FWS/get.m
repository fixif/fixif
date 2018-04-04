%Purpose:
% Get some properties of a FWS object (or list the properties if propName is ignored)
%
%Syntax:
% value = get(S, propName)
%
%Parameters:
% value: value of the property
% S: FWS object
% propName : name of the property (string)
%
% $Id: get.m 204 2009-01-05 09:39:04Z hilaire $


function value = get( S, propName)

if nargin==1
    disp(struct(S))
else
    st=struct(S);
    try
        value = getfield(st,propName);
    catch
        try
            % find the property in the list
            [p num] = pnmatch( propName, S.paramsName);
        catch
                error ([ propName,' is not a valid property of ' inputname(1)]);
		end
		v = getValues(S);
        value = cell2mat( v(num));
    end
end

%Description:
%	This function is most of the time called by \funcName[@FWS/subsref]{subsref}.\\
%	All the fields are actually changeable (may change).

%See also: <@FWR/get>
