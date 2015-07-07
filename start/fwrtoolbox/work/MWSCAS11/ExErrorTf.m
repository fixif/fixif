
% system
[num, den] = butter(4,0.125);
H=tf(num,den,-1);
Sys=ss(H);
Sys=balreal(Sys);

% FWS
S = SS2FWS(Sys);

Nbbits=16;



%============
% state-space

% direct form I
R1 = DFIqbis2FWR(H);


%==========
% rhoDFIIt

Srho = rhoDFIIt2FWS( H, [0.5 0.5 0.5 0.5], 0, 0.25*[1 1 1 1], 1);
Srho.Gamma = [1 1 1 1];

%S_rhotradeoff = optim(S_rhopole,{'method','ASA','MinMax',2,'l2scaling', 'relaxed2'},@tradeoffMeasureError, error_tf(R7), error_pole(R8) );
load S_rhotradeoff
R9 = S_rhotradeoff.R;


D1 = zeros(1,32);
D2 = D1;


% display results for different wordlength
WL=[3:20];
for Nbbits=WL

    disp('=====================');
    disp([ 'Nb bits = ' num2str(Nbbits) ]);
    
    %quantized realization
    R1q = setFPIS(R1, 2*Nbbits, 0.9999, Nbbits, 2*Nbbits, 2*Nbbits, 2*Nbbits, 3*Nbbits, 0, 'RBM');
    R1q = quantized(R1q);
    R9q = setFPIS(R9, 2*Nbbits, 0.9999, Nbbits, 2*Nbbits, 2*Nbbits, 2*Nbbits, 3*Nbbits, 0, 'RBM');
    R9q = quantized(R9q);    
    
    
    % display results
    %dispResult( R1, R1q, 'Z1 (direct form)' );
    %dispResult( R9, R9q, 'Z9 (tradeoff optimal rhoDFIIt');
    D1(Nbbits) = norm( tf(R1q)-H,Inf );
    D2(Nbbits) = norm( tf(R9q)-H,Inf );
   
end
semilogy( WL,D1(WL),'bd')
hold on
semilogy( WL,D2(WL),'r*')


Nbbits=5
R9q = setFPIS(R9, Nbbits, 10, Nbbits, Nbbits, Nbbits, Nbbits, Nbbits+10, 0, 'RBM');
R9q = quantized(R9q);







% % function to display result
% function dispResult( R, Rq, name)
% 
%     el = max(  abs( sort(abs(eig(R.AZ))) - sort(abs(eig(Rq.AZ))) )  ./ (1-abs(eig(R.AZ)))  );
% 
%     disp( [ name ':']);
%     disp([ '     error_tf=' num2str(error_tf(R)) ' |h-h''| = ' num2str(norm(tf(Rq)-tf(R))) ]);
%     disp([ '     error_lambda=' num2str(error_pole(R)) ' M|l-l''| = ' num2str(el ) ]);    
% end