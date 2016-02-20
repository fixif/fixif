%Purpose:
% Perform a UYW-transformation (similarity on Z)
%
%Syntax:
% R = transform(R, U, Y, W)
%
%Parameters:
% R: FWR object
% U,Y,W : transformation matrices
%
% $Id: transform.m 201 2009-01-03 22:31:50Z hilaire $


function R = transform(R, U, Y, W)

invU=inv(U);

R.J = Y*R.J*W;
R.K = invU*R.K*W;
R.L = R.L*W;
R.M = Y*R.M*U;
R.N = Y*R.N;
R.P = invU*R.P*U;
R.Q = invU*R.Q;
R.R = R.R*U;
R.S = R.S;
R = computeZ(R);

R.AZ = invU*R.AZ*U;
R.BZ = invU*R.BZ;
R.CZ = R.CZ*U;
R.Wc = invU * R.Wc * invU';
R.Wo = U' * R.Wo * U;

R = compute_rZ(R);


%Description:
% 	The $\mt{U}\mt{Y}\mt{W}$-transformation is defined as a particular similarity on $Z$:
% 	\begin{equation}
% 		\tilde{Z} =
% 		\begin{pmatrix}
% 			\mt{Y}\\
% 			&\mt{U}^{-1}\\
% 			&&I_{p}
% 		\end{pmatrix}
% 		Z
% 		\begin{pmatrix}
% 			\mt{W}\\
% 			&\mt{U}\\
% 			&&I_{m}
% 		\end{pmatrix}
% 	\end{equation}
% 	where $\mt{U}$, $\mt{W}$, $\mt{Y}$ are non-singular matrices, are
% 	equivalent to $\mathcal{R}$.

% TODO : what about WJ to WS (WZ and rZ also) ??