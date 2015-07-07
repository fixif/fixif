

% on recharge les indices parcourus (il ne reste que les indices interessants)
%
load indices_parcourusDL

Sysp2 = ss( Sysp.A, [Sysp.B Sysp.B], [Sysp.C; Sysp.C], 0,1);


% init valeurs
tab_norm = zeros(NbPart,1);
tab_M1 = zeros(NbPart,1);
tab_M2 = zeros(NbPart,1);
ind_interdit=zeros(NbPart,1);
minM1=+Inf; minM2=+Inf;

% on parcourt chaque indice possible
for i=1:NbPart

	if (mod(i,10)==0)
		i
	end

	indice = indices_part(i,:);
	[Kc, Kf,Q,M,reg_lqg] = lqgi(indice,Sysp,+Reg);
	%try
    R = Observer2FWR(Sysp,Kc,Kf,Q);
    
    tab_M1(i) = MsensH_cl(R,Sysp2);
    tab_M2(i) = MsensPole_cl(R,Sysp2);
    
    M1= tab_M1(i);
    if (M1<minM1)
        indM1=i;
        minM1=M1;
        minM1_M2=M2;
        RM1=R;
    end
    
    M2= tab_M2(i);
    if (M2<minM2)
        indM2=i;
        minM2=M2;
        minM2_M1=M1;
        RM2=R;
    end
    
    %catch
    %ind_interdit(i)=i;
    %end
    
end

