%Purpose:
% Compute the $A_Z$, $B_Z$, $C_Z$ and $D_Z$ matrices and the gramians of a FWR object
%
%Syntax:
% R=updateAZBZCZDZWoWc(R)
%
%Parameters:
% R: FWR object
%
%
% $Id$

function R=computeAZBZCZDZWoWc(R)

R.AZ = R.K*inv(R.J)*R.M + R.P;
R.BZ = R.K*inv(R.J)*R.N + R.Q;
R.CZ = R.L*inv(R.J)*R.M + R.R;
R.DZ = R.L*inv(R.J)*R.N + R.S;
%try
	%modif pour interval
	%if ( (isintval(R.AZ)==1)  )		%TODO: vérifier aussi sur les autres matrices BZ, CZ et DZ
	%	R.Wc = vermatreqn( R.AZ, R.AZ', -eye(R.n), eye(R.n),  -R.BZ*R.BZ');
	%	R.Wo = vermatreqn( R.AZ', R.AZ, -eye(R.n), eye(R.n), -R.CZ'*R.CZ);
	%else
	    R.Wc = gram( ss(R), 'c');
    	R.Wo = gram( ss(R), 'o');
    %end
%catch
    %[lastmsg, lastid] = lasterr;
    %warning( lastmsg);
%end

%Description:
% 	\begin{center}\I{Internal function}\end{center}
% 	Compute the matrices $A_Z$, $B_Z$, $C_Z$, $D_Z$ and the controllability and observability gramians associated with a FWR object.\\
% 	$A_Z\in\Rbb{n}{n}$, $B_Z\in\Rbb{n}{m}$, $C_Z\in\Rbb{p}{n}$ and $D_Z\in\Rbb{p}{m}$ are given by:
% 	\begin{align}
% 		A_Z &= KJ^{-1}M+P,   &  B_Z &= KJ^{-1}N+Q, \\	
% 		C_Z &= LJ^{-1}M+R, &  	D_Z &= LJ^{-1}N+S.
% 	\end{align}
% 	and the gramians are the solutions to the Lyapunov equations
% 	\begin{eqnarray}
% 		W_c &=& A_Z W_c A_Z^\top + B_Z B_Z^\top \\
% 		W_o &=& A_Z^\top W_o A_Z + C_Z^\top C_Z
% 	\end{eqnarray}

