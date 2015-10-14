%Purpose:
% Display the realization (dimensions and Z)
%
%Syntax:
% display(R)
%
%Parameters:
% R: FWR object
%
% $Id: display.m 201 2009-01-03 22:31:50Z hilaire $


function display(R)

st = [inputname(1),' has'];
st = strcat( st, [' ' num2str(R.m) ' input' plural(R.m) ', ']);
st = strcat( st, [' ' num2str(R.p) ' output' plural(R.p) ', ']);
st = strcat( st, [' ' num2str(R.n) ' state' plural(R.n) ', ']);
st = strcat( st, [' and ' num2str(R.l) ' intermediate variable' plural(R.l) '.']);
disp(st);
if (R.fp~=1) | (R.block~=2)
    fp={'fixed point','floating point'};
    block={'with full blocks','with natural blocks','whitout blocks'};
    disp( ['Coding used : ' fp{R.fp} ' ' block{R.block}] );
end
disp( 'Z=');
disp( R.Z);

return


% add s if necessesary
function s=plural(n)

if n>1
    s='s';
else
    s='';
end


%Description:
% 	Display the dimensions (inputs, outputs, states and intermediate variables) and $Z$.
%Example:
% 	\begin{verbatim}
% 		R has 1 input, 1 output, 4 states, and 0 intermediate variable.
% 		3.5897e+00  -1.2128e+00   3.6551e-01  -1.6575e-01   1.5625e-02 
% 		4.0000e+00            0            0            0            0 
% 		0		2.0000e+00            0            0            0 
% 	  0            0   5.0000e-01            0            0 
% 	  1.5174e-02   5.7416e-04   1.7304e-03   1.6844e-04   3.1239e-05 
% 	\end{verbatim}

%See also: <@FWS/display>
