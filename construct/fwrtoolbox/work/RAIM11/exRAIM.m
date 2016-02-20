% All frequency values are in Hz.
Fs = 48000;  % Sampling Frequency

N     = 3;    % Order
Fpass = 50;   % Passband Frequency
Apass = 0.1;  % Passband Ripple (dB)
Astop = 40;   % Stopband Attenuation (dB)

% Construct an FDESIGN object and call its ELLIP method.
h  = fdesign.lowpass('N,Fp,Ap,Ast', N, Fpass, Apass, Astop, Fs);
Hd = design(h, 'ellip');

[num den] = tf(Hd);
H = tf( num, den, -1);
u=8*[zeros(1,10) ones(1,4000)];

% DFI
R1 = DFIqbis2FWR(H);
N = 8; 
R18 = setFPIS( R1, N, 10, N,N,N,N,2*N,0,'RAM');
R18q = quantized(R18);
implementMATLAB(R18q,'filterR18q');
N = 16; 
R116 = setFPIS( R1, N, 10, N,N,N,N,2*N,0,'RAM');
R116q = quantized(R116);
implementMATLAB(R116q,'filterR116q');
N = 24; 
R124 = setFPIS( R1, N, 10, N,N,N,N,2*N,0,'RAM');
R124q = quantized(R124);
implementMATLAB(R124q,'filterR124q');


pause
pause


y18 = filterR18q(u');
y116 = filterR116q(u');
y124 = filterR124q(u');
y1f = realize(R1,u);

plot(y1f,'b'); hold on; plot (y18,'g'); plot(y116,'r'); plot(y124,'c');
legend('H', '8 bits', '16 bits', '24 bits')



% DFIq
R2 = rhoDFIIt2FWR( H, [1 1 1], [1 1 1], 2^-5*[1 1 1], 1 );
N = 12; R2 = setFPIS( R2, N, 10, N,N,N,N,2*N,0,'RAM');
R2q = quantized(R2);
implementMATLAB(R2q);

pause
pause


y2 = myFilter(u');
y2f = realize(R2,u);

plot(y2); hold on; plot(y2f,'r');