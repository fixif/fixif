[num den] = butter(2, 2*pi*10,'s');
Hc=tf(num,den);
H=c2d(Hc,0.001,'tustin');
Sys = ss(H);

M=[];I=[];i=1;
S=SSrho2FWS( Sys, 1, 0, 2^(-3), 1 );
i=1;
for gamma=linspace(0.99,1.01,100)
	S.Gamma(1) = gamma;
	M(i) = MsensH( relaxedl2scaling(S.R) );
	I(i) = gamma;
	i=i+1;
end
plot(I,M)
