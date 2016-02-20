 %Purpose:
% Transform a transfer function ('tf' object) into a FWR object with the Direct Form I scheme
% the two parts (numerator and denominator) are computed separately
% H is normalized (a0=1)
%
%Syntax:
% R = DFIqbis2FWR( H )
%
%Parameters:
% R: FWR object
% H: tf object
%
%% $Id$


function R = DFIqbis2FWR( numq,denq )

% dimensions
if nargin==1
	% dimensions
	H = numq
	numq = H.num{1};
	denq = H.den{1};
end
nnum = length(numq) - 1;
nden = length(denq) - 1;

% normalization
numq = numq / denq(1);
denq = denq / denq(1);

% Gammas
Gamma1 = [ numq(2:nnum+1) zeros(1,nden) ; zeros(1,nnum) -denq(2:nden+1) ];
Gamma2 = [ diag(ones([1 nnum-1]),-1) zeros([nnum nden]); zeros([nden nnum]) diag(ones([1 nden-1]),-1)];
Gamma3 = [ 1; zeros([nnum+nden-1 1]) ];
Gamma4 = [ zeros(nnum,2); 1 1 ; zeros(nden-1,2) ];

% transformation to 'optimize' the code
T=rot90(eye(2*nnum));


% build FWR object
%R = FWR( denq(1), Gamma4, 1, Gamma1, numq(1), Gamma2, Gamma3, [ zeros([1 nnum+nden]) ], 0);
R = FWR( eye(2), inv(T)*Gamma4, [1 1], Gamma1*T, [numq(1);0] , inv(T)*Gamma2*T, inv(T)*Gamma3, zeros([1 nnum+nden]), 0);

%myJ = eye(2)
%myK = inv(T)*Gamma4
%myL = [1 1]
%myM = Gamma1*T
%myN = [numq(1);0]
%myP = inv(T)*Gamma2*T
%myQ = inv(T)*Gamma3
%myR = zeros([1 nnum+nden])
%myS = 0

% cf fiche
% Gamma1 et Gamma4 sont changés, par rapport à la forme "en ligne" (en 1
% fois)