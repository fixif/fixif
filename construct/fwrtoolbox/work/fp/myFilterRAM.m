function y = myFilterRAM( u)                         
                                                  
% initialize                                      
y=zeros( length(u), 1 );                          
xn=zeros(4,1);                                    
                                                  
for i=1:length(u)                                 
                                                  
    % intermediate variables                      
    Acc0 = xn(1) * 31457;                         
    Acc0 = Acc0 + floor( (u(i)  * 16771) / 2^15 );
    T0 = floor( Acc0/2^15 );                      
                                                  
    Acc1 = xn(2) * 31457;                         
    T1 = floor( Acc1/2^15 );                      
                                                  
    Acc2 = xn(3) * 31457;                         
    T2 = floor( Acc2/2^15 );                      
                                                  
    Acc3 = xn(4) * 31457;                         
    T3 = floor( Acc3/2^15 );                      
                                                  
                                                  
    % output(s)                                   
    Acc8 = (T0) * 2^16;                           
    y(i) = floor( Acc8/2^16 );                    
                                                  
                                                  
    % states                                      
    Acc4 = T0    * 23718;                         
    Acc4 = Acc4 + (T1) * 2^14;                    
    Acc4 = Acc4 + floor( (xn(1) * 26214) / 2^2 ); 
    Acc4 = Acc4 + floor( (u(i)  * 27079) / 2^14 );
    xn(1) = floor( Acc4/2^14 );                   
                                                  
    Acc5 = T0    * -19902;                        
    Acc5 = Acc5 + (T2) * 2^12;                    
    Acc5 = Acc5 + floor( (xn(2) * 32768) / 2^1 ); 
    Acc5 = Acc5 + floor( (u(i)  * 17481) / 2^11 );
    xn(2) = floor( Acc5/2^15 );                   
                                                  
    Acc6 = T0    * 21143;                         
    Acc6 = Acc6 + (T3) * 2^11;                    
    Acc6 = Acc6 + xn(3) * 19661;                  
    Acc6 = Acc6 + floor( (u(i)  * 21308) / 2^8 ); 
    xn(3) = floor( Acc6/2^15 );                   
                                                  
    Acc7 = floor( (T0    * -20939) / 2^1 );       
    Acc7 = Acc7 + xn(4) * 22938;                  
    Acc7 = Acc7 + floor( (u(i)  * 20615) / 2^5 ); 
    xn(4) = floor( Acc7/2^15 );                   
                                                  
end