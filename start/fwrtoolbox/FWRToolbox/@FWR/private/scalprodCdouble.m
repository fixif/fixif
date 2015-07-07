%Purpose:
% Return the C-code corresponding to a double floating-point scalar product
% (the vector of coefficient 'P' by the vector of variables 'name').
% Ex: P(1)*name(1) + P(2)*name(2) + ... + P(n)*name(n)
%
%Syntax:
% S = scalprodCdouble(  P, name)
%
%Parameters:
% S: returned string
% P: vector of coefficients used in the scalar product
% name: name of the variables
%
%
% $Id$


function S = scalprodCdouble( P, name)

tol = 1e-10;
endl = 13;

S=[];
nzP = find( abs(P)>tol );

for i=nzP
    if ( abs(P(i))>tol)
        
        if ( abs(P(i)-1)<tol )
            S = [ S name(i,:) ];
        elseif ( abs(P(i)+1)<tol )
            S = [ S '-' name(i,:) ];
        else
            %S = [ S num2str(P(i),'%.255g') '*' name(i,:) ];
            S = [ S num2str(P(i),'%.6g') '*' name(i,:) ];
        end
        % is it the last non-zero parameter ?
        if ( i~= max(nzP) )
            S = [S '\' endl ' + '];
        end
    end
end

if isempty(S)
	S='0';
end



%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function is called by \funcName[@FWR/algorithmCdouble]{algorithmCdouble} for each scalar product to be done.\\
% 	It returns the C-code corresponding.\\
% 	\matlab{P} correspond to the vector of coefficients to use, and \matlab{name} to the vector of variables' name to use. 

%See also: <@FWR/algorithmCdouble>, <@FWR/scalprodVHDL>, <@FWR/scalprodMATLAB>