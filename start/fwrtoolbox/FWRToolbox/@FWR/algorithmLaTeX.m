%Purpose:
% Return the pseudocode algorithm described in \LaTeX
% (to be used with package {algorithm2e})
%
%Syntax:
% code = algorithmLaTeX( R)
% code = algorithmLaTeX( R, caption)
%
%Parameters:
% R: FWR object
% caption: caption used to describe the algorithm
%		: (default="Pseudocode algorithm ...")
%
% $Id: algorithmLaTeX.m 256 2012-03-12 10:43:20Z hilaire $


function code = algorithm( R, caption)

% args
if nargin<2
    caption='Pseudocode algorithm ...';
end


% parameters
tabu = '	';
endl = 13;
isPnut = any(any( tril(R.P,-1)) ); % is the lower triangular part of R.P non null ???
FP_file = fopen('private/myFilter.tex.template','r');
tmpFile = fopen([ tempdir '/FWRtempfile.tex' ],'w');


%===================================
% input(s)/states/output(s) strings
% output(s)
% generate y (if == 1)
% otherwise generate y(1), y(2), ..., y(p)
if (R.p==1)
    strY = 'y';
else
    strY = [ setstr( ones(R.p,1)*'y' ) setstr( ones(R.p,1)*'(' ) num2str((1:R.p)') setstr( ones(R.p,1)*')' ) ];
end
% states
% generate xn_{1}, ..., xn_{n} with n = number
% idem xnp{n}
strXn = [ setstr( ones(R.n,1)*'xn_{' ) num2str((1:R.n)') setstr( ones(R.n,1)*'}' ) ];
strXnp = [ setstr( ones(R.n,1)*'xnp_{' ) num2str((1:R.n)') setstr( ones(R.n,1)*'}' ) ];
% input(s)
% u (==1) or
% u(1), ..., u(m)
if (R.m==1)
    strU = 'u';
else
    strU = [ setstr( ones(R.m,1)*'u' ) setstr( ones(R.m,1)*'(' ) num2str((1:R.m)') setstr( ones(R.m,1)*')' ) ];
end
% intermediate variables
% T_{1} , ..., T_{L}
    strT = [ setstr( ones(R.l,1)*'T_{' ) num2str((1:R.l)') setstr( ones(R.l,1)*'}' ) ];
%

% Concatenate
strTXU = strvcat( strT, strXn, strU  );
if (isPnut)
    strTXY = strvcat( strT, strXnp, strY  );
else
    strTXY = strvcat( strT, strXn, strY  );
end


%=========
% caption

% Insert caption after first part of template

copyUntilSharps( FP_file, tmpFile); % ##CAPTION##
fwrite( tmpFile, caption);


%======================
% variables declaration

% Augment variables names
% with "declare" routine

copyUntilSharps( FP_file, tmpFile); % ##VARIABLES##
% inputs
declare( tmpFile, 'u', strU, 'KwIn');
% outputs
declare( tmpFile, 'y', strY, 'KwOut');
% states
if (isPnut)
	declare( tmpFile, 'xn, xnp', [ strXn setstr(ones(R.n,1)*', ') strXnp ],  'KwData');
else
	declare( tmpFile, 'xn', strXn,  'KwData');
end
% intermediates variables
declare( tmpFile, 'T', strT,  'KwData');




%=============
% computations
copyUntilSharps( FP_file, tmpFile); % ##COMPUTATIONS##
Zbis = R.Z + [ eye(R.l) zeros(R.l, R.n+R.m); zeros(R.n+R.p,R.l+R.n+R.m) ]; 
for i=1:R.l+R.n+R.p
    if i==1
        fwrite( tmpFile, [ tabu '\tcp{\emph{Intermediate variables}}' endl] );
	elseif i==(R.l+1) & (R.n~=0)
        fwrite( tmpFile, [ tabu '\tcp{\emph{States}}' endl] );
    elseif i==(R.l+R.n+1)
        fwrite( tmpFile, [ tabu '\tcp{\emph{Outputs}}' endl] );
    end        
%    scalprodLaTeX( tmpFile, Zbis(i,:), strTXU, R.FPIS.gammaZ(i,:), R.FPIS.shiftZ(i,:), strAcc(i,:) );
    fwrite( tmpFile, [ tabu '$' strTXY(i,:) ' \leftarrow '  scalprodCdouble(Zbis(i,:), strTXU) '$\;' endl ]);
end

% permutations
if (isPnut)
    fwrite( tmpFile, [ endl tabu '\tcp{\emph{Permutations}}' endl ] );
    fwrite( tmpFile, [ tabu '$xn \leftarrow xnp$\;']);
end


%=======================================
% close files and return tempfile string
copyUntilSharps( FP_file, tmpFile);
fclose(FP_file); fclose(tmpFile);
tmpFile = fopen([ tempdir '/FWRtempfile.tex' ],'r');
code=char(fread(tmpFile))';




%===================
%=== functions ! ===
%===================


function declare( tmpFile, varArray, varNames, KwName)

tabu = '	';
endl=13;
if length(varNames)==1
	fwrite( tmpFile, [ tabu '\' KwName '{$' varArray '$: real}' endl ]);
elseif length(varNames)>1
	fwrite( tmpFile, [ tabu '\' KwName '{$' varArray '$: array [1..'  num2str(length(varNames)) '] of reals}' endl ]);
end


%=================================================
% copy from src to dest until double shaprs appears
function copyUntilSharps( src, dest)

while ~feof(src)
    c=fread(src,1);
    if c=='#'
        c=fread(src,1);
        if c=='#'
            while fread(src,1)~='#'; end;
            fread(src,1);
            break;
        else
            fwrite(dest,c);
        end
    end
    fwrite(dest,c);
end


%Description:
% 	Return a \LaTeX-code that describe the algorithm of the realization:
% 	\begin{align*}
% 		&\text{[i]} & JT(k+1) & \leftarrow MX(k) + NU(k)\\
% 		&\text{[ii]} & X(k+1)  & \leftarrow KT(k+1) + PX(k) + QU(k)\\
% 		&\text{[iii]} & Y(k)    & \leftarrow LT(k+1) + RX(k) + SU(k)
% 	\end{align*} 
% 	All the operations with matrices are expanded, and null multiplications are removed, identity multiplications are simplified, etc.\\
%	The package \textit{algorithm2e} is used.\\
%	The file \matlab{@FWR/private/myFilter.tex.template} is used as a
%	template.
%Example:
% 	The following \LaTeX-code is produced by this function:
%	\begin{lstlisting}[language={[LaTeX]tex}]
% 	\begin{algorithm}[h]
% 		\caption{Pseudocode algorithm ...}
% 		\KwIn{$u$: real}
% 		\KwOut{$y$: real}
% 		\KwData{$xn, xnp$: array [1..13] of reals}
% 
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$xnp(1) \leftarrow 0.5529838718*xn(1) + -0.5379265439*xn(2) + 0.0291718129*xn(3) + 0.6715678041*u    $\;
% 		$xnp(2) \leftarrow 0.5379265439*xn(1) + 0.0971133953*xn(2) + -0.3562792507*xn(3) + -0.3237597311*u    $\;
% 		$xnp(3) \leftarrow 0.0291718129*xn(1) + 0.3562792507*xn(2) + -0.0728567423*xn(3) + 0.0792887747*u    $\;
% 		\tcp{\emph{Outputs}}
% 		$y      \leftarrow 0.6715678041*xn(1) + 0.3237597311*xn(2) + 0.0792887747*xn(3) + 0.0985311609*u    $\;
% 
% 		\tcp{\emph{Permutations}}
% 		$xn \leftarrow xnp$\;	
% 	}
% 	\end{algorithm}
% 	\end{lstlisting}
% 	And it corresponds to the algorithm \ref{algo:algorithmLaTeX:algo}: 
% 	\begin{algorithm}[h!]
% 		\caption{Pseudocode algorithm ...\label{algo:algorithmLaTeX:algo}}
% 		\KwIn{$u$: real}
% 		\KwOut{$y$: real}
% 		\KwData{$xn, xnp$: array [1..13] of reals}
% 
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$xnp(1) \leftarrow 0.5529838718*xn(1) + -0.5379265439*xn(2) + 0.0291718129*xn(3) + 0.6715678041*u    $\;
% 		$xnp(2) \leftarrow 0.5379265439*xn(1) + 0.0971133953*xn(2) + -0.3562792507*xn(3) + -0.3237597311*u    $\;
% 		$xnp(3) \leftarrow 0.0291718129*xn(1) + 0.3562792507*xn(2) + -0.0728567423*xn(3) + 0.0792887747*u    $\;
% 		\tcp{\emph{Outputs}}
% 		$y      \leftarrow 0.6715678041*xn(1) + 0.3237597311*xn(2) + 0.0792887747*xn(3) + 0.0985311609*u    $\;
% 
% 		\tcp{\emph{Permutations}}
% 		$xn \leftarrow xnp$\;	
% 	}
% 	\end{algorithm}

%See also: <@FWR/algorithmCfloat>, <@FWR/implementLaTeX>
