%Purpose:
% Fixed-point algorithm in Matlab language
% (it uses integer to simulate fixed-point)
%
%Syntax:
% y = rhoDFIIt(u)
%
%Parameters:
% y: filtered output(s)
% u: intput(s)
%
% date: 26-Apr-2011 17:50:21
% Automatically generated by implementMATLAB / FWRToolbox


function y = rhoDFIIt(u)

% initialize                   
u = round(2.^9.*u);y = zeros( size(u,1), 1 );xn = zeros(6,1);                
                               
for i=1:size(u,1)

    % intermediate variables    Acc00 = xn(1);    T00   = Acc00;    Acc01 = xn(2);    T01   = Acc01;    Acc02 = xn(3);    T02   = Acc02;    Acc03 = xn(4);    T03   = Acc03;    Acc04 = xn(5);    T04   = Acc04;    Acc05 = xn(6);    T05   = Acc05;    % states    Acc06 = T00   * -15;    Acc06 = Acc06 + (T01) * 2^5;    Acc06 = Acc06 + xn(1) * 115;    Acc06 = Acc06 + floor( (u(i)  * 80) / 2^12 );    xn(1) = floor( Acc06/2^7 );    Acc07 = T00   * -78;    Acc07 = Acc07 + (T02) * 2^6;    Acc07 = Acc07 + xn(2) * 100;    Acc07 = Acc07 + floor( (u(i)  * 86) / 2^8 );    xn(2) = floor( Acc07/2^7 );    Acc08 = T00   * -7;    Acc08 = Acc08 + (T03) * 2^6;    Acc08 = Acc08 + xn(3) * 94;    Acc08 = Acc08 + (u(i)) * 2^1;    xn(3) = floor( Acc08/2^7 );    Acc09 = T00   * -12;    Acc09 = Acc09 + (T04) * 2^5;    Acc09 = Acc09 + xn(4) * 92;    Acc09 = Acc09 + (u(i)) * 2^2;    xn(4) = floor( Acc09/2^7 );    Acc10 = T00   * -5;    Acc10 = Acc10 + (T05) * 2^4;    Acc10 = Acc10 + xn(5) * 92;    Acc10 = Acc10 + u(i)  * 11;    xn(5) = floor( Acc10/2^7 );    Acc11 = T00   * -4;    Acc11 = Acc11 + xn(6) * 95;    Acc11 = Acc11 + u(i)  * 27;    xn(6) = floor( Acc11/2^7 );    % output(s)    Acc12 = T00;    y(i)  = Acc12;
    
end

y = 2.^-8.*y;