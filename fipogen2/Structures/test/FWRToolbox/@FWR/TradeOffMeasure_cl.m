%Purpose:
% Compute a (pseudo) tradeoff closed-loop measure
% with the MsensH_cl, MsensPole_cl, RNG_cl
% 
%Syntax:
% M = TradeOffMeasure_cl( R, Sysp, MH, MP, MRNG)
%
%Parameters:
% M: measure value
% R: FWR object
% Sysp: plant system ('ss' object)
% MH,MP,MRNG: optimal value of the MsensH_cl, MsensPole_cl and RNG_cl measure
%
% $Id: TradeOffMeasure_cl.m 207 2009-01-05 13:03:51Z fengyu $


function M = TradeOffMeasure_cl( R, Sysp, MH, MP, MRNG)

M = (MsensH_cl(R,Sysp)/MH) + (MsensPole_cl(R,Sysp)/MP) + (RNG_cl(R,Sysp)/MRNG);


%Description:
% 	Even if a tradeoff measure like this one is not the best solution to multi-objective optimal realization, it is interesting to look for a realization that is \I{good enough} for the three measures $\bar{M}_{L_2}^W$, $\bar{\Psi}$ and $\bar{G}$.
% 	This (pseudo) tradeoff measure is defined by
% 	\begin{equation}
% 		\bar{TO}(Z) \triangleq \frac{\bar{M}_{L_2}^W(Z)}{\bar{M}_{L_2}^{W\ opt}} + \frac{\bar{\Psi}(Z)}{\bar{\Psi}^{opt}} + \frac{\bar{G}(Z)}{\bar{G}^{opt}}
% 	\end{equation}
% 	where $\bar{M}_{L_2}^{W\ opt}$, $\bar{\Psi}^{opt}$ and $\bar{G}^{opt}$ are the optimal values for these respective measures.

%See also: <@FWR/MsensH_cl>, <@FWR/MsensPole_cl>, <@FWR/RNG_cl>

%References:
%	\cite{Hila08b} T. Hilaire, P. Chevrel, and J. Whidborne. Finite
%	wordlength controller realizations using the specialized implicit form. Technical Report RR-6759, INRIA, 2008.