function S = scalprod( P, name)

tol=1e-10;

S=[];
nzP = find( abs(P)>tol );

for i=nzP
    if ( abs(P(i))>tol)
        
        if ( abs(P(i)-1)<tol )
            S = [ S name(i,:) ];
        elseif ( abs(P(i)+1)<tol )
            S = [ S '-' name(i,:) ];
        else
            S = [ S num2str(P(i),'%.10f') '*' name(i,:) ];
        end
        % is it the last non-zero parameter ?
        if ( i~= max(nzP) )
            S = [S ' + '];
        end
    end
end