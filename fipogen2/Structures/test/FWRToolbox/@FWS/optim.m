%Purpose:
% Find the optimal realization, according to the 'measureFun' measure, in the set of structured equivalent realizations
%
%Syntax:
% S = optim( S, options, measureFun, ...)
%
%Parameters:
% S: FWS object
% options: cells of pairs (string/value) to define the options of the optimization
%        :   { "param1", value1, "param2", value2 }
%        : - 'method' : "newton" (default), "simplex" or "ASA"
%		 :		"newton" refers to the Quasi-Newton algorithm used by fminunc and fmincon
%		 :		"simplex" refers to the simplex algorithm used by fminsearch
%		 : 		and "ASA" refers to the Annealed Simulated Algorithm
%        : - "l2scaling" : "no" (default) ,"yes" or "relaxed"
%        : - "useFWSmeasure" : "yes" (default) or "no"
%		 : - "fixedParameter" : a parameter to be fixed during optimization
%		 : - "matFileName" : filename of the mat-file created to store the result
%		 :		(default) : measureFun + funName + date
%		 :		[ ] : no mat-file is created
%		 :		if ASA method is used, the name is also used for the log-file
%		 : - "MinMax" : scalar that fix the maximum value for the
%		 parameters (min=-max)
%		 : - "Min" and "Max" : used to fix individually the min and max values. The values of "Min" and "Max" may have the same size as the parameters
%        : - the other string/values are given to the fminsearch/ASA function
% measureFun: handle to the measure function
% ...: the extra parameters are given to the measure function
%
% $Id$

function S = optim( S, options, measureFun, varargin)

% retrieve options
if mod(length(options),2)~=0
    error('options must be a cells of pair string/value')
end
% method
method = indexValue( options, 'method', {'newton', 'simplex', 'ASA'}, 1);
useFWSMethod = indexValue( options, 'useFWSmeasure', {'no','yes'}, 2) - 1;
% parameters
matFileName = optionValue(options,'matFileName',0);
%l2scaling
l2scaled = indexValue( options, 'l2scaling', {'no','yes', 'relaxed','relaxed2'}, 1) - 1;
Umax = optionValue(options,'Umax',1);
delta = optionValue(options,'delta',1);
if ~isempty(S.R.FPIS)
	Umax=S.R.FPIS.Umax;
end

S.dataMeasure=[];


% test if the measure is a FWS's method or a FWR's method
if useFWSMethod
    try
        U = eye(S.R.n); Y = eye(S.R.l); W = Y;
        M = feval( measureFun, S, U,Y,W, varargin{:} );
    catch
        disp(lasterr)
        M = feval( measureFun, S.Rini, varargin{:} );
        useFWSMethod=0;
    end
end
% test if the FWS has a UYWfunction
if isempty(S.UYWfun)
    useFWSMethod = 0;
    funName = func2str(S.Rfun);
else
    funName = func2str(S.UYWfun);
end
% disply method used
if useFWSMethod
    disp( ['The measure FWS/' func2str(measureFun) ' is used'])
else
    disp( ['The measure FWR/' func2str(measureFun) ' is used'])
end

% fixed parameters
var = optionValue(options,'fixedParameter',[]);
freeparams = 1:S.indices(end)-1;
while ~isempty(var)
	% find the variable in the list
	try
		[p num] = pnmatch( var, S.paramsName);
	catch
		warning([ var ' is not a valid parameter to be fixed']);
	end
	% remove corresponding indices
	freeparams( find( freeparams >=S.indices(num) & freeparams<S.indices(num+1) ) ) = [];
	% find next
	var = optionValue(options,'fixedParameter',[]);
end


% xini
xini(1:length(freeparams)) = S.paramsValue(freeparams);
if l2scaled==2
	xini( S.indices(end):S.Rini.l+S.Rini.n+S.indices(end)-1 ) = 3.99*ones( 1,S.Rini.l+S.Rini.n);
end	

