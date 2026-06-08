function Hz = Hs2Hz(Hs)
%HS2HZ Conversion of transfer function from s- to z-domain.
%	Hz = HS2HZ(Hs) converts the continuous-time transfer function(s) H(s)
%	to its corresponding discrete-time transfer function(s) H(z) using 
%	the bilinear transformation, such, that the frequency 1.0 of H(s) 
%	translates into the normalized discrete frequency 0.25 of H(z).
%                              z - 1
%	Thus, replace s with  s = -------.
%                              z + 1
% 	Hs should be entered as the structure described in e.g. Hs_butter, 
% 	resulting in the structure Hz:
%		Hz.poly_fz         -- the coefficients of the numerator function
%		Hz.poly_gz         -- the coefficients of the denominator function
%		Hz.ident           -- a string, describing the filter
%		Hz.roots_fz        -- the roots of the numerator 
%		Hz.roots_gz        -- the roots of the denominator
%	In the above, Hs.poly_fs and Hs.poly_gs are vectors of coefficients in
%	descending powers of s (N,N-1,...,2,1,0), while
%	Hz.poly_fz and Hz.poly_gz are vectors of coefficients in either 
%	descending positive powers of z (N,N-1,...,2,1,0), or 
%	ascending negative powers of z (0,-1,-2,...,-(N-1),-N).
% 	If more than one polynomial function is to be transformed,
% 	Hs has to be entered as a vector e.g. [Hs1 Hs2]. 
% 	Then Hz will become [Hz1 Hz2].
% 	In case Unit Elements are involved, Hs.poly_fs has to be given 
%	as the cell array { poly_fs without UEs; number of UEs }
%	while Hz.poly_fz will be returned as 
%				 	  { poly_fz without UEs; number of UEs }. 

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003


nHs = length(Hs);

for i = 1:nHs
	poly_fs = Hs(i).poly_fs;
	poly_gs = Hs(i).poly_gs;
	% pre-warping needed to maintain cutOffFrequency <-> sampleFrequency ratio
	if ~iscell(poly_fs)
		[poly_fz,poly_gz] = lfs2z_bilin(poly_fs,poly_gs);
		roots_fz = roots(poly_fz);
	else
		nUnitElements   = poly_fs{2};
		poly_fsq        = poly_fs{1};
		[poly_fzq,poly_gz] = lfs2z_bilin(poly_fsq,poly_gs);
		poly_fz  = { poly_fzq; nUnitElements };
		roots_fz = { roots(poly_fzq); nUnitElements };
	end
	Hz(i).poly_fz  = poly_fz;
	Hz(i).poly_gz  = poly_gz;
	Hz(i).ident    = Hs(i).ident;
	Hz(i).roots_fz = roots_fz;
	Hz(i).roots_gz = roots(poly_gz);
end



%====================================================================================
%======  Local functions  ===========================================================
%====================================================================================

function [fz,gz] = lfs2z_bilin(fs,gs)
%                                          z - 1
% perform the bilinear transformation s = -------
%                                          z + 1
% given the two polynomials fs and gs
%
% Huib, Jan 2003

  % get highest order of the input polynomials + 1
  N1 = max(length(fs),length(gs));
  % compute all possible convolutions (z+1)^m * (z-1)^(N-m) for m=0:N
  % resulting from the s -> z bilinear transformation
  % powers of (z+1)
  zp1 = zeros(N1,N1);
  for m = 1:N1
  	  coefs = diag(fliplr(pascal(N1)),(N1-m))';  
  	  zp1(m,:) = [coefs zeros(1,N1-length(coefs))];
  end
  % powers of (z-1)
  pmv = ones(N1,N1);
  pmv(2:2:end,1:2:end) = -1;  % even columns, odd rows
  pmv(1:2:end,2:2:end) = -1;  % odd columns, even rows
  zm1 = flipud(pmv.*zp1);
  % compute the combinations
  pcm = zeros(N1,2*N1-1);
  for i = 1:N1
  	  pcm(i,:) = conv(zp1(i,:),zm1(i,:));
  end
  pcm = fliplr(pcm(:,1:N1));

  % compute the resulting polynomials
  % DIM (=1) should be specified to prevent a vector to be summed! (e.g. if fs=1)
  fz = sum( pcm(N1+1-length(fs):end,:) .* (fs(:)*ones(1,N1)) ,1 );
  gz = sum( pcm(N1+1-length(gs):end,:) .* (gs(:)*ones(1,N1)) ,1 );
  % normalize to gz(1) = 1
  fz = fz/gz(1); 
  gz = gz/gz(1);
  