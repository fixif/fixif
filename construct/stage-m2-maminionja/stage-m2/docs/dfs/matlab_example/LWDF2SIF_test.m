clc

%FILTER ORDER
filterorder = 5;
%CUTOFF FREQUENCY
Wn = 0.1;

%HERE WE COMPUTE TRANSFER FUNCTION OF BUTTERWORTH FILTER
%WE DO THAT MANUALLY, BECAUSE OF NUMERICAL INSTABILITY PROBLEMS
[z,p,k] = butter(filterorder,Wn);
[num,a2] = butter(filterorder,Wn);
A = diag(p);
denum = poly(A); 
Hzbutter.ident = 'LP PROTOTYPE: butter,5,0.1';
Hzbutter.roots_fz = z;
Hzbutter.poly_fz = num;
Hzbutter.roots_gz = p;
Hzbutter.poly_gz = denum;
Hsbutter = Hz2Hs(Hzbutter);

%FINALLY WE CONVERT BUTTERWORTH FILTER TO THE 
%LATTICE WAVE DIGITAL FILTER USING wdf_toolbox

LWDF = Hs2LWDF(Hsbutter);   
%final LWDF is a structure with following fields:
%   LWDF.gamma  - coefficients of each adaptor, each of them is in interval [-1,1]
%   LWDF.wdaCodes  - special structure describing what adaptors each branch has

gamma = LWDF.gamma

%WE CONVERT LWDF TO SIF
SIF = LWDF2SIF(LWDF, filterorder, 'LPF');

%WE CHECK THAT TRANSFER FUNCTIONS OF ORIGINAL LWDF AND
%ITS CONVERTION TO SIF ARE NOT FAR FROM EACH OTHER IN TERMS
%OF NORM

tfSIF = tf(SIF);  %SIF transfer function

%for LWDF transfer function procedure is more complicated
Hz_LWDF = LWDF2Hz(LWDF);
[num1, num2] = Hz_LWDF.poly_fz;
[denum1, denum2] = Hz_LWDF.poly_gz;
tfLWDF = tf(num1, denum1, -1);

distance_norm = norm(tfSIF - tfLWDF)    %computing norm of the difference of tf





