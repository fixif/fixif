%Purpose:
% Subscripted reference for FWS object.
% Here, "S.prop" is equivalent to "get(S,'prop')"
%
%Syntax:
% value = subsref(S,Sub)
%
%Parameters:
% value: returned value
% S: FWS object
% Sub: layers of subreferencing
%
% $Id: subsref.m 204 2009-01-05 09:39:04Z hilaire $



function value = subsref(S,Sub)

if nargin==1,
    value = S;
    return
end

% Peel off first layer of subreferencing
switch Sub(1).type
    case '.'
        % The first subreference is of the form R.fieldname
        % The output is a piece of one of the system properties
        try
            if length(Sub)==1,
                value = get( S, Sub(1).subs);
            else
                value = subsref( get( S, Sub(1).subs), Sub(2:end));
            end
        catch
            rethrow(lasterror)
        end
    otherwise
        error ([ inputname(1) Sub(1).type ' is not valid'])
end


%Description:
%	These functions are called internally when operators \matlab{[]}, \matlab{()}
%	and \matlab{.} are applied on a FWR object.\\
%	Only the operator \matlab{.} is valid, and links to \funcName[@FWS/set]{set} and \funcName[@FWS/get]{get}
%	functions. The command \matlab{S.field} returns the field \matlab{field} of \matlab{S}
%	(internally, \matlab{get(S,'field')} is called), and \matlab{S.field=vaue} set the field
%	\matlab{field} of \matlab{S}

%Example:
%	\matlab{S.Rini = R}\\
%	\matlab{S.R}\\
%	\matlab{S.R.Z(3,3) = 0;}\\
%	\matlab{S.Rini.WZ = zeros(n);}

%See also: <@FWS/set>, <@FWS/get>, <@FWS/subsasgn>, <@FWR/subsref>
