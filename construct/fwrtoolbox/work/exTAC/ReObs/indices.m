
function [poles, ind_com, ind_obs, Umult]=indices(sys,reg)

n=size(sys.A,1);    % taille du système ou du régulateur 
nq=size(reg.A,1)-n; % diféérence entre sys et régulateur
nt=2*n+nq;          % taille de la BF
tab=[1:nt];

% matrice dynamique de la boucle fermée (t=0)
Atild = [sys.A + sys.B*reg.D*sys.C sys.B*reg.C ; reg.B*sys.C reg.A];
Btild = blkdiag(sys.B,eye(n+nq));
Ctild = blkdiag(sys.C,eye(n+nq));

% calcul des coef de commandabilié /observabilité
[Dcl,Vcl]=eig(Atild);
lambda=(eig(Atild));
B=inv(Dcl)*Btild;
C=Ctild*(Dcl);

for i=1:2*n+nq
    c(i)=norm(B(i,:));    
end  
for i=1:2*n+nq
    o(i)=norm(C(:,i));    
end  


[Dcl,Vcl]=cdf2rdf(Dcl,Vcl);
P=Dcl.*(inv(Dcl)');

for i=1:2*n+nq
    p(i)=sum(abs(P(:,i)));    
end  
for i=1:2*n+nq
    at(i)=real(lambda(i));    
end  

mult(1:2*n+nq)=0; %%%%multiplicité
for i=1:2*n+nq
    for j=1:2*n+nq
        if abs(lambda(i)-lambda(j))<1e-4  %%important peut etre vu comme parametre 
            mult(i)=mult(i)-1;
       end    
    end
end  

%ici on tri les poles suivant leurs commandabilité et observabilité (voir rapport page 100)
vp.num=1:2*n+nq;
vp.val=lambda;
vp.com=tri(c);
vp.obs=tri(o);
vp.par=tri(p);
vp.att=tri(at);
vp.mult=tri(mult);


%%%%%%%%ensemble des valeurs propres multiples ou quasi multiples
k=1;
for i=1:2*n
    if(mult(vp.mult(i))<-1)
        Umult.num(k)=vp.mult(i);
        k=k+1;
    end
end 

%X1=vp.val(setdiff(vp.com,Umult.num));
X1=vp.val(vp.com);

for l=1:size(X1,1)
    NUM(l)=find(lambda==X1(l));
    COM(l)=find(vp.com==find(lambda==X1(l)));
end    

% [X1 NUM' COM']

poles=lambda;
ind_com=c';
ind_obs=o';



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

