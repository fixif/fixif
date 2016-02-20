% random system
P=sysrand(6,1,1,1);
[Ac,Bc,Cc,Dc]=unpck(P);
Sc=ss(Ac,Bc,Cc,Dc);
S=c2d(Sc,1,'Tustin');
A=S.A; B=S.B; C=S.C; D=S.D;

% grammian
Wc=gram(S,'c');


T=rand(6); 


Ttilde=diag( sqrt(diag( inv(T)*Wc*inv(T)' )) );


TT=T*Ttilde;

%new system
Atilde=inv(TT)*A*TT; Btilde=inv(TT)*B; Ctilde=C*TT; Dtilde=D;
Stilde=ss(Atilde,Btilde,Ctilde,Dtilde,1);
Wctilde=gram(Stilde,'c');

diag(Wctilde)



