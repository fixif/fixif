% realize a fixed-point scalar product (the vector of coefficient 'P' by the vector of variables 'name')
% P(1)*name(1) + P(2)*name(2) + ... + P(n)*name(n)
% and write it in a file
%
% scalprodVHDL( file, P, name, gamma, shift, strAcc)
%
% file: file identifier
% P: vector of coefficients used in the scalar product
% name: name of the variables
% gamma: fractional part of the coefficients P
% shift: shift to apply after each multiplication
% strAcc: name of the accumulator
%
% $Id$

function scalprodVHDL( file, P, name, gamma, shift, strAcc)

tol=1e-10;
tabu = '    ';
nzP = find( abs(P)>tol );

for i=nzP
    if i==nzP(1)
        strAccPlus = '';
    else
        strAccPlus = [ strAcc ' + ' ];
    end
    
    if ( abs(P(i)-1)<tol )
        fwrite( file, [ tabu strAcc ' = ' strAccPlus shiftcode( name(i,:), shift(i) ) ';']);
    else
        fwrite( file, [ tabu strAcc ' = ' strAccPlus shiftcode( [ name(i,:) ' * ' num2str( round(P(i)*2^gamma(i)) ) ], shift(i)) ';' ]) ;
    end
    
end

return

function S = shiftcode( str, shift)

str=deblank(str);
if shift<0
    S = [ '(' str ') * 2^' num2str(-shift) ];
elseif shift==0
    S = str;
else
    S = [ '(' str ') / 2^' num2str(shift) ];
end
