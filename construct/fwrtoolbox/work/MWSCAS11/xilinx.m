clear all
close all
% system
[num, den] = butter(6,0.125);
H=tf(num,den,-1);




%============
% state-space

% direct form I
R1 = DFIqbis2FWR(H);


%==========
% rhoDFIIt

Srho = rhoDFIIt2FWS( H, 0.9*ones(1,6), 0, ones(1,6), 1);
%Srho = optim(Srho,{'method','newton','Display','Iter'},@error_tf);
load Srho
Srho.Gamma=Srho.Gamma; % renormalisation Delta=1 !!
R9 = Srho.R;


WL=[3:25];
D1A = zeros(1,max(WL));
D2A = D1A;
D1B = D1A;
D2B = D1A;
nbUY=8
% display results for different wordlength

for Nbbits=WL

    disp('=====================');
    disp([ 'Nb bits = ' num2str(Nbbits) ]);
    
    %quantized realization
    R1q = setFPIS(R1, Nbbits, 0.999, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R1q = quantized(R1q);
    R9q = setFPIS(R9, Nbbits, 0.999, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RAM');
    R9q = quantized(R9q);    
        
    % diff
    D1A(Nbbits) = norm( tf(R1q)-H, Inf );
    D2A(Nbbits) = norm( tf(R9q)-H, Inf );
    
    
    
    %quantized realization
    R1q = setFPIS(R1, Nbbits, 0.999, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RBM');
    R1q = quantized(R1q);
    R9q = setFPIS(R9, Nbbits, 0.999, Nbbits, Nbbits, Nbbits, Nbbits, 2*Nbbits, 0, 'RBM');
    R9q = quantized(R9q);            
   
    %RNG
    D1B(Nbbits) = ONP(R1q);
    D2B(Nbbits) = ONP(R9q);
    
    
    
    
  
end

figure
semilogy( WL,D1A(WL),'bd')
hold on
semilogy( WL,D2A(WL),'r*')
legend('DFI','\rhoDFIIt')


figure
semilogy( [15:25],D1B([15:25]),'bd')
hold on
semilogy( WL,D2B(WL),'r*')
legend('DFI','\rhoDFIIt')




n=12
R1q = setFPIS(R1, 10, 0.999, 18, 18, 18, 10, 3*n, 0, 'RBM');
R1q = quantized(R1q);
      

%n=7
%R9q = setFPIS(R9, 11, 0.999, 10, 11, 11, 11, 3*n, 0, 'qRBM');
%R9q = quantized(R9q); 
n=6
R9.Z(157)=0;    % supprime le coef en 1e-5
R9q = setFPIS(R9, 10, 0.999, 8, 10, 10, 10, 3*n, 0, 'qRBM');
R9q = quantized(R9q); 


implementMATLAB(R1q,'DFI');
implementMATLAB(R9q,'rhoDFIIt');



u=rand(1,1000);
y=filter(num,den,u);
y9=rhoDFIIt(u')';
y1=DFI(u')';
figure; plot(y); hold on; plot(y9,'r'); plot(y1,'g'); legend('y','\rhoDFIIt','DFI')
figure;plot(y-y1,'g'); hold on; plot(y-y9,'r'); legend('DFI','\rhoDFIIt')


% % function to display result
% function dispResult( R, Rq, name)
% 
%     el = max(  abs( sort(abs(eig(R.AZ))) - sort(abs(eig(Rq.AZ))) )  ./ (1-abs(eig(R.AZ)))  );
% 
%     disp( [ name ':']);
%     disp([ '     error_tf=' num2str(error_tf(R)) ' |h-h''| = ' num2str(norm(tf(Rq)-tf(R))) ]);
%     disp([ '     error_lambda=' num2str(error_pole(R)) ' M|l-l''| = ' num2str(el ) ]);    
% end