function fs = fz2fs(fz,sampleFreqFraction)
%FZ2FS   Inverse bilinear frequency translation
%	fs = FZ2FS(fz) converts the time-discrete frequency(vector) fz to its 
%	corresponding frequency(vector) fs in the time-continuous domain according 
%	to the inverse bilinear transformation rule.
%	fz = 0.25 corresponds with fs = 1.0
% 
%	fs = FZ2FS(fz,sampleFreqFraction), as above, but now sampleFracFraction is 
%	the normalized time-discrete frequency (with Sample frequency = 1) to be 
%	used as the reference: fz = sampleFreqFraction will translate to fs = 1.0

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003

if ~( all(fz >= 0.0) && all(fz < 0.5) )
	error( 'fz should be between 0.0 and 0.5 ...' );
end
if ( nargin == 1 )
	fs = tan(fz*pi);
else
	fs = tan(fz*pi) / tan(pi*sampleFreqFraction);
end
