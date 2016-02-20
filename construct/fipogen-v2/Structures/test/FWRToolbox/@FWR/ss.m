%Purpose:
% Convert a FWR object into a ss (state-space) object (equivalent state-space)
%
%Syntax:
% S = ss(R,Te)
%
%Parameters:
% S: ss object
% R: FWR object
% Te: period (default=1)
%
% $Id: ss.m 201 2009-01-03 22:31:50Z hilaire $


function S = ss(R,Te)

if nargin==1
    Te=1;
end

S = ss(R.AZ,R.BZ,R.CZ,R.DZ,Te);


%Description:
%	Give the equivalent state-space (\matlab{ss} object). It is defined with matrices
%	$A_Z$, $B_Z$, $C_Z$ and $D_Z$ (see eq. \eqref{eq:defAZandBZ} and \eqref{eq:defCZandDZ}).
%
%Example:
%	\matlab{>>bode(ss(R));}\\ where \matlab{R} is a FWR object, allows to plot its Bode frequency response.
%
%See also: <@FWR/tf>, <@FWS/ss>