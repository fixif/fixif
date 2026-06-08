%Purpose:
% Subscripted assign for FWR object
% here, 'R.prop=value' is equivalent to 'set(R,"prop",value)'
%
%Syntax:
% R = subsasgn(R,Sub,value)
%
%Parameters:
% R: FWR object
% Sub: subassignment layers
% value: value of the assignation
%
% $Id: subsasgn.m 201 2009-01-03 22:31:50Z hilaire $


function R = subsasgn(R,Sub,value)

% Peel off first layer of subassignment
switch Sub(1).type
    case '.'
        % Assignment of the form R.fieldname(...)=value
        try
            if length(Sub)==1,
                FieldValue = value;
            else
                FieldValue = subsasgn( get(R,Sub(1).subs), Sub(2:end),value);
            end
            R = set(R,Sub(1).subs,FieldValue);
        catch
            rethrow(lasterror)
        end
    otherwise
        error ([ inputname(1) Sub.type '=value; is not valid'])
end


%Description:
%	These functions are called internally when operators \matlab{[]}, \matlab{()}
%	and \matlab{.} are applied on a FWR object.\\
%	Only the operator \matlab{.} is valid, and links to \funcName[@FWR/set]{set} and \funcName[@FWR/get]{get}
%	functions. The command \matlab{R.field} returns the field \matlab{field} of \matlab{R}
%	(internally, \matlab{get(R,'field')} is called), and \matlab{R.field=vaue} set the field
%	\matlab{field} of \matlab{R}

%Example:
%	\matlab{R.P .* R.WP}\\
%	\matlab{R.P(1,:)}\\
%	\matlab{R.Z(3,3) = 0;}\\
%	\matlab{R.WZ = zeros( size(R.WZ) );}

%See also: <@FWR/set>, <@FWR/get>, <@FWR/subsref>, <@FWS/subsasgn>
