
import gabarit

import sollya

sollya.suppressmessage(57, 174, 130, 457)

sollya.execute("filtre1.sol")

b = sollya.parse("b")
a = sollya.parse("a")

res = gabarit.check_modulus_filter_in_specification(b, a, [ { "Omega" : sollya.parse("[0;2*9600/48000]"),
                                                              "omegaFactor" : sollya.pi,
                                                              "betaInf" : sollya.parse("10^(-1/20)"),
                                                              "betaSup" : sollya.parse("10^(0/20)"),
                                                            },
                                                            { "Omega" : sollya.parse("[2*12000/48000;1]"),
                                                              "omegaFactor" : sollya.pi,
                                                              "betaInf" : 0,
                                                              "betaSup" : sollya.parse("10^(-20/20)"),
                                                            } ]) 

gabarit.present_results(res)

