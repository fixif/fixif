double filtre1double( double u, double* xn){    double y;    // states    // intermediate variables    double T = 0.98932706840712325568887308691046200692653656005859375*xn[0]\ + -4.9571981140316569991455253330059349536895751953125*xn[1]\ + 9.935631309482101158891964587382972240447998046875*xn[2]\ + -9.956976547934797139305374003015458583831787109375*xn[3]\ + 4.989216284071265050670263008214533329010009765625*xn[4]\ + 0.0001878773934842481452278661890886723995208740234375*xn[5]\ + -0.00056358116206478570120452786795794963836669921875*xn[6]\ + 0.000375703771577917677859659306704998016357421875*xn[7]\ + 0.0003757037715335087568746530450880527496337890625*xn[8]\ + -0.00056358116204346941913172486238181591033935546875*xn[9]\ + 0.00018787739348080645385152820381335914134979248046875*u    ;    // output(s)    y = T    ;    // states    xn[0] = xn[1];    xn[1] = xn[2];    xn[2] = xn[3];    xn[3] = xn[4];    xn[4] = T    ;    xn[5] = xn[6];    xn[6] = xn[7];    xn[7] = xn[8];    xn[8] = xn[9];    xn[9] = u    ;    // output    return y;}