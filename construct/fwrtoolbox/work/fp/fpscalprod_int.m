function S = fpscalprod_int( P, name, beta, gamma, shift, strAcc)

tol=1e-10;
tabu = '    ';
S=[];
nzP = find( abs(P)>tol );

for i=nzP
    if ( abs(P(i))>tol)
        
        if ( abs(P(i)-1)<tol )
            S = strvcat(S, [ tabu strAcc '+= ' shiftcode(name(i,:), shift(i)) ';']);
        else
            S = strvcat(S, [ tabu strAcc '+= ' ...
                                shiftcode( ...
                                    [ name(i,:) '* ' num2str( round(P(i)*2^gamma(i)) ) ],...
                                    shift(i))...
                                ';' ]) ;
        end
       
    end
end




function S = shiftcode( str, shift)

if shift<0
    S = [ '(' str ') *2^' num2str(-shift) ];
elseif shift==0
    S = str;
else
    S = [ '(' str ') /2^ ' num2str(shift) ];
end