% system
[num, den] =butter(4,0.05);
H=tf(num,den,-1);
Sys=ss(H);
Sys=balreal(Sys);

% FWS
S = SS2FWS(Sys);

Nbbits=16;


% optimal tf_error
%S_tferror = optim(S,{'method','ASA','l2scaling','relaxed2'},@error_tf)
load S_tferror
R1 = setFPIS(S_tferror.R, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
R1q = quantized(R1);

% optimal ML2
%S_ML2 = optim(S,{'method','newton','Display','Iter','l2scaling','yes'},@MsensH)
load S_ML2
R2 = setFPIS(S_ML2.R, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
R2q = quantized(R2);

% direct form II
R3 = SS2FWR(ss(H));
R3 = setFPIS(R3, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
R3q = quantized(R3);

% balanced realization
R4 = setFPIS(S.Rini, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
R4q = quantized(R4);

disp([ 'balanced realization Z1: ' 'error_tf=' num2str(error_tf(R3)) ' |h-h''| = ' num2str(norm(tf(R3q)-H)) ])
disp([ 'balanced realization Z2: ' 'error_tf=' num2str(error_tf(R4)) ' |h-h''| = ' num2str(norm(tf(R4q)-H)) ])
disp([ 'balanced realization Z3: ' 'error_tf=' num2str(error_tf(R1)) ' |h-h''| = ' num2str(norm(tf(R1q)-H)) ])