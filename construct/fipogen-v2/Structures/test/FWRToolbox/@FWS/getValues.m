%Purpose:
% Return the parameters' value (cells of values)
%
%Syntax:
% v = getValues(S)
%
%Parameters:
% v: cells of values
% S: FWS object
%
% $Id: getValues.m 204 2009-01-05 09:39:04Z hilaire $


function v = getValues(S)

for i=1:length(S.paramsName)
	v{i} = reshape( S.paramsValue( S.indices(i):S.indices(i+1)-1 ), S.paramsSize(i,:) );
end

%Description:
%	This function returns the parameters value that are encapsuled in the \matlab{paramsValue} field.\\
%	It is used by UYWfunctions.

%See also: <@FWS/FWS>
