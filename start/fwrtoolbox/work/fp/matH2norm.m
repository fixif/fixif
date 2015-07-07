% efficient computation of the matrix of the sub H2 norms of a system
% (such M(i,j) = norm( Sys(i,j),2)
%
% M = matH2norm(Sys,method);
%
% M: matrix of the H2-norms
% Sys: ss object
% method : 'c' (default) to use the commandability grammian
%          or 'o' to use the observability grammian
%
% $Id$

function M = matH2norm(Sys, method)


% dimensions
p=size(Sys.C,1);
m=size(Sys.B,2);
n=size(Sys.A,1);
M = zeros(p,m);

% for i=1:p
%     for j=1:m
%         M(i,j) = norm( Sys(i,j) )^2;
%     end
% end

if method=='o'
    % observability grammians
    SWo = zeros(n,n,p);
    for i=1:p
        SWo(:,:,i) = dlyap( Sys.A', Sys.C(i,:)'*Sys.C(i,:) );
    end    
    %construction    
    for i=1:p
        M(i,:) = diag( Sys.B'*SWo(:,:,i)*Sys.B )';
    end
    M = M + Sys.D.*Sys.D;
else
    % controllability grammians        
    SWc = zeros(n,n,m);
    for j=1:m
        SWc(:,:,j) = dlyap( Sys.A, Sys.B(:,j)*Sys.B(:,j)' );
    end
    %construction
    for j=1:m
        M(:,j) = diag( Sys.C*SWc(:,:,j)*Sys.C' );
    end
    M = M + Sys.D.*Sys.D;
end


