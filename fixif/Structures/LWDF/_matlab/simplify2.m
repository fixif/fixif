function [R, counter] = simplify2(R)


l = R.l;
n = R.n;
Z = R.Z;

changes = 1;
counter = 0;
while changes
    [Z, l, n, changes] = simplify_Nastia(Z, l, n);
    counter = counter + changes;
end
R = Z2SIF(Z, l, n, R.p, R.m);
end

function [Z, l, n, changes] = simplify_Nastia(Z, l, n)
changes = 0;
i = 1;
while (i < l)
    %detect what rows have only two operands
    cols = find(Z(i,:)~=0);
    
   if(length(cols) == 1) %if we have a zero expression, e.g. t_i = 0
       Z(i,:) = [];
       Z(:,i) = [];
       l = l - 1;
       changes = 1;
   end
    
   if(length(cols) == 2) %if we have a simple expression, e.g. t_i = c * t_k
       j = cols(find(cols ~= i));   %index of the column whose value must be saved
       row_use_t = find(Z(:,i));    %rows that use the current variable
       row_use_t(find(row_use_t==i))=[]; %exclude the current row from that list
       Z(row_use_t, j) = sign(Z(row_use_t,i)) * Z(i,j);    %replace the value 
              
       Z(i,:) = [];
       Z(:,i) = [];
       l = l - 1;        
       changes = changes + 1;
   end
   
   i = i + 1;
end

end


function SIF = Z2SIF(Z, l, n, p, m)

J = - Z(1: l,1: l);
K =  Z( l+1: l+ n,1: l);
L =  Z( l+ n+1: l+ n+ p,1: l);
M =  Z(1: l, l+1: l+ n);
N =  Z(1: l, l+ n+1: l+ n+ m);
P =  Z( l+1: l+ n, l+1: l+ n);
Q =  Z( l+1: l+ n, l+ n+1: l+ n+ m);
R =  Z( l+ n+1: l+ n+ p, l+1: l+ n);
S =  Z( l+ n+1: l+ n+ p, l+ n+1: l+ n+ m);

SIF =  FWR(J,K,L,M,N,P,Q,R,S);
 
end




