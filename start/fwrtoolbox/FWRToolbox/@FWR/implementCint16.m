%Purpose:
% Return the implementation associated to this realization.
% The algorithm is written in C-code with int16 and int32
%
% WARNING: this function is only to use with int16 and int32
% (other formats will be used later, when I will have more time)
%
%Syntax:
% code = implementCint16( R, funcName)
%
%Parameters:
% code: resulting C-code (with int16)
% R: FWR object
% funcName: name of the C-function (default='myFilter')
%
% $Id$


function code = implementCint16(R, funcName)

if nargin==1
    funcName='myFilter';
end

% FPIS?
if isempty(R.FPIS)
    error( 'The realization must have a valid FPIS');
end
if R.FPIS.betaZ~=16
    error( 'beta should be equal to 16');
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
% accumulator
strAcc = setstr( ones(R.l+R.n+R.p,1)*'Acc'); %strAcc = [ setstr( ones(R.l+R.n+R.p,1)*'Acc') num2str((0:R.l+R.n+R.p-1)','%-d') ];
strTXU = strvcat( strT, strXn, strU  );
if (isPnut)
    strTXY = strvcat( strT, strXnp, strY  );
else
    strTXY = strvcat( strT, strXn, strY  );
end

%==========
% prototype

Cfile = fopen([ funcName '.c'],'w');

fwrite( Cfile, [ endl '#define int16 signed short' endl '#define int32 signed int' endl ]);

% output
fwrite( Cfile, [ endl 'int16']);
fwrite( Cfile, [' ' funcName '( ' ]);


% input(s)
if (R.m==1)
    fwrite( Cfile, 'int16 u' );
else
    fwrite( Cfile, 'int16* u' );
end
if (isPnut)
    fwrite( Cfile, ', int16** xn');
	fwrite( Cfile, ', int16** xnp');
else
    fwrite( Cfile, ', int16* xn');
end
fwrite( Cfile, ')');


%=============
% computations

% beginning
fwrite( Cfile, [endl '{' endl]);
fwrite( Cfile, [ tabu 'int16 y;' tabu tabu '// output' endl]);
fwrite( Cfile, [ tabu 'int32 Acc;' tabu tabu '// accumulator' endl]);
Zbis = R.Z + [ eye(R.l) zeros(R.l, R.n+R.m); zeros(R.n+R.p,R.l+R.n+R.m) ]; 
for i=1:R.l+R.n+R.p
    if i==1
        fwrite( Cfile, [ endl tabu '// intermediate variables' endl] );
    elseif i==(R.l+1)
        fwrite( Cfile, [ endl tabu '// states' endl] );
    elseif i==(R.l+R.n+1)
        fwrite( Cfile, [ endl tabu '// output(s)' endl] );
    end
    scalprodCint( Cfile, Zbis(i,:), strTXU, R.FPIS.gammaZ(i,:), R.FPIS.shiftZ(i,:), strAcc(i,:) );
    fwrite( Cfile, tabu);
    if i<=R.l
        fwrite( Cfile, 'int16 ');
    end
    fwrite( Cfile, [ strTXY(i,:) ' = ' shiftcode( strAcc(i,:), R.FPIS.shiftADD(i) ) ';' endl ]);
end

% permutation
if (isPnut)
    fwrite( Cfile, [ endl tabu '//permutations' endl ] );
    fwrite( Cfile, [ tabu 'int16* temp = (*xn);' endl ]);
    fwrite( Cfile, [ tabu '(*xn) = (*xnp);' endl ]);
    fwrite( Cfile, [ tabu '(*xnp) = temp;' endl]);
end


% end
fwrite( Cfile, [ endl tabu '// output' endl ] );
fwrite( Cfile, [ tabu 'return y;' endl endl '}' endl] );

fclose( Cfile);
        



%===================
% code for the shift
function S = shiftcode( str, shift)

if shift<0
    S = ['(' str ' << ' num2str(-shift) ')' ];
elseif shift==0
    S = str;
else
    S = [ str ' >> ' num2str(shift) ];
end

        
        
