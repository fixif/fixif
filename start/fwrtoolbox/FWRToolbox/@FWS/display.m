%Purpose:
% Display the realization (dimensions, $Z$ and the parameters)
%
%Syntax:
% display(S)
%
%Parameters:
% S: FWS object
%
% $Id: display.m 204 2009-01-05 09:39:04Z hilaire $


function display(S)

display(S.R);
v=getValues(S);
for i=1:length(S.paramsName)
    disp( [ S.paramsName{i} '=' ] );	
    disp( cell2mat(v(i)) );
end


%Description:
% 	Display the dimensions (inputs, outputs, states and intermediate variables), $Z$ and the associated parameters.
% 
%Example:
% 	\begin{verbatim}
% 	 has 1 input, 1 output, 3 states, and 0 intermediate variable.
% 	Z=
% 	   5.5298e-01  -5.3793e-01   2.9172e-02   6.7157e-01
% 	   5.3793e-01   9.7113e-02  -3.5628e-01  -3.2376e-01
% 	   2.9172e-02   3.5628e-01  -7.2857e-02   7.9289e-02
% 	   6.7157e-01   3.2376e-01   7.9289e-02   9.8531e-02
% 
% 	T=
% 		 1     0     0
% 		 0     1     0
% 		 0     0     1
% 	\end{verbatim}

%See also: <@FWR/display>