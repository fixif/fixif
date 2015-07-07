%Purpose:
% Set some properties of a FWS object
%
%Syntax:
% S = set(S, propName, value)
%
%Parameters:
% S: FWR object
% propName : name of the property
% value : new value for this property
%
% $Id: set.m 208 2009-01-05 13:52:19Z fengyu $


function S = set( S, propName, value)

% check args
if nargin~=3
    error(['error....']);
end

% is it 'Rini' ?
if strcmpi( propName, 'Rini')
    % check the size and the type
    if isa(value,'FWR') & (size(value)==size(S.Rini))
        S.Rini = value;
        S.R = updateR(S);
    else
        error(['Cannot change the size of property ' propName]);
    end

% is it 'paramsName'    
elseif strcmpi( propName, 'paramsName')
    % check the size
    error('It is not possible (yet) to change paramsName');
    
% is it one of the parameters of the structuration ?    
else
    try
        [p num] = pnmatch( propName, S.paramsName);
    catch
        error(['The property ' propName ' cannot be changed or doesnt''t exist']);
    end
    
    % check the size
    if size(value) == S.paramsSize(num,:)
        S.paramsValue(S.indices(num):S.indices(num+1)-1) = value;
    else
        error(['Cannot change the size of property ' propName]);
    end
    
    % update R
    S.R = updateR(S);
end

% TODO : can we do better than use the 'eval' function ???

%Description:
% 	This function is most of the time called by \funcName[@FWS/subsasgn]{subsasgn}.\\
% 	The initial realization \matlab{Rini} can be changed (if the size doesn't change), so can the parameters of the structuration. It is not allowed to modified other fields.

%See also: <@FWS/get>, <@FWS/subsasgn>, <@FWR/set>



