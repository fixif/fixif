function emax = er_cifa(S, U,Y,W, tol)

emax=-Inf; 

Nb = S.dataFWS(1);
gm = S.dataFWS(2);
gM = S.dataFWS(3);
T = S.dataFWS(4);
xim = S.dataFWS(5);
xiM = S.dataFWS(6);
wcm = S.dataFWS(7);
wcM = S.dataFWS(8);

for g=linspace(gm,gM,Nb)
    for xi=linspace(xim,xiM,Nb)
        for wc=linspace(wcm,wcM,Nb)

            [A,B,C,D] = toto(g,T,xi,wc);
            R = SS2FWR(balreal(ss(A,B,C,D)));
            R.WZ = ones(size(R.WZ));
            R = transform(R,U,Y,W);

            [M MZ] = MsensH(R);
            e = error_tf(R);

            dZdxi = [8*T*wc - 2*T*wc + 2*T*wc/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                8*T^2*wc^2 + 4*T*wc/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                0;
                0  0  0;
                16*T*wc - 2*T*wc + 2*T^3*g*wc/T^2*wc^2 + 4*T*wc*xi + 4^3 ...
                16*T*wc - 2*T*wc + 2*T^3*g*wc/T^2*wc^2 + 4*T*wc*xi + 4^3 ...
                -4*T^3*g*wc/T^2*wc^2 + 4*T*wc*xi + 4^2];
            dZdg = [0  0  0;
                0  0  0;
                2*T^4*wc^4 + 8*T^3*wc^3*xi + 16*T^2*wc^2*xi^2 + 7*T^2*wc^2 + 32*T*wc*xi + 20*T^2/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                T^4*wc^4 + 8*T^3*wc^3*xi + 16*T^2*wc^2*xi^2 + 6*T^2*wc^2 + 32*T*wc*xi + 24*T^2/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                T^2/T^2*wc^2 + 4*T*wc*xi + 4];

            dZdT = [-8*T^2*wc^2*xi + 4*T*wc + 4*xi*wc/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                -8*T*wc - 2*T*wc + 2*wc*xi/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                0;
                0  0  0;
                4*T^6*wc^6 + 12*T^5*wc^5*xi + 48*T^4*wc^4*xi^2 + 64*T^3*wc^3*xi^3 + 12*T^4*wc^4 + 92*T^3*wc^3*xi + 192*T^2*wc^2*xi^2 + 36*T^2*wc^2 + 192*T*wc*xi + 80*T*g/T^2*wc^2 + 4*T*wc*xi + 4^3 ...
                2*T^6*wc^6 + 12*T^5*wc^5*xi + 48*T^4*wc^4*xi^2 + 64*T^3*wc^3*xi^3 + 12*T^4*wc^4 + 88*T^3*wc^3*xi + 192*T^2*wc^2*xi^2 + 24*T^2*wc^2 + 192*T*wc*xi + 96*T*g/T^2*wc^2 + 4*T*wc*xi + 4^3 ...
                4*T*wc*xi + 2*T*g/T^2*wc^2 + 4*T*wc*xi + 4^2];

            dZdwc = [-8*T^2*wc^2*xi + 4*T*wc + 4*xi*T/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                -8*T*wc - 2*T*wc + 2*T*xi/T^2*wc^2 + 4*T*wc*xi + 4^2 ...
                0;
                0 0 0;
                4*T^3*wc^3 - 12*T*wc - 16*xi*T^3*g/T^2*wc^2 + 4*T*wc*xi + 4^3 ...
                4*T^3*wc^3 - 12*T*wc - 16*xi*T^3*g/T^2*wc^2 + 4*T*wc*xi + 4^3 ...
                -2*T*wc + 2*xi*T^3*g/T^2*wc^2 + 4*T*wc*xi + 4^2];


            % intermediate matrices
            M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
            M2 = [ R.L*inv(R.J) zeros(R.p,R.n) eye(R.p) ];
            N1 = [ inv(R.J)*R.M; eye(R.n); zeros(R.m,R.n) ];
            N2 = [ inv(R.J)*R.N; zeros(R.n,R.m); eye(R.m) ];
            Te = 1;




            Thetaxi = 2.^floor(log2(abs(xiM)));
            e = e + w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, dZdxi*Thetaxi );

            Thetag = 2.^floor(log2(abs(gM)));
            e = e + w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, dZdg*Thetag );

            ThetaT = 2.^floor(log2(abs(T)));
            e = e + w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, dZdT*ThetaT );

            Thetawc = 2.^floor(log2(abs(wcM)));
            e = e + w_prod_norm( R.AZ,M1,R.CZ,M2, R.AZ,R.BZ,N1,N2, dZdwc*Thetawc );

            if e>emax
                emax=e;
            end
            
            
        end
    end
end

