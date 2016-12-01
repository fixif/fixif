execute("gabarit.sol");
execute("filtre2.sol");

res = checkModulusFilterInSpecification(b, a, [| { .Omega = [0;2*50/50000],
                                                   .omegaFactor = pi,
	                                           .betaInf = 10^(-0.1/20),
                                                   .betaSup = 10^(0/20)
                                                 },
                                                 { .Omega = [2*90/50000;1],
                                                   .omegaFactor = pi,
					           .betaInf = 0,
					           .betaSup = 10^(-40/20)
					         } |]);

presentResults(res);

