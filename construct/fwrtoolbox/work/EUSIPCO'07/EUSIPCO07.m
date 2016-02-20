% examples EUSIPCO'07

% filtre ini
%[num,den] = butter(3,0.1);
num = 0.01594*conv( conv( [1 1], [1 1]),[1 1]);
den = [1 -1.9749 1.5562 -0.4538];

%======================
% R1 : forme directe II
R1 = SS2FWR( canon(ss(tf(num,den,1)),'companion') );
20*log10( RNG(l2scaling(R1)) )

%======================
% R1b : forme directe I
R1b = DFIq2FWR(num,den);
20*log10( RNG(l2scaling(R1b)) )

%=========================
% R2 : forme espace d'Žtat
S2 = SS2FWS( balreal(ss(R1)) );

opt={'method','ASA','l2scaling','yes','MinMax',1e6};

%S2opt = optim( S2, opt, @RNG)
S2.T = [ 6.889419923908653e+05    -2.088243825969795e+05    -9.885528082083269e+04 ;
         6.517881303437560e+04    -9.508808580278528e+04     3.589515003929240e+05 ;
        -7.052304391892418e+05    -2.127831230778995e+05    -6.339519633331064e+04 ];
20*log10( RNG(l2scaling(S2.R)) )


%==================
% R3 : forme delta
Delta = 2^-5;
S3 = SSdelta2FWS( balreal(ss(R1)), Delta);
%S3opt = optim( S3, opt, @RNG)

S3.T = [ 1.532424209114965e-02    -2.921532214554645e-03    -2.346529721834305e-05 ;
        -5.813882253906119e-03     3.411814929962174e-04    -9.450563251383820e-05 ;
         1.563847934267144e-02     2.989547295696574e-03    -1.213985177328962e-05 ];
20*log10( RNG(l2scaling(S3.R)) )


%============================
% R4 : forme d'Žtat implicite
S4 = SSwithE2FWS( ss(l2scaling(S2.R)) );
%S4.E=[1 1 1];
opt={'method','ASA','l2scaling','yes','MinMax',1e3,'FWSmeasure','no'};
%S4opt = optim( S4, opt, @RNG) 

S4.T = [  1.988783321385407e-02    -1.350318963257524e-02    -5.391218707410612e-03 ;
         -4.387834368367410e-04     1.385968564224432e-02    -1.018474715925879e-02 ;
          2.024589582254330e-02     1.339234833025612e-02     5.059054263172245e-03 ];
S4.E = [ -7.427116274652800e-01    -9.834549509485258e-01     5.236269358377529e-02 ];

20*log10( RNG(l2scaling(S4.R)) )
