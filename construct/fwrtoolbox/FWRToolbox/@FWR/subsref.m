%Purpose:
% Subscripted reference for FWR object
% here, R.prop is equivalent to get(R,'prop')
%
%Syntax:
% value = subsref(R,Sub)
%
%Parameters:
% value: returned value
% R: FWR object
% Sub: layers of subreferencing
%
% $Id: subsref.m 201 2009-01-03 22:31:50Z hilaire $

function value = subsref(R,Sub)

if nargin==1,
   value = R;
   return
end

% Peel off first layer of subreferencing
switch Sub(1).type
    case '.'
        % The first subreference is of the form R.fieldname
        % The output is a piece of one of the system properties
        try
            if length(Sub)==1,
                value = get( R, Sub(1).subs);
            else
                value = subsref( get( R, Sub(1).subs), Sub(2:end));
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
%	Only the operator \matlab{.} is valid, and links to \funcName[@FWR/set]{set} and \funcName[@FWR/get]{get}
%	functions. The command \matlab{R.field} returns the field \matlab{field} of \matlab{R}
%	(internally, \matlab{get(R,'field')} is called), and \matlab{R.field=vaue} set the field
%	\matlab{field} of \matlab{R}

%Example:
%	\matlab{R.P .* R.WP}\\
%	\matlab{R.P(1,:)}\\
%	\matlab{R.Z(3,3) = 0;}\\
%	\matlab{R.WZ = zeros( size(R.WZ) );}

%See also: <@FWR/set>, <@FWR/get>, <@FWR/subsasgn>, <@FWS/subsref>
