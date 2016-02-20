xn=zeros(1,4);
u=16000*ones(1,1000);
v=zeros(1,1000);
Tv=v;Txn=xn;

for i=1:1000
    
                                                                        
    % intermediate variables                                               
    Acc0= xn(1)* 15729;                                                    
    Acc0=Acc0+ dummy((u(i)    * 8386) /2^ 15);                                            
    T0= dummy(Acc0 /2^14);                                                         
                                                                            
    Acc1= xn(2)* 15729;                                                    
    T1= dummy(Acc1 /2^ 14);                                                         
                                                                            
    Acc2= xn(3)* 15729;                                                    
    T2= dummy(Acc2 /2^ 14);                                                         
                                                                            
    Acc3= xn(4)* 15729;                                                    
    T3= dummy(Acc3 / 2^ 14);                                                         
                                                                            
                                                                            
    % outpu(i)t(s)
    Acc8= (T0   ) *2^15;
    v(i)= dummy(Acc8 /2^15);                                                          
                                                                            
                                                                            
    % states                                                               
    Acc4= T0   * 11859;                                                    
    Acc4= Acc4+(T1   ) *2^13;                                                   
    Acc4= Acc4+dummy((xn(1)* 13107) /2^ 2);                                            
    Acc4= Acc4+dummy((u(i)    * 13539) /2^ 14);                                           
    xn(1)= dummy(Acc4 /2^ 13);                                                      
                                                                            
    Acc5= T0   * -9951;                                                    
    Acc5= Acc5+(T2   ) *2^11;                                                   
    Acc5= Acc5+dummy((xn(2)* 16384) /2^ 1);                                            
    Acc5= Acc5+dummy((u(i)    * 8741) /2^ 11);                                            
    xn(2)= dummy(Acc5 /2^ 14);                                                      
                                                                            
    Acc6= T0   * 10571;                                                    
    Acc6= Acc6+(T3   ) *2^10;                                                   
    Acc6= Acc6+xn(3)* 9830;                                                     
    Acc6= Acc6+dummy((u(i)    * 10654) /2^ 8);                                            
    xn(3)= dummy(Acc6 /2^ 14);                                                      
                                                                            
    Acc7= (T0   * -10470) /2^ 1;                                           
    Acc7= Acc7+xn(4)* 11469;                                                    
    Acc7= Acc7+dummy((u(i)    * 10308) /2^ 5);                                            
    xn(4)= dummy(Acc7 /2 ^ 14);                                                      
    
    
    TT0 = ( 15729*Txn(1) + (8386*u(i))/2^15 ) / 2^14;
    TT1 = ( 15729*Txn(2) ) / 2^14 ;
    TT2 = ( 15729*Txn(3) ) / 2^14 ;
    TT3 = ( 15729*Txn(4) ) / 2^14 ;
    
    Tv(i) = TT0;
    
    Txn(1) = ( TT0*11859 + (TT1*2^13) + (Txn(1)*13107)/2^2 + (u(i)*13539)/2^14 ) /2^13 ;
    Txn(2) = ( TT0*(-9951) + (TT2*2^11) + (Txn(2)*16384)/2^1 + (u(i)*8741)/2^11 ) /2^14;
    Txn(3) = ( TT0*10571 + (TT3*2^10) + (Txn(3)*9830) + (u(i)*10654)/2^8 ) / 2^14 ;
    Txn(4) = ( (TT0*(-10470))/2^1 + (Txn(4)*11469) + (u(i)*10308)/2^5 ) /2^14 ;
    
    
    
    
    
end


