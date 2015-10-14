%Purpose:
% Return the implementation associated to this realization.
% The algorithm is written in C-code with double 
%
%Syntax:
% code = implementCdouble( R, funcName)
%
%Parameters:
% code: resulting C-code (with double)
% R: FWR object
% funcName: name of the C-function (default='myFilter')
%
% $Id$


function code = implementCdouble(R, funcName)

if nargin==1
    funcName='myFilter';
end

if (R.p~=1)
	error ('R.p should be equal to 1')
end

% parameters
tabu = '    ';	% tabulation
endl = 13;	% end of the line
isPnut = any(any( tril(R.P,-1)) ); % is the lower triangular part of R.P non null ???

%===================================
% input(s)/states/output(s) strings
% output(s)
if (R.p==1)
    strY = 'y';
else
    strY = [ setstr( ones(R.p,1)*'y' ) setstr( ones(R.p,1)*'[' ) num2str((0:R.p-1)') setstr( ones(R.p,1)*']' ) ];
end
% states
if (isPnut)
    strXn = [ setstr( ones(R.n,1)*'(*xn)' ) setstr( ones(R.n,1)*'[' ) num2str((0:R.n-1)') setstr( ones(R.n,1)*']' ) ];
    strXnp = [ setstr( ones(R.n,1)*'(*xnp)' ) setstr( ones(R.n,1)*'[' ) num2str((0:R.n-1)') setstr( ones(R.n,1)*']' ) ];
else
    strXn = [ setstr( ones(R.n,1)*'xn' ) setstr( ones(R.n,1)*'[' ) num2str((0:R.n-1)') setstr( ones(R.n,1)*']' ) ];
end

% input(s)
if (R.m==1)
    strU = 'u';
else
    strU = [ setstr( ones(R.m,1)*'u' ) setstr( ones(R.m,1)*'[' ) num2str((0:R.m-1)') setstr( ones(R.m,1)*']' ) ];
end
    % intermediate variables
if (R.l==1)
    strT = 'T';
else
    strT = [ setstr( ones(R.l,1)*'T' ) num2str((0:R.l-1)','%-d') ];
end


%==========
% prototype

Cfile = fopen([ funcName '.c'],'w');


% output
fwrite( Cfile, [ endl 'double' ]);
fwrite( Cfile, [' ' funcName '( ' ]);


% input(s)
if (R.m==1)
    fwrite( Cfile, 'double u' );
else
    fwrite( Cfile, 'double* u' );
end
if (isPnut)
    fwrite( Cfile, ', double** xn');
	fwrite( Cfile, ', double** xnp');
else
    fwrite( Cfile, ', double* xn');
end
fwrite( Cfile, ')');


%=============
% computations

% beginning
fwrite( Cfile, [endl '{' endl]);
fwrite( Cfile, [ tabu 'double y;' tabu tabu '// output' endl]);


% intermediate variables J.T = M.X(k) + N.U(k)
if (R.l>0)
    fwrite( Cfile, [ endl tabu '// intermediate variables' endl] );
end
for i=1:R.l
    fwrite( Cfile, [ tabu 'double ' strT(i,:) ' = ' scalprodCdouble( [R.M(i,:) R.N(i,:) -R.J(i,1:i-1) ], strvcat( strXn, strU, strT(1:i-1,:) )) ';' endl] );
end

% output Y(k) = R.X(k) + code.U(k) + L.T
fwrite( Cfile, [ endl tabu '// output(s)' endl] );
for i=1:R.p
    fwrite( Cfile, [ tabu strY(i,:) ' = ' scalprodCdouble( [ R.R(i,:) R.S(i,:) R.L(i,:) ], strvcat( strXn, strU, strT) ) ';' endl] );
end

% states X(k) = P.X(k) + Q.U(k) + K.T
fwrite( Cfile, [ endl tabu '// states' endl] ); 
for i=1:R.n
    if (isPnut)
        fwrite( Cfile, [ tabu strXnp(i,:) ' = ' scalprodCdouble( [ R.P(i,:) R.Q(i,:) R.K(i,:) ], strvcat( strXn, strU, strT ) ) ';' endl ] );
    else
        fwrite( Cfile, [ tabu strXn(i,:) ' = ' scalprodCdouble( [ R.P(i,:) R.Q(i,:) R.K(i,:) ], strvcat( strXn, strU, strT ) ) ';' endl ] );
    end
end

% permutation
if (isPnut)
    fwrite( Cfile, [ endl tabu '//permutations' endl ] );
    fwrite( Cfile, [ tabu 'double* temp = (*xn);' endl ]);
    fwrite( Cfile, [ tabu '(*xn) = (*xnp);' endl ]);
    fwrite( Cfile, [ tabu '(*xnp) = temp;' endl]);
end


% end
fwrite( Cfile, [ endl tabu '// output' endl ] );
fwrite( Cfile, [ tabu 'return y;' endl endl '}' endl] );

fclose( Cfile);
        

%Description:
% 	Transform in \texttt{C}-code with \texttt{double} the algorithm of the realization:
% 	\begin{align*}
% 		&\text{[i]} & JT(k+1) & \leftarrow MX(k) + NU(k)\\
% 		&\text{[ii]} & X(k+1)  & \leftarrow KT(k+1) + PX(k) + QU(k)\\
% 		&\text{[iii]} & Y(k)    & \leftarrow LT(k+1) + RX(k) + SU(k)
% 	\end{align*} 
% 	All the operations with matrices are expanded, and null multiplications are removed, identity multiplications are simplified, etc.\\
% 	The input or a pointer to the vector of inputs is given to the function. The function returns the output or a pointer to a vector of putputs.\\
% 	The intermediate variables are stored in a variable \matlab{T}. The states are stored in \matlab{static} variables \matlab{xn} and \matlab{xnp} (\matlab{xnp} is not necessary if $P$ is upper triangular), and a permutation of the vector (a permutation of the pointer to the vector) is performed for the next call. 
%Example:
% 	\begin{lstlisting}[language=C]
% 	>> algorithmCdouble(R)
% 	ans =
% 	double myFilter( double u, double* xn)                                                                                                                                                                                   
% 	{                                                                                                                                                                                                          
% 
% 		// intermediate variables                                                                                                                                                                              
% 		double T = -0.6630104844*xn[0] + 2.9240526562*xn[1] + -4.8512758825*xn[2] 
% 			+ 3.5897338871*xn[3] + 0.0000312390*xn[4] + 0.0001249559*xn[5] 
% 			+ 0.0001874339*xn[6] + 0.0001249559*xn[7] + 0.0000312390*u    ;
% 
% 		// output(s)                                                                                                                                                                                           
% 		y = T    ;                                                                                                                                                                                             
% 
% 		// states                                                                                                                                                                                              
% 		xn[0] = xn[1];                                                                                                                                                                                         
% 		xn[1] = xn[2];                                                                                                                                                                                         
% 		xn[2] = xn[3];                                                                                                                                                                                         
% 		xn[3] = T    ;                                                                                                                                                                                         
% 		xn[4] = xn[5];                                                                                                                                                                                         
% 		xn[5] = xn[6];                                                                                                                                                                                         
% 		xn[6] = xn[7];                                                                                                                                                                                         
% 		xn[7] = u    ;                                                                                                                                                                                         
% 	}
% 	\end{lstlisting}

%See also: <@FWR/algorithmLaTeX>


        
        
