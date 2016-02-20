% exemple state-space

ordre=30;
rng(123456)

% random ss
sys = drss(ordre,10,10);
T = [ 1000*rand(2,ordre); rand(ordre-2,ordre)];
R = SS2FWR( inv(T)*sys.A*T, inv(T)*sys.B, sys.C*T, sys.D)

%R=SSrho2FWR(sys,rand(1,10),1,2^-5*ones(1,10),1)

gen_Benoit(R,[-25,30], 'ex-MIMO-grand.mat')
