filterorder = 5;
Wn = 0.25;

[z,p,k] = butter(filterorder,Wn);
[num,a2] = butter(5,0.1);
A = diag(p);
denum = poly(A); %denumerator for tf
butter_tf = tf(num,denum, -1);

Hzbutter.ident = 'LP PROTOTYPE: butter,5,0.1';
Hzbutter.roots_fz = z;
Hzbutter.poly_fz = num;
Hzbutter.roots_gz = p;
Hzbutter.poly_gz = denum;

Hsbutter = Hz2Hs(Hzbutter);
LWDF = Hs2LWDF(Hsbutter);
Hz_LWDF = LWDF2Hz(LWDF);

[num1, num2] = Hz_LWDF.poly_fz;
[denum1, denum2] = Hz_LWDF.poly_gz;
tfLWDF = tf(num1, denum1, -1);


spectral_radius = max(abs(roots(tfLWDF.den{1})))

SIF_LWDF = LWDF2SIF(LWDF, filterorder, 'LPF');
tfSIF_LWDF = tf(SIF_LWDF);

SIF_DFI = DFIq2FWR(tfLWDF);
tfSIF_DFI = tf(SIF_DFI);


SIF_SS_noopt = SS2FWS(balreal(ss(tfLWDF)));

SS_Sopt_tf = optim(SIF_SS_noopt, {'method','newton','Display','Iter'}, @error_tf);
SIF_SS = SS_Sopt_tf.R;

SIF_rho_noopt = rhoDFIIt2FWS( tfLWDF, ones(1, filterorder), 1, -ones(1, filterorder), 1 );
Sopt_tf = optim(SIF_rho_noopt, {'method','newton','Display','Iter'}, @error_tf);
Sopt_pole = optim(SIF_rho_noopt, {'method','newton','Display','Iter'}, @error_pole);
Sopt_troff = optim(SIF_rho_noopt, {'method','newton','Display','Iter'},...
   @tradeoffMeasureError,  error_tf(Sopt_tf.R), error_pole(Sopt_pole.R));

SIF_rho = Sopt_troff.R;