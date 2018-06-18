%Purpose:
% Set some properties of a FWR object
%
%Syntax:
% R = set(R, propName, value)
%
%Parameters:
% R: FWR object
% propName : name of the property
% value : new value for this property
%
% $Id: set.m 201 2009-01-03 22:31:50Z hilaire $


function R = set( R, propName, value)

% check args
if nargin~=3
    error(['error....']);
end

% list of properties that can be changed
Props = {   'J','K','L','M','N','P','Q','R','S','Z'};

% find the property in the list
num = find( strcmpi(propName, Props) );
if isempty(num)
    error(['The property ' propName ' cannot be changed  or doesnt''t exist']);
end

% change the value if propName is from 'J' to 'WZ'
if num<21 
    % check the size
    if eval(['size(R.' propName ')'])==size(value)
        eval(['R.' propName '=value;']);
    else
        error(['Cannot change the size of property ' propName]);
    end
    % compute appropriate parameters
    if num<10                                % 'J' to 'S'
        R = computeZ(R);
    elseif num==10                          % 'Z'
        R = computeJtoS(R);

    end
end


%Description:
% 	This function is most of the time called by \funcName[@FWR/subsasgn]{subsasgn}.\\
% 	The value of every field (\matlab{l}, \matlab{m}, \matlab{n} and \matlab{p} ; \matlab{J},
% 	\matlab{K}, \matlab{L}, \matlab{M}, \matlab{N}, \matlab{P}, \matlab{Q}, \matlab{R} and \matlab{S};
% 	\matlab{Z} ; \matlab{WJ}, \matlab{WK}, \matlab{WL}, \matlab{WM}, \matlab{WN}, \matlab{WP},
% 	\matlab{WQ}, \matlab{WR} and \matlab{WS}, \matlab{WZ}, \matlab{AZ}, \matlab{BZ}, \matlab{CZ}
% 	and \matlab{AZ}) can be evaluated, but \matlab{l}, \matlab{m}, \matlab{n}, \matlab{p}, 
% 	\matlab{AZ}, \matlab{BZ}, \matlab{CZ} and \matlab{AZ} cannot be modified.\\
% 	Changing \matlab{Z} changes fields \matlab{J} to \matlab{S}, and reciprocally (this is
% 	the same with \matlab{WZ}).

%See also: <@FWR/get>, <@FWR/subsasgn>, <@FWS/set>

% TODO: can we do better than use the 'eval' function ???



