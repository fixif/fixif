function cl_essai(R,Plant)

% sizes
np = size(Plant.A,1);
m = size(Plant.C,1);
p = size(Plant.B,2);
l=R.l; m2=R.m; n=R.n; p2=R.p;
m1=m-m2;
p1=p-p2;
if ( (p1<0) | (m1<=0) )
    error('dimension error - check plant and realization dimension');
end


% plant matrices
B1 = Plant.B(:,1:p1);
B2 = Plant.B(:,p1+1:p);
C1 = Plant.C(1:m1,:);
C2 = Plant.C(m1+1:m,:);
D11 = Plant.D(1:p1,1:m1);
D12 = Plant.D(1:p1,m1+1:m);
D21 = Plant.D(p1+1:p,1:m1);
D22 = Plant.D(p1+1:p,m1+1:m);
if (D22~=zeros(size(D22)))
    error('D22 needs to be null')
end

% closedloop related matrices
Abar = [ Plant.A + B2*R.DZ*C2 B2*R.CZ;
         R.BZ*C2 R.AZ];
Bbar = [ B1 + B2*R.DZ*D21; R.BZ*D21 ];
Cbar = [ C1 + D12*R.DZ*C2 D12*R.CZ ];
Dbar = D11 + D12*R.DZ*D21;

% intermediate matrices
M1bar = [ B2*R.L*inv(R.J) zeros(np,n) B2;
          R.K*inv(R.J) eye(n) zeros(n,p2) ];
M2bar = [ D12*R.L*inv(R.J) zeros(m1,R.n) D12 ];      
N1bar = [ inv(R.J)*R.N*C2 inv(R.J)*R.M;
          zeros(n,np) eye(n);
          C2 zeros(m2,n) ];
N2bar = [ inv(R.J)*R.N*D21; zeros(R.n,p1); D21 ];




eig(Abar)