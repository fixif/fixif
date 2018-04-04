function ExError


% system
[num, den] =butter(4,0.125);
H=tf(num,den,-1);
Sys=ss(H);
Sys=balreal(Sys);

% FWS
S = SS2FWS(Sys);

Nbbits=16;



%============
% state-space

% direct form II
R1 = SS2FWR(ss(H));

% balanced realization
R2 = S.Rini;

% optimal tf_error
%S_tferror = optim(S,{'method','ASA','l2scaling','relaxed2'},@error_tf)
S_tferror = S;
S_tferror.T = [ -1997.522 -3047.426 -2578.324  965.124 ;
	  -835.1027	-115.6848  1265.865	 568.9062;		
	  -4811.008 1982.06	  -1392.713	-9983.339;
	   3036.66  -4788.372  1121.302	-5923.437]';
R3 = S_tferror.R;


% optimal pole_error
%S_poleerror = optim(S,{'method','ASA','l2scaling','relaxed2'},@error_pole);
load S_poleerror
R4 = S_poleerror.R;


% optimal tradeoff tf/pole
%S_tradeoff = optim(S,{'method','ASA','l2scaling','relaxed2'},@tradeoffMeasureError, error_tf(R3), error_pole(R4) );
load S_tradeoff
R5 = S_tradeoff.R;



%==========
% rhoDFIIt

Srho = rhoDFIIt2FWS( H, [0.5 0.5 0.5 0.5], 0, 0.25*[1 1 1 1], 1);
Srho.Gamma = [1 1 1 1];
R6 = Srho.R;
Srho.Gamma = [0.5 0.5 0.5 0.5]; 
%S_rhotf = optim(Srho,{'method','ASA','MinMax',2,'l2scaling', 'relaxed2'},@error_tf);
load S_rhotf



%S_rhopole = optim(S_rhotf,{'method','ASA','MinMax',2,'l2scaling', 'relaxed2'},@error_pole);
load S_rhopole

R7 = S_rhotf.R;
R8 = S_rhopole.R;
%S_rhotradeoff = optim(S_rhopole,{'method','ASA','MinMax',2,'l2scaling', 'relaxed2'},@tradeoffMeasureError, error_tf(R7), error_pole(R8) );
load S_rhotradeoff
R9 = S_rhotradeoff.R;


pause

% display results for different bitlength
for Nbbits=[8 12 16]

    disp('=====================');
    disp([ 'Nb bits = ' num2str(Nbbits) ]);
    
    %quantized realization
    R1q = setFPIS(R1, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R1q = quantized(R1q);
    R2q = setFPIS(R2, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R2q = quantized(R2q);
    R3q = setFPIS(R3, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R3q = quantized(R3q);
    R4q = setFPIS(R4, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R4q = quantized(R4q);
    R5q = setFPIS(R5, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R5q = quantized(R5q);
    R6q = setFPIS(R6, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R6q = quantized(R6q);    
    R7q = setFPIS(R7, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R7q = quantized(R7q);    
    R8q = setFPIS(R8, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R8q = quantized(R8q);      
    R9q = setFPIS(R9, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R9q = quantized(R9q);    
    
    
    % display results
    dispResult( R1, R1q, 'Z1 (direct form)' );
    dispResult( R2, R2q, 'Z2 (balanced ss)' );
    dispResult( R3, R3q, 'Z3 (sigma_tf optimal ss)' );    
    dispResult( R4, R4q, 'Z4 (sigma_pole optimal ss)' );    
    dispResult( R5, R5q, 'Z5 (tradeoff tf/pole optimal ss)' );
    dispResult( R6, R6q, 'Z6 (delta-DFIIt)' );
    dispResult( R7, R7q, 'Z7 (sigma_tf optimal rhoDFIIt');
    dispResult( R8, R8q, 'Z8 (sigma_pole optimal rhoDFIIt');
    dispResult( R9, R9q, 'Z9 (tradeoff optimal rhoDFIIt');

    if Nbbits==16
       implementLaTeX(R5q,'realization Z5 implemented in 16-bit fixed-point')
       implementLaTeX(R9q,'realization Z9 implemented in 16-bit fixed-point')
    end
    
end

end


% function to display result
function dispResult( R, Rq, name)

    el = max(  abs( sort(abs(eig(R.AZ))) - sort(abs(eig(Rq.AZ))) )  ./ (1-abs(eig(R.AZ)))  );

    disp( [ name ':']);
    disp([ '     error_tf=' num2str(error_tf(R)) ' |h-h''| = ' num2str(norm(tf(Rq)-tf(R))) ]);
    disp([ '     error_lambda=' num2str(error_pole(R)) ' M|l-l''| = ' num2str(el ) ]);    
end