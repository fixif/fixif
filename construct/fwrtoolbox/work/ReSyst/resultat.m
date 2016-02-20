function rep = resultat( R, nom)

display(nom)

R = setFPIS( R, 'DSP8', 1);
Rq = quantized(R);

display( [ 'diff |H-Himplanté|=' num2str( norm( tf(R) - tf(Rq) ) ) ])
display( [ 'tf=', num2str( MsensH(R) ) ])
display( [ 'ONP=', num2str( ONP(R) ) ])

display( implementLaTeX( R, nom) )

implementMATLAB(R,['fun' nom])

u = ones(1,100);
rep = feval(['fun' nom ],u');