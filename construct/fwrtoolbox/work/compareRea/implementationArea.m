
% $Id$


function area = implementationArea( R, betaZ, betaU, gammaU, betaTXY, betaADD, betaG )


[gammaZ, shiftZ, gammaADD, shiftADD, gammaTXY] = implementationFormat( R, betaZ, betaU, gammaU, betaTXY, betaADD, betaG );
betaTXU = [ betaTXY(1:R.l+R.n); betaU ];


betaZ( find(abs(R.Z)<eps) ) = 0;
Mul = 0.5*ones(1,size(R.Z,2))*betaZ*betaTXU;
Add = ones(1,size(R.Z,2))*( betaADD .* (R.WZ*ones(size(R.Z,1),1)) );
area = Mul+Add;





