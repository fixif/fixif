function fz = fs2fz(fs,sampleFreqFraction)
%FS2FZ   Bilinear frequency translation 
%	fz = FS2FZ(fs) converts the time-continuous frequency(vector) fs to its
%	corresponding frequency(vector) fz in the time-discrete domain according
%	to the bilinear transformation rules.
%	fs = 1.0 corresponds with fz = 0.25
% 
%	fz = FS2FZ(fs,sampleFreqFraction), as above, but now sampleFracFraction is 
%	the normalized time-discrete frequency (with Sample frequency = 1) to be 
%	used as the reference, which means that fs = 1.0 will translate to 
%	fz = sampleFracFraction.

% (c) H.J. Lincklaen Arriens, 
%     Delft University of Technology, September 2003

if ( nargin == 1 )
	fz = atan(fs) / pi;
else
	fz = atan( tan(pi*sampleFreqFraction)*fs ) / pi;
end
