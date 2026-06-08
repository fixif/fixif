execute("gabarit.sol");
execute("filtre_silviu_20.sol");



res = checkModulusFilterInSpecification(b, a, [| { .Omega = [0;2*9600/48000],
                                                   .omegaFactor = pi,
	                                           .betaInf = 10^(-1/20),
                                                   .betaSup = 10^(0/20)
                                                 },
                                                 { .Omega = [2*12000/48000;1],
                                                   .omegaFactor = pi,
					           .betaInf = 0,
					           .betaSup = 10^(-20/20)
					         } |], prec);

presentResults(res);

