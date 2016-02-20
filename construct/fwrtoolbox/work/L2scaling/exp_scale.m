% realisation initial
[num,den]=butter(3,0.4);
H=tf(num,den,1);
Sys=ss(H);

i=1;
N=100;
W=zeros(N,3);
for K=linspace(52,53,N)

	% structuration
	S = SS2FWS(K*Sys);

	% optimal pb
	Sl2=optim(S,{'l2scaling','no','method','fmincon','Display','none'},@MsensH);
	
	% controlability grammian
	W(i,:)=diag(Sl2.R.Wc);
	i=i+1
	
end
