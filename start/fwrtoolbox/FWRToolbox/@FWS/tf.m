%Purpose:
% Convert a FWS object into a tf object (transfer function)
%
%Syntax:
% H = tf(S,Te)
%
%Parameters:
% H: tf object
% S: FWS object
% Te: period (default=1)
%
% $Id: tf.m 204 2009-01-05 09:39:04Z hilaire $


function H = tf(S,Te)

if nargin==1
    Te=1;
end

H = tf( S.R,Te );

%Description:
%	Give the transfer function of the realization. The current realization (\matlab{R}) is considered.\\
%	It is defined with matrices $A_Z$, $B_Z$, $C_Z$ and $D_Z$ (see eq. \eqref{eq:defAZandBZ} and \eqref{eq:defCZandDZ}) by:
%	\begin{equation}
%		H:z\mapsto C_Z \pa{zI_n-A_Z}^{-1}B_Z + D_Z
%	\end{equation}

%See also: <@FWS/ss>, <@FWR/tf>