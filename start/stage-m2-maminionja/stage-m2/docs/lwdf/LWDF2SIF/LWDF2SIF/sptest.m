function [Znew] = sptest()

Z = zeros(22,22);   %1

M = zeros(22,22);   % -1
D = zeros(22,22); %1/2
A = zeros(22,22);   %-alphas

for i = 1:16
    Z(i,i) = 1;
end
A(2,1) = 1;
Z(3,1) = 1;
M( 3,2 ) = 1;
A( 5, 4) = 1;
Z( 6,4 ) = 1;
M( 6,5 ) = 1;
Z( 7,3 ) = 1;
M( 7,6 ) = 1;
A( 8,7 ) = 1;
Z( 8,6 ) = 1;
M( 9,8 ) = 1;
Z( 9,7 ) = 1;
A( 11,10 ) = 1;
M( 12,11 ) = 1;
Z( 12,10 ) = 1;
M( 13,12 ) = 1;
A( 14,13 ) = 1;
Z( 14,12 ) = 1;
M( 15,14 ) = 1;
Z( 15,13 ) = 1;
M( 16,9 ) = 1;
M( 16,15 ) = 1;
M( 17, 2) = 1;
M( 18, 8) = 1;
M( 19,5 ) = 1;
M( 20,14 ) = 1;
M( 21,11 ) = 1;
D( 22,16 ) = 1;

M( 1,17 ) = 1;
Z( 1,22 ) = 1;
Z( 2,17 ) = 1;
Z( 4,18 ) = 1;
M( 4,19 ) = 1;
Z( 5,19 ) = 1;
Z( 10,20 ) = 1;
M( 10,21 ) = 1;
Z( 11, 21) = 1;
M( 13, 22) = 1;

Znew = Z + A + M + D;

save('MatrixZ', 'Znew');

hold on
Asp = sparse(A);
Zsp = sparse(Z);
Msp = sparse(M);
Dsp = sparse(D);
spy(Zsp, '.r', 30)
spy(Msp, 'oblue', 9)
spy(Dsp, '+black', 10)
spy(Asp, 'xblack', 15)
hold off

