% Create sample butter filter
%[num, den] = butter(10, 0.05);
[num, den] = butter(4, 0.05);
[A, B, C, D] = tf2ss(num, den);
H = tf(num, den, 1);
% create DFI

%num = [0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.10]
%den = [1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0]

R = DFIq2FWR(num, den)
R2 = SS2FWR(A,B,C,D)

%DONE
%mycode = algorithmLaTeX(R, 'proutix')
implementCdouble(R, 'fuckingFilter')