%Purpose:
% Return the associated fixed-point algorithm described in \LaTeX
% (to be used with package 'algorithm2e')
%
%Syntax:
% code = implementLaTeX( R)
% code = implementLaTeX( R, caption)
%
%Parameters:
% R: FWR object
% caption: caption used to describe the algorithm
%		: (default = "Numerical fixed-point algorithm ...")
%
% $Id: implementLaTeX.m 256 2012-03-12 10:43:20Z hilaire $


function code = implementLaTeX( R, caption)

% args
if nargin<2
    caption='Numerical fixed-point algorithm ...';
end

% FPIS?
if isempty(R.FPIS)
    error( 'The realization must have a valid FPIS');
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
if (R.p==1)
    strY = 'y';
else
    strY = [ setstr( ones(R.p,1)*'y' ) setstr( ones(R.p,1)*'(' ) num2str((1:R.p)') setstr( ones(R.p,1)*')' ) ];
end
% states
strXn = [ setstr( ones(R.n,1)*'xn' ) setstr( ones(R.n,1)*'(' ) num2str((1:R.n)') setstr( ones(R.n,1)*')' ) ];
strXnp = [ setstr( ones(R.n,1)*'xnp' ) setstr( ones(R.n,1)*'(' ) num2str((1:R.n)') setstr( ones(R.n,1)*')' ) ];
% input(s)
if (R.m==1)
    strU = 'u';
else
    strU = [ setstr( ones(R.m,1)*'u' ) setstr( ones(R.m,1)*'(' ) num2str((1:R.m)') setstr( ones(R.m,1)*')' ) ];
end
% intermediate variables
    strT = [ setstr( ones(R.l,1)*'T_{' ) num2str((1:R.l)') setstr( ones(R.l,1)*'}' ) ];
% accumulator
isOneAcc = all( (R.FPIS.betaADD+R.FPIS.betaG)==(R.FPIS.betaADD(1)+R.FPIS.betaG(1)));
if isOneAcc
    strAcc = setstr( ones(R.l+R.n+R.p,1)*'Acc');
else
    strAcc = [ setstr( ones(R.l+R.n+R.p,1)*'Acc_{') num2str((1:R.l+R.n+R.p)') setstr( ones(R.l+R.n+R.p,1)*'}' ) ];
end
%
strTXU = strvcat( strT, strXn, strU  );
if (isPnut)
    strTXY = strvcat( strT, strXnp, strY  );
else
    strTXY = strvcat( strT, strXn, strY  );
end


%=========
% caption
copyUntilSharps( FP_file, tmpFile); % ##CAPTION##
fwrite( tmpFile, caption);

%======================
% variables declaration
copyUntilSharps( FP_file, tmpFile); % ##VARIABLES##
% inputs
declare( tmpFile, 'u', strU, R.FPIS.betaU, 'KwIn');
% outputs
declare( tmpFile, 'y', strY, R.FPIS.betaY, 'KwOut');
% states
if (isPnut)
	declare( tmpFile, 'xn, xnp', [ strXn setstr(ones(R.n,1)*', ') strXnp ], R.FPIS.betaX, 'KwData');
else
	declare( tmpFile, 'xn', strXn, R.FPIS.betaX, 'KwData');
end
% intermediates variables
declare( tmpFile, 'T', strT, R.FPIS.betaT, 'KwData');
% accumulator
if isOneAcc
	declare( tmpFile, 'Acc', strAcc(1), R.FPIS.betaADD(1)+R.FPIS.betaG(1), 'KwData');
else
	declare( tmpFile, 'Acc', strAcc, R.FPIS.betaADD+R.FPIS.betaG, 'KwData');
end



%=============
% computations
copyUntilSharps( FP_file, tmpFile); % ##COMPUTATIONS##
Zbis = R.Z + [ eye(R.l) zeros(R.l, R.n+R.m); zeros(R.n+R.p,R.l+R.n+R.m) ]; 
for i=1:R.l+R.n+R.p
    if i==1
        fwrite( tmpFile, [ tabu '\tcp{\emph{Intermediate variables}}' endl] );
    elseif i==(R.l+1)
        fwrite( tmpFile, [ tabu '\tcp{\emph{States}}' endl] );
    elseif i==(R.l+R.n+1)
        fwrite( tmpFile, [ tabu '\tcp{\emph{Outputs}}' endl] );
    end        
    if scalprodLaTeX( tmpFile, Zbis(i,:), strTXU, R.FPIS.gammaZ(i,:), R.FPIS.shiftZ(i,:), strAcc(i,:) )
		fwrite( tmpFile, [ tabu '$' strTXY(i,:) ' \leftarrow 0$\;' endl ]);
	else 
		fwrite( tmpFile, [ tabu '$' strTXY(i,:) ' \leftarrow ' shiftcode( strAcc(i,:), R.FPIS.shiftADD(i) ) '$\;' endl ]);
	end
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


function declare( tmpFile, varArray, varNames, Wordlength, KwName)

tabu = '	';
endl=13;
if length(varNames)==1
	fwrite( tmpFile, [ tabu '\' KwName '{$' varArray '$: ' num2str(Wordlength(1)) ' bits integer}' endl ]);
elseif length(varNames)>1
	if all(Wordlength==Wordlength(1))
		fwrite( tmpFile, [ tabu '\' KwName '{$' varArray '$: array [1..'  num2str(length(varNames)) '] of ' num2str(Wordlength(1)) ' bits integers}' endl ]);
	else
		for i=1:length(varNames)
			fwrite( tmpFile, [ tabu '\' KwName '{$' varNames(i) '$: ' num2str(Wordlength(i)) ' bits integer}' endl ]);
		end
	end
end



function isZero=scalprodLaTeX( file, P, name, gamma, shift, strAcc)

tol=1e-10;
tabu = '	';
nzP = find( abs(P)>tol );
endl=13;


for i=nzP
    if i==nzP(1)
        strAccPlus = '';
    else
        strAccPlus = [ strAcc ' + ' ];
    end
    
    coef = round(P(i)*2^gamma(i));
    if ( coef<=0 | abs(rem(log2(abs(coef)),1))>tol )
        fwrite( file, [ tabu '$' strAcc ' \leftarrow ' strAccPlus shiftcode( [ '(' name(i,:) ' * ' num2str( coef ) ')' ], shift(i)) '$\;' endl ]) ;
    else
        fwrite( file, [ tabu '$' strAcc ' \leftarrow ' strAccPlus shiftcode( name(i,:), shift(i)-log2(coef) ) '$\;' endl ]) ;
	end
end

isZero = isempty(nzP);



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



%===================
% code for the shift
function S = shiftcode( str, shift)

str=deblank(str);
if shift<0
    S = [ '(' str ' << ' num2str(-shift) ')'];
elseif shift==0
    S = str;
else
    S = [ '(' str ' >> ' num2str(shift) ')'];
end

%Description:
% 	Return the associated fixed-point algorithm in \LaTeX. It uses the package
% 	\textit{algorithm2e}. All the wordlengths and the fixed-point positions should be
% 	first computed by adjusting the FPIS with
% 	\funcName{@FWR/setFPIS}.\\
%	The file \matlab{@FWR/private/myFilter.tex.template} is used as a
%	template.
%Example:
% 	It returns \LaTeX-code like this
% 	\begin{lstlisting}[language={[LaTeX]tex}]
% 	\begin{algorithm}[h]
% 		\caption{Numerical fixed-point algorithm ...}
% 		\KwIn{$u$: 16 bits integer}
% 		\KwOut{$y$: 16 bits integer}
% 		\KwData{$xn, xnp$: array [1..13] of 16 bits integers}
% 		\KwData{$Acc$: 32 bits integer}
% 
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$Acc \leftarrow (xn(1) * 18120)$\;
% 		$Acc \leftarrow Acc + (xn(2) * -8813)$\;
% 		$Acc \leftarrow Acc + (xn(3) * 239)$\;
% 		$Acc \leftarrow Acc + (u     * 11003)$\;
% 		$xnp(1) \leftarrow Acc >> 15$\;
% 		$Acc \leftarrow (xn(1) * 17627)$\;
% 		$Acc \leftarrow Acc + (xn(2) * 1591)$\;
% 		$Acc \leftarrow Acc + (xn(3) * -2919)$\;
% 		$Acc \leftarrow Acc + (u     * -5304)$\;
% 		$xnp(2) \leftarrow Acc >> 14$\;
% 		$Acc \leftarrow (xn(1) * 3824)$\;
% 		$Acc \leftarrow Acc + (xn(2) * 23349)$\;
% 		$Acc \leftarrow Acc + (xn(3) * -2387)$\;
% 		$Acc \leftarrow Acc + (u     * 5196)$\;
% 		$xnp(3) \leftarrow Acc >> 15$\;
% 		\tcp{\emph{Outputs}}
% 		$Acc \leftarrow (xn(1) * 22006)$\;
% 		$Acc \leftarrow Acc + (xn(2) * 5304)$\;
% 		$Acc \leftarrow Acc + (xn(3) * 650)$\;
% 		$Acc \leftarrow Acc + (u     * 1614)$\;
% 		$y      \leftarrow Acc >> 14$\;
% 
% 		\tcp{\emph{Permutations}}
% 		$xn \leftarrow xnp$\;	
% 	}
% 	\end{algorithm}
% 	\end{lstlisting}
% 	That corresponds to the algorithm \ref{algo:implementLaTeX:algo}.
% 	\begin{algorithm}[h]
% 		\caption{Numerical fixed-point algorithm ...\label{algo:implementLaTeX:algo}}
% 		\KwIn{$u$: 16 bits integer}
% 		\KwOut{$y$: 16 bits integer}
% 		\KwData{$xn, xnp$: array [1..13] of 16 bits integers}
% 		\KwData{$Acc$: 32 bits integer}
% 
% 		\SetLine
% 		\Begin{
% 		\tcp{\emph{Intermediate variables}}
% 		$Acc \leftarrow (xn(1) * 18120)$\;
% 		$Acc \leftarrow Acc + (xn(2) * -8813)$\;
% 		$Acc \leftarrow Acc + (xn(3) * 239)$\;
% 		$Acc \leftarrow Acc + (u     * 11003)$\;
% 		$xnp(1) \leftarrow Acc >> 15$\;
% 		$Acc \leftarrow (xn(1) * 17627)$\;
% 		$Acc \leftarrow Acc + (xn(2) * 1591)$\;
% 		$Acc \leftarrow Acc + (xn(3) * -2919)$\;
% 		$Acc \leftarrow Acc + (u     * -5304)$\;
% 		$xnp(2) \leftarrow Acc >> 14$\;
% 		$Acc \leftarrow (xn(1) * 3824)$\;
% 		$Acc \leftarrow Acc + (xn(2) * 23349)$\;
% 		$Acc \leftarrow Acc + (xn(3) * -2387)$\;
% 		$Acc \leftarrow Acc + (u     * 5196)$\;
% 		$xnp(3) \leftarrow Acc >> 15$\;
% 		\tcp{\emph{Outputs}}
% 		$Acc \leftarrow (xn(1) * 22006)$\;
% 		$Acc \leftarrow Acc + (xn(2) * 5304)$\;
% 		$Acc \leftarrow Acc + (xn(3) * 650)$\;
% 		$Acc \leftarrow Acc + (u     * 1614)$\;
% 		$y      \leftarrow Acc >> 14$\;
% 
% 		\tcp{\emph{Permutations}}
% 		$xn \leftarrow xnp$\;	
% 	}
% 	\end{algorithm}

%See also: <@FWR/algorithmLaTeX>, <@FWR/implementMATLAB>, <@FWR/implementVHDL>
