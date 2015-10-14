%Purpose:
% Compute the matrix $r_Z$
%
%Syntax:
% R = compute_rZ(R)
%
%Parameters:
% R: FWR object
%
%
% $Id: compute_rZ.m 207 2009-01-05 13:03:51Z fengyu $

function R = compute_rZ(R)

% fp
if (R.fp==1)
    R.rZ = R.WZ;
else
    % block
    switch (R.block)
        case 1 % full
            eta = max(abs(R.Z(:)))*ones(size(R.Z));
        case 2 % natural
            eta.J = maxi(R.J);
            eta.K = maxi(R.K);
            eta.L = maxi(R.L);
            eta.M = maxi(R.M);
            eta.N = maxi(R.N);
            eta.P = maxi(R.P);
            eta.Q = maxi(R.Q);
            eta.R = maxi(R.R);
            eta.S = maxi(R.S);
            eta = [ R.J R.M R.N; R.K R.P R.Q; R.L R.R R.S];
        case 3 % none
            eta = abs(R.Z);
    end
    R.rZ = 2 * eta .* R.WZ;
end


% maxi of a matrix, but we take care of empty matrix...
function M = maxi(m)
    if (isempty(m))
        M = zeros(size(m));  % don't care of the max in this case
    else
        M = max(abs(m(:)))*ones(size(m));
	end

	
%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	During the quantization process, $Z$ is perturbed to $Z+r_Z\times\Delta$ where
% 	\begin{equation}
% 		r_Z \triangleq
% 		\begin{cases}
% 			W_Z & \text{for fixed-point representation,} \\
% 			2\eta_Z \times W_Z & \text{for floating-point representation,}
% 		\end{cases}
% 	\end{equation}
% 	and $\eta_Z$ is such that
% 	\begin{equation}
% 		\pa{\eta_Z}_{i,j} \triangleq
% 			\left\lbrace\begin{array}{l}
% 				\text{the largest absolute value of}\\
% 				\text{the block in which }  Z_{i,j} \text{ resides.}
% 			\end{array}\right.
% 	\end{equation}
% 
% 	This function considers the \matlab{fp} and \matlab{block} records of the FWR class, and $r_Z$ is built according to the fixed-point or floating-point and the possible block representations \cite{Hila07b}.


%References:
%\cite{Hila07b} T. Hilaire, P. Chevrel, and J. Whidborne. A unifying framework for finite wordlength realizations. IEEE Trans. on Circuits and Systems, 8(54), August 2007.