%Purpose:
% Convert a FWS object into a ss (state-space) object (equivalent state-space)
%
%Syntax:
% Sys = ss(S,Te)
%
%Parameters:
% Sys: ss object
% S: FWS object
% Te: period (default=1)
%
% $Id: ss.m 204 2009-01-05 09:39:04Z hilaire $


function Sys = ss(S,Te)

if nargin==1
    Te=1;
end

Sys = ss(S.R,Te);


%Description:
%	Give the equivalent state-space (\matlab{ss} object). The current realization (\matlab{R}) is considered.\\
%	It is defined with matrices
%	$A_Z$, $B_Z$, $C_Z$ and $D_Z$ (see eq. \eqref{eq:defAZandBZ} and \eqref{eq:defCZandDZ}).

%See also: <@FWR/ss>