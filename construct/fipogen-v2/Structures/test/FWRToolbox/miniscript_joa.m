% Create sample butter filter
[num, den] = butter(10, 0.05);
%[num, den] = butter(4, 0.05);
[A, B, C, D] = tf2ss(num, den);

SIF1 = SS2FWR(A,B,C,D);

%[num,den] = butter(4,0.05);
%[A,B,C,D] = tf2ss(num,den);

%ss1 = ss(A,B,C,D,1)

%[M, MZ ] = MsensH_cl(SIF1, ss1)

%H = tf(num, den, 1);
% create DFI

%num = [0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.10]
%den = [1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0]

%R = DFIq2FWR(num, den)
%R = SS2FWR(A,B,C,D)

%DONE
%mycode = algorithmLaTeX(R, 'proutix')
%implementCdouble(R, 'fuckingFilter')

% n = 3
% p = 4
% q = 5

a = [0.00 0.01 0.02 ; 
     0.10 0.11 0.12 ; 
     0.20 0.21 0.22 ]

b = [1.00 1.01 1.02 1.03 ; 
     1.10 1.11 1.12 1.13 ; 
     1.20 1.21 1.22 1.23 ]

c = [2.00 2.01 2.02 ; 
     2.10 2.11 2.12 ; 
     2.20 2.21 2.22 ; 
     2.30 2.31 2.32 ; 
     2.40 2.41 2.42 ]

d = [3.00 3.01 3.02 3.03 ;
     3.10 3.11 3.12 3.13 ;
     3.20 3.21 3.22 3.23 ;
     3.30 3.31 3.32 3.33 ;
     3.40 3.41 3.42 3.43 ]
%  
% d = [0 0 0 0 ;
%      0 0 0 0 ;
%      0 0 0 0 ;
%      0 0 0 0 ;
%      0 0 0 0 ]
%  
% a = a/10
% b=b/10
% c=c/10
%  
gzz = ss(a,b,c,d,1);

gzz(2,4)

gzz(2,:)

gzz(3,:)

gzz(:,2)

gzz(:,3)


%gzz = SS2FWR(A,B,C,D)

%[M, MX] = MsensH(gzz)