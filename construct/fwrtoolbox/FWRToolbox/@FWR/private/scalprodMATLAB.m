%Purpose:
% Write the MATLAB code corresponding to a fixed-point scalar product
% (the vector of coefficient 'P' by the vector of variables 'name').
% Ex: P(1)*name(1) + P(2)*name(2) + ... + P(n)*name(n)
%
%Syntax:
% scalprodMATLAB( fiel, P, name, gamma, shift, strAcc)
%
%Parameters:
% file: file id, where the scalar product is written
% P: vector of coefficients used in the scalar product
% name: name of the variables
% gamma: fractional part of the coefficients P
% shift: shift to apply after each multiplication
% strAcc: name of the accumulator
%
%
% $Id$

function scalprodMATLAB( file, P, name, gamma, shift, strAcc)

tol=1e-10;
tabu = '    ';
nzP = find( abs(P)>tol );
endl=13;


for i=nzP
    if i==nzP(1)
        strAccPlus = '';
    else
        strAccPlus = [ strAcc ' + ' ];
    end
    
    coef = round(P(i)*2^gamma(i));
    if ( coef<=0 | abs(rem(log2(abs(coef)),1))>tol )
        fwrite( file, [ tabu strAcc ' = ' strAccPlus shiftcode( [ name(i,:) ' * ' num2str( coef ) ], shift(i)) ';' endl ]) ;
    else
        fwrite( file, [ tabu strAcc ' = ' strAccPlus shiftcode( name(i,:), shift(i)-log2(coef) ) ';' endl ]) ;
    end
    
end

%===================
% code for the shift
function S = shiftcode( str, shift)

str=deblank(str);
if shift<0
    S = [ '(' str ') * 2^' num2str(-shift) ];
elseif shift==0
    S = str;
else
    S = [ 'floor( (' str ') / 2^' num2str(shift) ' )'];
end



%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function is called by \funcName[@FWR/implementMATLAB]{implementMATLAB} for each scalar product to be done.\\
% 	It writes the corresponding MATLAB code in a file.\\
% 	\matlab{P} corresponds to the vector of coefficients to use, and \matlab{name} to the vector of variables' name to use. 

%See also: <@FWR/implementMATLAB>, <@FWR/scalprodCfloat>, <@FWR/scalprodVHDL>