% xupper, xlower
if l2scaled==2
	if isempty(S.R.FPIS)
		alphaX = - ( log2(Umax) - floor(log2(Umax)) )*ones(S.R.n,1);
		alphaT = - ( log2(Umax) - floor(log2(Umax)) )*ones(S.R.l,1);
	else
		alphaX = R.FPIS.betaX - ( R.FPIS.betaU + log2(Umax) - floor(log2(Umax)) )*ones(S.R.n,1);
		alphaT = R.FPIS.betaT - ( R.FPIS.betaU + log2(Umax) - floor(log2(Umax)) )*ones(S.R.l,1);
	end	
	xupL2 = [ (4*2.^(2*[alphaT;alphaX])/delta^2)' ];
	xloL2 = [ (2.^(2*[alphaT;alphaX])/delta^2)' ];
else
	xupL2 = [];
	xlowL2= [];
end

boundedparameters=0; %count the numbers of options 'MinMax', 'Min' and 'Max'
if method==3
	[xmax, bp] = optionValue(options, 'MinMax', 1e4);
	xmax = xmax  * ones( 1,length(freeparams) );
	xmin = -xmax;
	boundedparameters = boundedparameters + bp;
else
	[xmax, bp] = optionValue(options, 'MinMax', Inf);
	xmax = xmax * ones( 1,length(freeparams) );
	xmin = -xmax;
	boundedparameters = boundedparameters + bp;
end
[xmax, bp] = optionValue(options,'Max',xmax);
boundedparameters = boundedparameters + bp;
[xmin, bp] = optionValue(options,'Min',xmin);
boundedparameters = boundedparameters + bp;
xupper = [ xmax xupL2 ];
xlower = [ xmin xupL2 ];


	
% optimization
if method == 3
    % ASA method
    myoptions_asamin;
	if ~isempty(matFileName)
		if isstr(matFileName)
			asamin('set','asa_out_file',matFileName);
		else
			asamin('set','asa_out_file',['optim_' func2str(measureFun) '_' funName '_' date '.log']);
		end
	end	
    xt = -ones(size(xini));
	%TODO : ˆ changer !!!
	

    if ~isempty( options )
        asamin(options{:});
    end
    
    [Mopt, xstar, grad, hessian, state] = asamin(	'minimize', 'genCostFunction', ...
													xini', xlower', xupper', xt', ...
													S, freeparams, useFWSMethod, ...
													l2scaled, Umax, delta, ...
													measureFun, varargin{:} );
elseif method == 2
    %fminsearch method
    opt = optimset('TolX',1e-5,'TolFun',1e-8);
    opt = optimset(opt,options{:});
	if l2scaled==2 | l2scaled==3
		error('relaxed L2-scaling is not possible with simplex method...');
	end
	[xstar, Mopt ] = fminsearch(	@genCostFunction, xini, opt, ...
									S, freeparams, useFWSMethod, ...
									l2scaled, Umax, delta, ...
									measureFun, varargin{:} );
	
elseif method == 1
	% fminunc or fmincon
	opt = optimset('TolX',1e-5,'TolFun',1e-8);
    opt = optimset(opt,options{:});
	if l2scaled==2 || boundedparameters
		[xstar, Mopt ] = fmincon(	@genCostFunction, xini, ...
									[],[],[],[], xlower, xupper, ...
									[], opt, S, freeparams, useFWSMethod, ...
									l2scaled, Umax, delta, ...
									measureFun, varargin{:} );
	else
		[xstar, Mopt ] = fminunc(	@genCostFunction, xini, opt, ...
									S, freeparams, useFWSMethod, ...
									l2scaled, Umax, delta, ...
									measureFun, varargin{:} );
	end
end


% store results in S
S.paramsValue(freeparams) = xstar(1:length(freeparams));

% update R
S.R = updateR(S);

% a posteriori l2-scaling
if l2scaled==1
    S.R = l2scaling(S.R);
elseif l2scaled==2
	S.R = l2scaling(S.R, xstar( S.indices(end):S.Rini.l+S.Rini.n+S.indices(end)-1 ) );
	display( 'l2scaling parameters:');
	xstar( S.indices(end):S.Rini.l+S.Rini.n+S.indices(end)-1 )
elseif l2scaled==3
	S.R = relaxedl2scaling(S.R, Umax, delta);
	display( 'l2scaling parameters:');
	[diag(S.R.Wc)' diag( inv(S.R.J)*(S.R.N*S.R.N' + S.R.M*S.R.Wc*S.R.M')*inv(S.R.J)' )']
end


% save workspace
%assignin( 'caller',inputname(1),S);
if ~isempty(matFileName)
	if isstr(matFileName)
		save (matFileName)
	else
		save (['optim_' func2str(measureFun) '_' funName '_' date ])
	end
end






% find the value corresponding to parameter 'paramName'
% the value must be in the set of 'possibilities'
% 'default' gives the default index
function ind = indexValue( options, paramName, possibilities, default)

try
    [p i] = pnmatch( paramName, options(1:2:length(options)) );
    value = options{i*2};
    try
        [p ind] = pnmatch( value, possibilities);
    catch
        ind = default;
        display( [ 'The value ' value ' of property ' paramName ' is not correct']);
    end
    options(i*2-1)=[];
    options(i*2-1)=[];
    assignin( 'caller', inputname(1), options);
catch
    ind = default;
end



% find the value corresponding to parameter 'paramName'
% return this value OR the defaultValue
% present is true (=1) if the parameter 'paramName' is present in option
function [val present] = optionValue( options, paramName, defaultValue)
try
    [p i] = pnmatch( paramName, options(1:2:length(options)) );
    val = options{i*2};
    options(i*2-1)=[];
    options(i*2-1)=[];
    assignin( 'caller', inputname(1), options);
	present = 1;
catch
    val = defaultValue;
	present = 0;
end


%Description:
% 	This method is the main method of the FWS class. It allows to search over the set of the structured realizations
% 	(defined with the FWS object), by running some optimization algorithms, like \matlab{fminsearch} or \matlab{ASA}.\\
% 	Some options could be passed to this function, in order to parametrize the optimization:
% 	\begin{itemize}
% 		\item the \matlab{method} option can take the following values
% 			\begin{itemize}
% 				\item \matlab{'newton'} (default): to use the Quasi-Newton algorithm (\matlab{fminunc} or \matlab{fmincon} functions)
% 				\item \matlab{'simplex'}: to use the simplex algorithm (\matlab{fminsearch})
% 				\item \matlab{'ASA'}: to use the Annealed Simulated Algorithm\footnote{In that case, \matlab{ASA} and
% 				its Matlab gateway \matlab{asamin} should be correctly
% 				installed, and added in the Matlab's path)}
% 			\end{itemize}
% 		\item the \matlab{l2scaling} option indicates if a $L_2$-scaling should be applied. It can take the following values:
% 			\begin{itemize}
% 				\item \matlab{'no'} (default): no $L_2$-scaling constraints is applied
% 				\item \matlab{'yes'}: the classical $L_2$-scaling constraints are applied (see \funcName[@FWR/l2scaling]{l2scaling})
% 				\item \matlab{'relaxed'}: the relaxed-$L_2$-scaling constraints are applied (see \funcName[@FWR/relaxedl2scaling]{relaxedl2scaling})
% 			\end{itemize}
% 		\item the \matlab{useFWSmeasure} option (\matlab{'yes'} (default) or \matlab{'no'}) forces the use of the $\mt{UYW}$-function
% 		\item the \matlab{fixedParameter} allows to fix some parameters during the optimization. The value associated should be the name of the parameters. Several parameters coudld be fixed.
% 		\item the \matlab{matFileName} sets the filename of the .mat file that is created at the end of the optimization process
% 		to store the final optimized result. By default, this filename is defined by the name of the measure function plus the
% 		name of the structuration (given by the name of the UYWfun or the Rfun) plus the date. If the filename is empty, no
% 		.mat file is storned.\\ In case of ASA method, this name is also used for the log-file created by asamin.
% 		\item the \matlab{MinMax} allows to set the minimum and
% 		maximum values for the parameters. Here only a scalar is required (the maximum value is set to this scalar, the minimum values to the opposite).
%		In order to set individually the min and max values, uses \matlab{Min} and \matlab{Max} options, where you have to pass a vector this the same size as the parameters.
%		\item the extra options are given to the optimization algorihtm (\matlab{fminunc}, \matlab{fmincon}, \matlab{fminsearch},
% 		\matlab{ASA}. See Matlab's\matlab{optimset} or \matlab{asamin} documentation). Classical option (for quasi-Newton and convex
% 		algorithm) is \matlab{\{'Display','Iter'\}}
% 	\end{itemize}
 
%Example:
% 	\begin{verbatim}
% 	>>S = SS2FWS(A,B,C,D);
% 	>>options = {'method','newton','Display','Iter', 'l2scaling','yes');
% 	>>Sopt = optim( S, options, @MsensH_cl, Plant);
% 	\end{verbatim}
% 	The \matlab{Plant} value is given to the function \matlab{MsensH\_cl} as a supplementary parameter. The pair of options
% 	\matlab{'Display','Iter'} is passed to the newton algorithm (\matlab{fminunc} here), so as the iterations are displayed.\\
% 	So, these commands define a state-space structuration, and search for the optimal $L_2$-scaled realization according to the
% 	closed-loop input-output sensitivity (with \matlab{Plant} as a plant to be controlled, see section \ref{sec:closed_loop}).\\
% 	\matlab{Sopt} contains now the structuration \matlab{S} with the optimal realization in \matlab{R} and the optimal parameter
% 	in \matlab{T}.

