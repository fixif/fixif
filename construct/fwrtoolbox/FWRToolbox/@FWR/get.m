%Purpose:
% Get some properties of a FWR object
% (or list the properties if 'propName' is ignored)
%
%Syntax:
% value = get(R, propName)
%
%Parameters:
% value: value of the property
% R: FWR object
% propName : name of the property (string)
%
% $Id: get.m 201 2009-01-03 22:31:50Z hilaire $


function value = get( R, propName)

if nargin==1
    disp(struct(R))
else
    st=struct(R);
    try
        value = getfield(st,propName);
    catch
        error ([ propName,' is not a valid property of ' inputname(1)]);
    end
end


%Description:
%	This function is most of the time called by \funcName{@FWR/subsref}.\\
%	The value of every field (\matlab{l}, \matlab{m}, \matlab{n} and \matlab{p} ; \matlab{J},
%	\matlab{K}, \matlab{L}, \matlab{M}, \matlab{N}, \matlab{P}, \matlab{Q}, \matlab{R} and \matlab{S};
%	\matlab{Z} ; \matlab{WJ}, \matlab{WK}, \matlab{WL}, \matlab{WM}, \matlab{WN}, \matlab{WP},
%	\matlab{WQ}, \matlab{WR} and \matlab{WS} ;	\matlab{WZ} ; \matlab{AZ}, \matlab{BZ}, \matlab{CZ}
%	and \matlab{AZ}) can be evaluated with this command, but \matlab{l}, \matlab{m}, \matlab{n}, \matlab{p}, 
%	\matlab{AZ}, \matlab{BZ}, \matlab{CZ} and \matlab{AZ} cannot be modified.\\
%	Changing \matlab{Z} changes fields \matlab{J} to \matlab{S}, and reciprocally (this is
%	the same with \matlab{WZ}).

%See also: <@FWR/set>, <@FWR/subsref>, <@FWR/subsasgn>, <@FWS/get>
