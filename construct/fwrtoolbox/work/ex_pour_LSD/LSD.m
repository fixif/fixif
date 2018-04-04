% filtre, Gevers p68
num = 0.01594*conv( conv( [1 1], [1 1]),[1 1]);
den = [1 -1.9749 1.5562 -0.4538];

% forme directe I
R1 = DFIq2FWR(tf(num,den,-1))
implementCdouble( R1, 'DFIq')

% forme directe IIt delta
R2 = rhoDFIIt2FWR( tf(num,den,-1), [1 1 1])
implementCdouble( R2, 'DFIIdelta')