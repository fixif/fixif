%Purpose:
% Subscripted assign for FWS object.
% Here, "S.prop=value" is equivalent to 'set(S,"prop",value)'
%
%Syntax:
% S = subsasgn(S,Sub,value)
%
%Parameters:
% S: FWS object
% Sub: subassignment layers
% value: value of the assignation
%
% $Id: subsasgn.m 204 2009-01-05 09:39:04Z hilaire $


function S = subsasgn(S,Sub,value)

% Peel off first layer of subassignment
switch Sub(1).type
    case '.'
        % Assignment of the form R.fieldname(...)=value
        try
            if length(Sub)==1,
                FieldValue = value;
            else
                FieldValue = subsasgn( get(S,Sub(1).subs), Sub(2:end),value);
            end
            S = set( S, Sub(1).subs, FieldValue);
        catch
            rethrow(lasterror)
        end
    otherwise
        error ([ inputname(1) Sub.type '=value; is not valid'])
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

%See also: <@FWS/set>, <@FWS/get>, <@FWS/subsref>, <@FWR/subsasgn>