% DSPE'11 example

% transfer function
[num,den]=butter(4,0.125); 
H=tf(num,den,-1);

% state-space realization (with balanced state-space as origin)
S=SS2FWS( balreal(ss(H)));

% L2-sensitivity optimization
options = {'method','newton', 'display', 'Iter'}
Sopt = optim( S, options, @MsensH);

% set the Fixed-Point Implementation Scheme