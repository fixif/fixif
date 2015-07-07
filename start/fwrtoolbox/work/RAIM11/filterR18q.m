%Purpose:
% Fixed-point algorithm in Matlab language
% (it uses integer to simulate fixed-point)
%
%Syntax:
% y = filterR18q(u)
%
%Parameters:
% y: filtered output(s)
% u: intput(s)
%
% date: 07-Feb-2011 00:04:31
% Automatically generated by implementMATLAB / FWRToolbox


function y = filterR18q(u)

% initialize                   
u = round(2.^3.*u);
y = zeros( size(u,1), 1 );
xn = zeros(6,1);
                
                               
for i=1:size(u,1)


    % intermediate variables
    Acc0 = xn(4) * 88;
    Acc0 = Acc0 + xn(5) * -88;
    Acc0 = Acc0 + xn(6) * -88;
    Acc0 = Acc0 + u(i)  * 88;
    T0    = rem( floor( Acc0/2^8 ) , 128);
    Acc1 = floor( (xn(1) * 126) / 2^2 );
    Acc1 = Acc1 + xn(2) * -95;
    Acc1 = Acc1 + xn(3) * 96;
    T1    = rem( floor( Acc1/2^5 ), 128);

    % states
    Acc2 = xn(2);
    xn(1) = Acc2;
    Acc3 = xn(3);
    xn(2) = Acc3;
    Acc4 = floor( (T0) / 2^4 );
    Acc4 = Acc4 + (T1) * 2^6;
    xn(3) = rem( floor( Acc4/2^6 ), 128);
    Acc5 = xn(5);
    xn(4) = Acc5;
    Acc6 = xn(6);
    xn(5) = Acc6;
    Acc7 = u(i);
    xn(6) = Acc7;

    % output(s)
    Acc8 = floor( (T0) / 2^4 );
    Acc8 = Acc8 + (T1) * 2^6;
    y(i)  = rem( floor( Acc8/2^6 ), 128);
    
end

y = 2.^-3.*y;
