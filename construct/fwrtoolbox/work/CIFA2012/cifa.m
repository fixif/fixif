
function S = cifa()

Nb = 5;
gm = (2*pi*150)^2;
gM = (2*pi*250)^2;
T = 0.1;
xim = 0.08;
xiM = 0.2;
wcm = 2*pi*150;
wcM = 2*pi*250;

[A,B,C,D] = toto( (gm+gM)/2, T, (xim+xiM)/2, (wcm+wcM)/2 ) ;
R = SS2FWR( balreal(ss(A,B,C,D)) );
R.WZ = ones(size(R.WZ));
S = FWS( R, @UYW_SScifa, [], [Nb,gm,gM,T,xim,xiM,wcm,wcM], 'T', eye(R.n));



% UYW function for the classical state-space structuration
function [U,Y,W,cost_flag] = UYW_SScifa( Rini, paramsValue, dataFWS)

%test if T is singular    
if (cond(paramsValue{1})>1e10)
    cost_flag=0;
    paramsValue{1} = eye(size(paramsValue{1}));
else
    cost_flag=1;
end

% compute U,W,Y
Y = eye(0);
W = eye(0);
U = paramsValue{1};