%Purpose:
% Write the VHDL code corresponding to a fixed-point scalar product
% (the vector of coefficient 'P' by the vector of variables 'name').
% Ex: P(1)*name(1) + P(2)*name(2) + ... + P(n)*name(n)
%
%Syntax:
% S = scalprodVHDL( file, P, name, gamma, shift, strAcc)
%
%Parameters:
%S: returned string
% P: vector of coefficients used in the scalar product
% name: name of the variables
% gamma: fractional part of the coefficients P
% shift: shift to apply after each multiplication
% finalshift: shift to apply at the end
%
% $Id$

function S = scalprodVHDL( P, name, gamma, shift, finalshift)

tol=1e-10;
tabu = '    ';
endl = 13;
nzP = find( abs(P)>tol );
S = '    ';
for i=nzP
    
    coef = round(P(i)*2^gamma(i));
    if ( coef<=0 | abs(rem(log2(abs(coef)),1))>tol )
        %fwrite( file, [ tabu strAcc ' = ' strAccPlus shiftcode( [ name(i,:) ' * ' num2str( coef ) ], shift(i)) ';' endl ]) ;
        S = [ S shiftcode( [ name(i,:) ' * ' strSign(coef) ], shift(i), 1) ];
    else
        %fwrite( file, [ tabu strAcc ' = ' strAccPlus shiftcode( name(i,:), shift(i)-log2(coef) ) ';' endl ]) ;
        S = [ S shiftcode( name(i,:), shift(i)-log2(coef), 0 ) ];
    end
    

    % is it the last non-zero parameter ?
    if ( i~= max(nzP) )
        S = [S ' + '];
    end

end

S = shiftcode( S, finalshift, 1);

return




%=================
function S = shiftcode( str, shift, parenthesis)

if parenthesis
    po='('; pc=')';
else
    po=''; pc='';
end

str=deblank(str);
if shift<0
    S = [ po str pc ' * 2**' num2str(-shift) ];
elseif shift==0
    S = str;
else
    S = [ po str pc ' / 2**' num2str(shift) ];
end


%=======================
function S = strSign( i)
if i>0
    S = num2str(i);
else
    S = [ '(' num2str(i) ')' ];
end




%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	This function is called by \funcName[@FWR/implementVHDL]{implementVHDL} for each scalar product to be done.\\
% 	It writes the corresponding VHDL code in a file.\\
% 	\matlab{P} corresponds to the vector of coefficients to use, and \matlab{name} to the vector of variables' name to use. 

%See also: <@FWR/implementVHDL>, <@FWR/scalprodCfloat>, <@FWR/scalprodMATLAB>