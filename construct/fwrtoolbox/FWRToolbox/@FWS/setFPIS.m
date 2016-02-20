%Purpose:
% Set the Fixed-Point Implementation Scheme (FPIS) of an FWS object
% (the wordlength may be a matrix or scalar. The scalar case is used to set all the wordlength to the same length)
% 
%Syntax:
% S = setFPIS( S, betaU, Umax, betaZ, betaT, betaX, betaY, betaADD, betaG, method );
% S = setFPIS( S, FPIS);
% S = setFPIS( S, FPISname,Umax);
%
%Parameters:
% S: FWS object
% FPIS: an other Fixed-Point Implementation Scheme (a structure with betaU, Umax, betaZ, betaT, betaX, betaY, betaADD, betaG and method)
% FPISname : "DSP8" or "DSP16"
% betaU: wordlength of $U$ (inputs)
% Umax: maximum value of $U$ (necessary to set gammaU)
% betaZ: wordlength of the coefficients
% betaT, betaX, betaY: wordlength of the intermediate variables $T$, the states $X$ and the outputs
% betaADD: wordlength of the accumulators
% betaG: nb of guard bits in the accumulators
% method: "RBM" (default) Roundoff Before Multiplication
%       : "RAM" Roundoff After Multiplication
%
% $Id$


function S = setFPIS( S, varargin )

S.Rini= setFPIS( S.Rini, varargin{:} );
S.R = setFPIS( S.R, varargin{:} );


%Description:
% 	This function sets the Fixed-Point Implementation Scheme (FPIS) of an FWS object. It means that all the associated realization (\matlab{Rini} and \matlab{R}) whill have the same FPIS (the values can changed).

%See also: <@FWR/setFPIS>

%References:
%\cite{Hila08c} T. Hilaire, D. Ménard, and O. Sentieys. Bit accurate roundoff noise analysis of fixed-point linear controllers. In Proc. IEEE International Symposium on Computer-Aided Control System Design (CACSD'08), September 2008.

