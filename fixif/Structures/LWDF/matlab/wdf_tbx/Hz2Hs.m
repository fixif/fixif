function Hs = Hz2Hs(Hz)
%HZ2HS Conversion of transfer function from z- to s-domain.
%	Hs = HZ2HS(Hz) converts the discrete-time transfer function(s) H(z)
%	to its corresponding continuous-time transfer function(s) H(s) using 
%	the inverse bilinear transformation, such, that the discrete frequency 
%	0.25 of H(z) translates into the normalized frequency 1.0 of H(s).
%                                s - 1
%	Thus, replace z with  z = - -------.
%                                s + 1
% 	Hz should be entered as a structure according to 
%		Hz.poly_fz         -- the coefficients of the numerator function
%		Hz.poly_gz         -- the coefficients of the denominator function
%		Hz.ident           -- a string, describing the filter
%		Hz.roots_fz        -- the roots of the numerator 
%		Hz.roots_gz        -- the roots of the denominator
%	where Hz.poly_fz and Hz.poly_gz are vectors of coefficients in either 
%	descending positive powers of z (N,N-1,...,2,1,0), or 
%	ascending negative powers of z (0,-1,-2,...,-(N-1),-N).
%	The conversion will return a structure Hs (see p.e. Hs_Butter.m).
% 	If more than one polynomial function is to be transformed,
% 	Hz has to be entered as a vector e.g. [Hz1 Hz2], resulting in [Hs1 Hs2].
% 	In case Unit Elements are involved, Hz.poly_fz has to be given 
%	as the cell array { poly_fz without UEs; number of UEs }
%	while Hs.poly_fs will be returned as 
%				 	  { poly_fs without UEs; number of UEs }. 

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003


nHz = length(Hz);
for i = 1:nHz
	poly_fz = Hz(i).poly_fz;
	poly_gz = Hz(i).poly_gz;
	% pre-warping needed to maintain cutOffFrequency <-> sampleFrequency ratio
	if ~iscell(poly_fz)
		[poly_fs,poly_gs] = lfz2s_bilin(poly_fz,poly_gz);
		roots_fs = roots(poly_fs);
	else
		nUnitElements   = poly_fz{2};
		poly_fzq        = poly_fz{1};
		[poly_fsq,poly_gs] = lfz2s_bilin(poly_fzq,poly_gz);
		poly_fs  = { poly_fs; nUnitElements };
		roots_fs = { roots(poly_fsq); nUnitElements };
	end
	Hs(i).poly_fs  = poly_fs;
	Hs(i).poly_gs  = poly_gs;
	Hs(i).ident    = Hz(i).ident;
	Hs(i).roots_fs = roots_fs;
	Hs(i).roots_gs = roots(poly_gs);
end



%====================================================================================
%======  Local functions  ===========================================================
%====================================================================================

function [fs,gs] = lfz2s_bilin(fz,gz)
%                                                    s - 1
% perform the inverse bilinear transformation z = - -------
%                                                    s + 1
% given the two polynomials fz and gz
%
% Huib, Oct 2003

  % 
  N = length(fz);
  if ( length(gz) ~= N )
  	error( 'Numerator and denominator polynomials differ in length ...' );
  end

  % compute all possible convolutions (S+1)^m * (S-1)^(N-m) for m=0:N
  % resulting from the z -> S inverse bilinear transformation (S=Ts/2)
  % powers of (S+1)
  Sp1 = zeros(N,N);
  for m = 1:N
  	  coefs = diag(fliplr(pascal(N)),(N-m))';  
  	  Sp1(N-m+1,:) = [coefs zeros(1,N-length(coefs))];
  end
  % powers of (S-1), note that odd powered terms of z become negative
  % if we take care for that here, pmv becomes very simple
  pmv = ones(N,N);
  pmv(:,2:2:end) = -1;
  Sm1 = flipud(pmv.*Sp1);
  % compute the combinations
  pcm = zeros(N,2*N-1);
  for i = 1:N
  	  pcm(i,:) = conv(Sp1(i,:),Sm1(i,:));
  end
  % take input parameter T into account
%  pcm = ((T/2).^(N-1:-1:0)')*ones(1,N) .* fliplr(pcm(:,1:N));
  pcm = fliplr(pcm(:,1:N));
  % compute the resulting polynomials
  fs = sum( pcm .* (fz(:)*ones(1,N)) );
  gs = sum( pcm .* (gz(:)*ones(1,N)) );
  % round small residues of f(s) to zero and remove trailing zeros 
  fs( abs(fs) < 1e-14 ) = 0;
  while ( fs(1) == 0 )
    fs = fs(2:end);
  end 
  % normalize to gs(1) = 1
  fs = fs/gs(1); 
  gs = gs/gs(1);
