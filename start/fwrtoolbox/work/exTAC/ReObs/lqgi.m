

function [Kc, Kf,Q,M,reg_lqg]=lqgi(indice,sys,reg)

tol=10^-6;


[ac,bc,cc,dc]=ssdata(reg);
[A,B2,C2,D22]=ssdata(sys);
n=size(A,1);nk=size(ac,1);ntot=n+nk;
[acd,bcd,ccd,dcd]=feedback(ac,bc,cc,dc,[],[],[],-D22);
[abf,bbf,cbf,dbf]=feedback(A,B2,C2,0*D22,acd,bcd,ccd,dcd,1);

[V,D]=eig(abf);
lesvp=diag(D);

vpG=eig(A);

indice2=[indice,setdiff([1:ntot],indice)];

M=V(:,indice2);
D=D(indice2,indice2);
%[M,D]=cdf2rdf(M,real(D));
[M,D]=cdf2rdf(M,D);

%%%%%%%%calcul des structures LQG

nbo=size(A,1);
nbf=length(lesvp);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

T=real(M(nbo+1:nbf,1:nbo)*inv(M(1:nbo,1:nbo)));

F=acd-T*B2*ccd;
G=bcd-T*B2*dcd;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%
U=real(T*M(1:nbo,n+1:nbf)-M(nbo+1:nbf,nbo+1:nbf));
U1=U(:,1:nbf-2*nbo);
Um1=inv(U);
U1t=Um1(1:nbf-2*nbo,:);
U2t=Um1(nbf-2*nbo+1:nbf-nbo,:);

Gtilde1=U1t*G;
Gtilde2=U2t*G;
Ttilde1=U1t*T;
Ttilde2=U2t*T;

Kf=inv(Ttilde2)*Gtilde2;
Kc=-ccd*T-dcd*C2;
AQ=real(D(nbo+1:nbf-nbo,nbo+1:nbf-nbo));
BQ=Gtilde1-Ttilde1*inv(Ttilde2)*Gtilde2;
CQ=ccd*U1;
DQ=dcd;

Q=pck(AQ,BQ,CQ,DQ);
  
% matrice de passage finale:
M=[T U1];


[A,B,C,D]=ssdata(sys);
[p,m]=size(D);
SYS_K=pck([A-B*Kc-Kf*C+Kf*D*Kc],[Kf B-Kf*D],[-Kc;-C+D*Kc],...
         [0*ones(m,p) eye(m,m);eye(p,p) -D]);
reg_lqg=starp(SYS_K,Q);

