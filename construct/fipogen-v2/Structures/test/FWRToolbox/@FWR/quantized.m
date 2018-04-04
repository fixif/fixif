%Purpose:
% Return the quantized realization, according to a fixed-point implementation scheme
%
%Syntax:
% [Rqt, DeltaZ] = quantized( R);
%
%Parameters:
% Rqt: quantized realization (FWR object)
% DeltaZ: approximation on $Z$ (it is NOT $Z-Z^\dagger$ )
% R: FWR object
%
%$Id$


function [Rqt, DeltaZ] = quantized( R)

% FPIS?
if isempty(R.FPIS)
    error( 'The realization must have a valid FPIS');
end

% quantized realization
Rqt=R;
gammaZbis=R.FPIS.gammaZ;
gammaZbis( find(isinf(R.FPIS.gammaZ)) ) = 0;
Rqt = set(Rqt, 'Z', round( R.Z .* (2.^gammaZbis) ) .* (2.^-gammaZbis));

% diff on Z
DeltaZ = 0.5*2.^-gammaZbis .* R.WZ;


%Description:
% 	According to a fixed-point implementation scheme, this function returns the realization with quantized coefficients.
% 	The binary point position of the coefficient depends on the computational scheme (\I{Roundoff Before Multiplication} or \I{Roundoff After Multiplication})
% 	and is given by:
% 	\begin{equation}
% 		\tilde\gamma_Z = \begin{cases}
% 			\gamma_Z & \text{if \I{RAM}}\\
% 			\gamma_{ADD}.\VecOne{1}{l+n+m} - \VecOne{l+n+p}{1}. \begin{pmatrix} \gamma_T \\ \gamma_X \\ \gamma_U \end{pmatrix}^{\hspace{-2mm}\top} & \text{if \I{RBM}}
% 		\end{cases}
% 	\end{equation}
% 	($\gamma_{ADD}$ is the binary point position of the adders, see
% 	\cite{Hila08c} and \funcName[@FWR/setFPIS]{setFPIS}).\\
% 
% 	The new coefficients $Z^\dagger$ are then given by
% 	\begin{equation}
% 		Z^\dagger \triangleq 2^{-\gamma_Z} \left\lfloor Z \times 2^{\gamma_Z} \right\rceil
% 	\end{equation}
% 	and the approximation $\Delta_Z$ on $Z$ is
% 	\begin{equation}
% 		\Delta_Z = \frac{2^{-\gamma_Z}}{2} \times W_Z
% 	\end{equation}

%See also: <@FWR/setFPIS>

%References:
%	\cite{Hila08c} T. Hilaire, D. Ménard, and O. Sentieys. Bit accurate roundoff noise analysis of fixed-point linear controllers. In Proc. IEEE International Symposium on Computer-Aided Control System Design (CACSD'08), September 2008.