function Hw = evalHs(Hs,omega)
%EVALHS	  Evaluate H(s) for s = j*omega
%	Hw = EVALHS(Hs,omega) evaluates Hs for the given omega.
%
% 	See also EVALHZ, PLOTHS, PLOTHZ.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, October 2005

jw  = j * omega;
nHs = length(Hs);
Hw  = zeros(nHs,length(omega));
for i = 1:nHs
	poly_fs = Hs(i).poly_fs;
	poly_gs = Hs(i).poly_gs;
	if ~iscell(poly_fs)
		Hw(i,:) = polyval(poly_fs,jw) ./ polyval(poly_gs,jw);
	else
		nUnitElements = poly_fs{2};
		poly_fs       = poly_fs{1};
		% each Unit Element needs an additional multiplication with sqrt(1+w^2),
		mulFac = (1 + w.^2) .^ (nUnitElements/2);
		Hw(i,:) = polyval(poly_fs,jw) .* mulFac ./ polyval(poly_gs,jw);
	end
end
