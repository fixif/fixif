p=10;n=30;
R=30

t1=0;
for i=1:R
    A=rand(n,n); B=rand(n,p);
    tic;
    W=dlyap(A,B*B');
    t1 = t1+toc;
end
t1 = t1/R

In=eye(n);
WA = sparse(dlyap( kron(In,A), In(:)*(In(:))' ));
In=sparse(eye(n));
t2=0;
for i=1:R
    tic;
    toto = kron( B(:)',In) * kron(eye(p),WA) * kron( B(:),In);
    t2 = t2+toc;
end
t2 = t2/R