
% normalized sensitivity-based pole error

function e = error_pole( R, moduli)

% args
if (nargin<2)
    moduli = 1;
end

%
M1 = [ R.K*inv(R.J) eye(R.n) zeros(R.n,R.p) ];
N1 = [ inv(R.J)*R.M; eye(R.n); zeros(R.m,R.n) ];

%
sigmaZ = 2.^floor(log2(abs(R.Z))) .* R.WZ;
sigmaZ( R.WZ==0 .* isnan(sigmaZ) ) = 0;	% remove NaN (where R.WZ==0)

% measures
[dlambda_dZ, dlk_dZ] = deigdZ( R.AZ, M1, N1, size(R.Z) );
sigma_polek = zeros(1,R.n);
for k=1:R.n
    sigma_polek(k) = norm( dlk_dZ(:,:,k) .* sigmaZ, 'fro' )^2;
end

%
[Mx,Dlambda] = eig(R.AZ);
My = inv(Mx)';
lambda=diag(Dlambda)';
omegak = 1./(1-abs(lambda));

e = sum( sigma_polek.*omegak);
