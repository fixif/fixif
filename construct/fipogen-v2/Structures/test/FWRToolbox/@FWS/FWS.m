%Purpose:
% Constructor of the FWS class.
% A structuration is characterized by an initial realization and a 'way' to transform this realization
%
%Syntax:
% S = FWS(Rini, UYWfun, Rfun, dataFWS, param1Name, param1Value, param2Name, param2Value, ...)
%
%Parameters:
% S: FWS object
% Rini: initial realization (FWR object)
% UYWfun: handle to a function that links the parameters to the transformation matrices U,Y and W
% Rfun : handle to a function that links the parameters to the new realization
%	   : only ONE of these two functions must be provided
% dataFWS: cells of extra datas 
% paramName: parameters' names
% paramValue: initial value for the parameters
%
% $Id: FWS.m 207 2009-01-05 13:03:51Z fengyu $


function S = FWS(Rini, UYWfun, Rfun, dataFWS, varargin)

% fields
S.Rini = Rini;
S.UYWfun = UYWfun;
S.Rfun = Rfun;
S.R = Rini;

% params
n=length(varargin);
S.paramsName = varargin(1:2:n-1);
pValue = varargin(2:2:n);
S.indices = zeros(n/2+1,1);
j=0;
for i=1:n/2
    S.indices(i) = j+1;
    if i<n/2+1
		j = j + prod( size(pValue{i}) );
	end
	S.paramsValue( S.indices(i):j ) = reshape( pValue{i}, [1 prod( size(pValue{i}) )] );
	S.paramsSize(i,:) = size(pValue{i});
end
S.indices(i+1) = j+1;

% extra datas for FWL measure
S.dataMeasure = [];

% extra datas for the structuration
S.dataFWS = dataFWS;

% build the class
S = class( S, 'FWS');

% update R
S.R = updateR(S);


%Description:
% 	This function is called to construct a FWS object.\\
% 	Only one of the two functions \matlab{UYWfun} \matlab{Rfun} must be given (a handle to a function is defined by \matlab{@} + \matlab{name of the function} - see Matlab's documentation for more informations on function's handle).\\
% 	These functions must satisfy the specifications explain in section \ref{sec:FWSclass}.\\ 
% 	The names and values of each parameter are given by pair.
% 
%Example:
% 	Let us consider a state-space realization $(A,B,C,D)$.\\
% 	The equivalent realizations are given by the state-space $(T^{-1}AT,T^{-1}B,CT,D)$. This correspond to the following SIF
% 	\begin{equation}
% 		Z = 
% 		\begin{pmatrix}
% 			. & . & . \\
% 			. & A_q & B_q \\
% 			. & C_q & D_q
% 		\end{pmatrix}
% 	\end{equation}
% 	and the $\mt{Y}\mt{U}\mt{W}$ transformation with $\mt{U}=T$, $\mt{Y}=\mt{W}=I_{l}$.
% 
% 	Then, to create a state-space structuration, from matrices \matlab{A}, \matlab{B}, \matlab{C} and \matlab{D},
% 	with a parameter \matlab{T}, one should create a UYWfun like
% 	\begin{verbatim}
% 	% UYW function for the classical state-space structuration
% 	function [U,Y,W,cost_flag] = UYW_SS( Rini, paramsValue, dataFWS)
% 
% 	%test if T is singular    
% 	if (cond(paramsValue{1})>1e10)
% 		cost_flag=0;
% 		paramsValue{1} = eye(size(paramsValue{1}));
% 	else
% 		cost_flag=1;
% 	end
% 
% 	% compute U,W,Y
% 	Y = eye(0);
% 	W = eye(0);
% 	U = paramsValue{1};
% 	\end{verbatim}
% 	The \matlab{cost\_flag} could return $0$ if the paramsValue proposed is not acceptable (here a non-invertible matrix).\\
% 	Then the structuration is created by
% 	\begin{verbatim}
% 	Rini =  SS2FWR(A,B,C,D);
% 	S = FWS( Rini, @UYW_SS, [], [], 'T', eye(R.n));
% 	\end{verbatim}
% 	(there is no need for a \matlab{dataFWS}).
% 
% 	Even if it is not preferrable, it is also possible to create this FWS with a \matlab{Rfun} function.\\
% 	So a function that creates a new state-space realization from the \matlab{paramsValue} is needed
% 	\begin{verbatim}
% 	% UYW function for the classical state-space structuration
% 	function [R,cost_flag] = Rfun_SS( Rini, paramsValue, dataFWS)
% 
% 	%test if T is singular    
% 	if (cond(paramsValue{1})>1e10)
% 		cost_flag=0;
% 		paramsValue{1} = eye(size(paramsValue{1}));
% 	else
% 		cost_flag=1;
% 	end
% 
% 	% compute the new realization
% 	T = paramsValue{1};
% 	R = SS2FWR( inv(T)*Rini.P*T, inv(T)*Rini.Q, Rini.R*T, Rini.S );
% 	\end{verbatim}
% 	and the FWS object is defined by
% 	\begin{verbatim}
% 	Rini =  SS2FWR(A,B,C,D);
% 	S = FWS( Rini, [], @Rfun_SS, [], 'T', eye(R.n));
% 	\end{verbatim}
% 	In that case, the optimization process will have to compute for each iteration a new realization (with the \matlab{Rfun} function)
% 	and then compute the associated FWL measure; whereas in the first case, the FWL measure is directly compute from the $\mt{U}$,
% 	$\mt{Y}$, $\mt{W}$ matrices.

%See also: <@FWR/FWR>