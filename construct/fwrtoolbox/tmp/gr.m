n=40;
m=5;
p=5;

N=1;
t1=zeros(1,N);
t2=t1;
for k=1:N


% random stable system
[Ac,Bc,Cc,Dc] = unpck( sysrand(n,m,p,1) );
Sc = ss(Ac,Bc,Cc,Dc);
S = c2d(Sc,1,'Tustin');
[A,B,C,D] = ssdata(S);


% method 1
M1=zeros(p,m);
tic
for j=1:m
	Wj = dlyap( A, B(:,j)*B(:,j)' );
	huhu = C*Wj*C';
	for i=1:p
		M1(i,j) = D(i,j)^2 + huhu(i,i); 
		%M1(i,j) = norm( S(i,j) )^2;
	end
end
t1(k)=toc;

% method 2
In=eye(n);

dXdX=In(:)*(In(:))';
superK = dlyap( kron(In,A), dXdX);

tic
for j=1:m
	Wj = kron( B(:,j)', In ) * superK * kron( B(:,j), In );
	huhu = C*Wj*C';
	for i=1:p
		M2(i,j) = D(i,j)^2 + huhu(i,i);
	end
	
end
t2(k)=toc;

end