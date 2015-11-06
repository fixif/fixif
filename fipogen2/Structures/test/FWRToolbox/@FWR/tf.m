%Purpose:
% Convert a FWR object into a tf object (transfer function)
%
%Syntax:
% H = tf(R,Te)
%
%Parameters:
% H: tf object
% R: FWR object
% Te: period (default=1)
%
% $Id: tf.m 201 2009-01-03 22:31:50Z hilaire $


function H = tf(R,Te)

if nargin==1
    Te=1;
end

H = tf( ss(R.AZ,R.BZ,R.CZ,R.DZ,Te) );


%Description:
%	Give the transfer function of the realization. It is defined with matrices
%	$A_Z$, $B_Z$, $C_Z$ and $D_Z$ (see eq. \eqref{eq:defAZandBZ} and \eqref{eq:defCZandDZ}) by:
%	\begin{equation}
%		H:z\mapsto C_Z \pa{zI_n-A_Z}^{-1}B_Z + D_Z
%	\end{equation}

%See also: <@FWR/ss>, <@FWS/tf>
