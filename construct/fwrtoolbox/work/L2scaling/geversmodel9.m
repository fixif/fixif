%GEVERSMODEL9
% model for Gevers , Li controller in Chpter 9
%

function [G,K,Abar]=geversmodel9

Ag=[ 3.7156, -5.4143 , 3.6525 , -0.9642;
     1.000 , 0 , 0 , 0;
     0 , 1.000 , 0 , 0;
     0 , 0 , 1.000 , 0];
Bg=[1 , 0 , 0 , 0]';
Cg=[0.1116 , 0.0043 , 0.1088 , 0.0014]*1e-5;
Dg=0;

G=ss(Ag,Bg,Cg,Dg,-1);
G=canon(G,'modal');

P1=[0.9844+0.0357*j;
    0.9844-0.0357*j;
    0.9643+0.0145*j;
    0.9643-0.0145*j];
 
 P2=[0.7152+0.6348*j;
    0.7152-0.6348*j;
    0.3522+0.2857*j;
    0.3522-0.2857*j];
 
 Ck=place(Ag,Bg,P1);
 Bk=place(Ag',Cg',P2)';
 Ak=Ag-Bg*Ck-Bk*Cg;
 Ck=-Ck;

Dk=0;

K=ss(Ak,Bk,Ck,Dk,-1);


% closed loop system matrix
if nargout==3,
   Abar=[Ag+Bg*Dk*Cg, Bg*Ck;
         Bk*Cg,       Ak  ];
end

return
