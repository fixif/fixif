function HfFs = evalHz(Hz,fFs)
%EVALHZ	  Evaluate H(z) for z = exp(j*2pi*fFs)
%	HfFs = EVALHZ(Hz,fFs) evaluates Hz for the given fFs,
%	where fFs is the frequency relative to the sample frequency ( 0 to 0.5 ).
%
% 	See also EVALHS, PLOTHS, PLOTHZ.
%
%	Warning: When a fairly large number of Unit Elements are being used, the 
%			 accuracy of the output data for normalized frequency values near 
%			 0.5 may deteriorate.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, October 2005

z = exp(j*2*pi*fFs);

nHz  = length(Hz);
Hpsi = zeros(nHz,length(fFs));

for i = 1:nHz
	poly_fz = Hz(i).poly_fz;
	poly_gz = Hz(i).poly_gz;
	if ~iscell(poly_fz)
		Hpsi(i,:) = polyval(poly_fz,z) ./ polyval(poly_gz,z);
	else
		nUnitElements = poly_fz{2};
		poly_fz       = poly_fz{1};
		% each Unit Element needs an additional multiplication with sqrt(1-W^2),
		%            2   z - 1
		% where W = ---.-------   and T is the sample period. 
		%            T   z + 1
		% According to our definitions, we always use T = 2 (fs=1.0 <==> fz=0.25).
		% Note: for w -> pi, W -> j*infinite, but this should be overruled by
		%       H(z) -> 0
		%       If no special action is taken, problems would arise for 
		%       nUnitElements larger than about 6
%		W = (z - 1)./(z + 1);   	% NOTE: ought to be purely imaginary
%		mulFac = (1 - W.^2) .^ (nUnitElements/2);
% mulFac can be simplified to:
		mulFac = ( 2 ./ (1 + cos(w) ) ) .^ (nUnitElements/2);
		if ( all( mulFac < 1e15 ) )
			Hpsi(i,:) = polyval(poly_fz,z) .* mulFac ./ polyval(poly_gz,z);
		else
			Hp = abs(polyval(poly_fz,z) ./ polyval(poly_gz,z));
			ix = find( mulFac < 1e15);
			ixOK = ix(end);
			% limit problematic data to constant values
			Hp( ixOK+1:end )     = Hp(ixOK);
			mulFac( ixOK+1:end ) = mulFac(ixOK);
			Hpsi(i,:) = Hp .* mulFac;;
		end
	end
end

HfFs = Hpsi;

