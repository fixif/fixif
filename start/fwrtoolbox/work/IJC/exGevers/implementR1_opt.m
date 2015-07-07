% Fixed-point algorithm in Matlab language
% (it uses integer to simulate fixed-point)
%
% y = implementR1_opt(u)
%
% y: filtered output(s)
% u: intput(s)
%
% date: 16-Nov-2007 16:55:42
% Automatically generated by implementMATLAB / FWRToolbox


function y = implementR1_opt(u)

% initialize                   
u = round(2^11*u);y = zeros( length(u), 1 );xn = zeros(4,1);xnp = zeros(4,1);                
                               
for i=1:length(u)

    % intermediate variables    Acc0 = xn(1) * 16477;    Acc0 = Acc0 + xn(2) * -12633;    Acc0 = Acc0 + xn(3) * 6457;    Acc0 = Acc0 + xn(4) * -7047;    Acc0 = Acc0 + u(i)  * -498;    xnp(1) = floor( Acc0/2^14 );    Acc1 = xn(1) * -13976;    Acc1 = Acc1 + xn(2) * 18235;    Acc1 = Acc1 + xn(3) * 2562;    Acc1 = Acc1 + xn(4) * -14063;    Acc1 = Acc1 + u(i)  * 748;    xnp(2) = floor( Acc1/2^14 );    Acc2 = xn(1) * -26423;    Acc2 = Acc2 + xn(2) * 22730;    Acc2 = Acc2 + xn(3) * 9504;    Acc2 = Acc2 + xn(4) * -15444;    Acc2 = Acc2 + u(i)  * 2241;    xnp(3) = floor( Acc2/2^14 );    Acc3 = xn(1) * -21277;    Acc3 = Acc3 + xn(2) * 24592;    Acc3 = Acc3 + xn(3) * -7956;    Acc3 = Acc3 + xn(4) * -1565;    Acc3 = Acc3 + u(i)  * 1950;    xnp(4) = floor( Acc3/2^12 );    % output(s)    Acc4 = xn(1) * 21996;    Acc4 = Acc4 + xn(2) * -2083;    Acc4 = Acc4 + xn(3) * -4531;    Acc4 = Acc4 + xn(4) * 22994;    y(i)   = floor( Acc4/2^15 );    %permutations    xn = xnp;
    
end

y = 2^--6*y;