%Purpose:
% Display a matrix ($Z$ or a sensitivity matrix) in \LaTeX (with 'pmat'
% package). The non trivial parameters (according to $W_Z$) are in bold.
%
%Syntax:
% S = FWRmat2LaTeX( R)
% S = FWRmat2LaTeX( R, M, format,tol)
%
%Parameters:
% S: string result (to be pasted in \LaTeX source)
% R: FWR object
% M: matrix to print in \LaTeX format
%	: if $M$ is omitted (or empty), $Z$ is printed
%	: $M$ must have the same size as $Z$
% format: print format
%		: default value : "%0.5g"
%		: "%.3e" for short e format, etc...
% tol: tolerance to find trivial parameter (1,-1,0)
%		:default value: 1e-10
%
% $Id: FWRmat2latex.m 180 2008-12-12 19:13:32Z hilaire $


function S = FWRmat2LaTeX( R, M, format,tol)

%args
if (nargin<2) | isempty(M)
    M=R.Z;
else
    if size(M)~=size(R.Z)
        error('M must have the same size as Z');
    end
end
if (nargin<3)
    format = '%0.5g';
end
if nargin<4
    tol=1e-10;
end


%begin
S = [ '\begin{pmat}({' put('.',R.l-1) '|' put('.',R.n-1) '|' put('.',R.m-1) '})'];

if (R.l==0)
    S = strvcat(S, '	\cr\-');
end

%each row
for i=1:(R.l+R.n+R.p)

    row='';
    if (R.l==0)
        row='&';
    end
    
    % each column
    for j=1:(R.l+R.n+R.m)
        
        % check trivial parameter
        if abs(M(i,j))<tol | abs(M(i,j)-1)<tol | abs(M(i,j)+1)<tol
            val = sprintf( '%d', round(M(i,j)/tol)*tol);
        else
            val = sprintf( format, M(i,j));
        end
        % replace 'e+' and 'e-' by '\expp' and '\expm'
        val = strrep( val,'e+0','\expp');
        val = strrep( val,'e-0','\expm');
        val = strrep( val,'e+','\expp');
        val = strrep( val,'e-','\expm'); 
        % bold font ?
        if (R.WZ(i,j)~=0)
            val = [ '\mathbf{' val '}' ];
        end
        row = [ row val];
        if (j~=(R.l+R.n+R.m))
            row = [ row ' & '];
        end
        
    end
    
    % vertical ligne
    row = [ row ' \cr' ];
    if ( (i==R.l) | (i==(R.l+R.n)) )
        row = [ row, '\-' ];
    end
    
    S = strvcat(S, [ '	' row] );
end

%end
S = strvcat(S, '\end{pmat}');


% concat a char n times
function Str=put(char,n)
    
    Str='';
    for i=1:n
        Str=[ Str char ];
	end
	
	
%Description:
% 	Display a matrix ($Z$ or a given matrix \matlab{M}, for example a sensitivity matrix) of a FWR object in a special \LaTeX format
% 	(with \texttt{pmat} package): the coefficients with $W_{Z(i,j)}$ non null are in bold.
% 
%Example:
% 	The command \matlab{FWRmat2latex(R)}, where $R$ is a FWR object,
% 	returns:
% 	\begin{lstlisting}
% 	\begin{pmat}({|...|})                                                                               
% 		\cr\-                                                                                              
% 		&\mathbf{3.7673} & \mathbf{-1.8552} & \mathbf{1.0013} & \mathbf{-0.91839} & \mathbf{2} \cr         
% 		&\mathbf{4} & 0 & 0 & 0 & 0 \cr                                                                    
% 		&0 & \mathbf{2} & 0 & 0 & 0 \cr                                                                    
% 		&0 & 0 & \mathbf{0.5} & 0 & 0 \cr\-                                                                
% 		&\mathbf{0.90722} & \mathbf{-0.56715} & \mathbf{0.24114} & \mathbf{-0.16096} & \mathbf{0.48163} \cr
% 	\end{pmat}
% 	\end{lstlisting}
% 	When compiled, this \LaTeX code produces
% 	$$\begin{pmat}({|...|})                                                                               
% 		\cr\-                                                                                              
% 		&\mathbf{3.7673} & \mathbf{-1.8552} & \mathbf{1.0013} & \mathbf{-0.91839} & \mathbf{2} \cr         
% 		&\mathbf{4} & 0 & 0 & 0 & 0 \cr                                                                    
% 		&0 & \mathbf{2} & 0 & 0 & 0 \cr                                                                    
% 		&0 & 0 & \mathbf{0.5} & 0 & 0 \cr\-                                                                
% 		&\mathbf{0.90722} & \mathbf{-0.56715} & \mathbf{0.24114} & \mathbf{-0.16096} & \mathbf{0.48163} \cr
% 	\end{pmat}$$
% 
% If a scientif format is used, the following \LaTeX macros are used (just to save some spaces)
% \begin{verbatim}
% \newcommand{\expm}[0]{e\hspace{-0.75mm}-\hspace{-0.75mm}}
% \newcommand{\expp}[0]{e\hspace{-0.75mm}+\hspace{-0.75mm}
% \end{verbatim}
   
