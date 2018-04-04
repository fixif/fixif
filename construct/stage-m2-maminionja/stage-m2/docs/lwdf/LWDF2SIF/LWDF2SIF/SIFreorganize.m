function SIF = SIFreorganize(SIF, porder)
%The function SIFreorganize, if matrix J is not lower triangular, permutes 
%rows of matricex J,K,L and columns of M,N following order given in the
%input vector porder.
%ATTENTION: SIF is recreated, which would mean that other properties of SIF
%apart from its matrix Z are lost!

if istril(SIF.J) == 1
    return
end


nt = SIF.l;
nx = SIF.n;
nu = SIF.m;
ny = SIF.p;

Jsparse = sparse(SIF.J);
Ksparse = sparse(SIF.K);
Lsparse = sparse(SIF.L);
Msparse = sparse(SIF.M);
Nsparse = sparse(SIF.N);

%rows of matrix J

[row, col, val] = find(Jsparse);
n = length(row);
J = eye(nt,nt);
for i=1:n
    old_i = row(i);
    old_j = col(i);
    
    new_i = find(porder==old_i);
    new_j = find(porder==old_j);
    
    J(new_i, new_j) = val(i);
end  
       
%columns of matrix K
K = zeros(nx, nt);
[row, col, val] = find(Ksparse);
n = length(row);
if n~= 0
    for i=1:n
        old_j = col(i);
        old_i = row(i);

        new_j = find(porder==old_j);

        K(old_i, new_j) = val(i);
    end  
end

%columns of matrix L
L = zeros(ny, nt);
[row, col, val] = find(Lsparse);
n = length(row);
if n~= 0
    for i=1:n
        old_j = col(i);
        old_i = row(i);

        new_j = find(porder==old_j);

        L(old_i, new_j) = val(i);
    end  
end

%rows of matrix M
M = zeros(nt, nx);
[row, col, val] = find(Msparse);
n = length(row);
if n~= 0
    for i=1:n
        old_i = row(i);
        old_j = col(i);
        
        new_i = find(porder==old_i);

        M(new_i, old_j) = val(i);
    end  
end

%rows of matrix N
N = zeros(nt, nu);
[row, col, val] = find(Nsparse);
n = length(row);
if n~= 0
    for i=1:n
        old_i = row(i);
        old_j = col(i);
        
        new_i = find(porder==old_i);

        N(new_i, old_j) = val(i);
    end  
end

%ATTENTION: SIF is recreated, which would mean that other properties of SIF
%apart from its matrix Z are lost!

SIF = FWR(J, K, L, M, N, SIF.P, SIF.Q, SIF.R, SIF.S, 'fixed', 'natural');


end

