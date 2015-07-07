N=50;

M = zeros(N,3);
i=1;

for ratio=linspace(1,100,N)
	
	[num,den] = butter(3,[0.75 0.9]/ratio);
	H = tf(num,den,-1);
	Sys = ss(H);
	
	% forme rhoDFIIt
	% to do...
	
	% forme modale en q
	SysM = canon( Sys, 'modal' );
	R2 = SS2FWR( SysM);
	R2 = relaxedl2scaling(R2);
	R2 = computeW(R2);
	M(i,2) = MsensH(R2);
	
		
	% forme modale en rho
	R3 = Modaldelta2FWR(Sys);
	M(i,3) = MsensH(R3);

	
	i=i+1;
	if mod(i,10)==0
		i
	end
end