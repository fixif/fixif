% give the associated algorithm (in C-code with cFp)
%
% [code, Rqt] = fpC( R, betaZ, betaU, gammaU, betaT, betaX, betaY, betaADD, betaG, method, funcName)
%
% code: resulting C-code
% Rqt: quantized realization (FWR object)
% R: FWR object
% betaZ: Z's wordlength 
% betaU, gammaU: input format
% betaT, betaX, betaY: T, X, Y 's wordlength
% betaADD, betaG: additionneur wordlentgh and gard bits
% method: 'RBM' (default) Roundoff Before Multiplication
%         or 'RAM' Roundoff After Multiplication
% funcName: name of the function (default='myFilter')
%
% $Id$

function [code, Rqt] = fpC(R, betaZ, betaU, gammaU, betaT, betaX, betaY, betaADD, betaG, method, funcName)

% args
if nargin<10
    method=1;
elseif method=='RAM'
    method=2;
else
    method=1;
end
if nargin<11
    funcName='myFilter';
end

% change args if they are scalar
if prod( size(betaZ) )==1
    betaZ = betaZ * ones(size(R.Z));
end
if prod( size(betaU) )==1
    betaU = betaU * ones(R.m,1);
end
if prod( size(gammaU) )==1
    gammaU = gammaU * ones(R.m,1);
end
if prod( size(betaY) )==1
    betaY = betaY * ones(R.p,1);
end
if prod( size(betaX) )==1
    betaX = betaX * ones(R.n,1);
end
if prod( size(betaT) )==1
    betaT = betaT * ones(R.l,1);
end
if prod( size(betaADD) )==1
    betaADD = betaADD * ones( size(R.Z,1), 1);
end
if prod( size(betaG) )==1
    betaG = betaG * ones( size(R.Z,1), 1);
end

% gammas / betas
H6 = ss(R.AZ,R.BZ, [ inv(R.J)*R.M ; eye(R.n); R.CZ ], [inv(R.J)*R.N; zeros(R.n,R.m); R.DZ],1);
[Yimp Timp] = impulse(H6);
L1 = sum(abs(Yimp))';
betaTXY = [ betaT; betaX; betaY ];
betaTXU = [ betaT; betaX; betaU ];
gammaTXY = betaTXY - ones(size(R.Z,1),1) - ceil( log2( L1*(2*ones(R.m,1)).^(betaU-gammaU-1) ) );
gammaTXU = [ gammaTXY(1:(R.l+R.n)); gammaU ];
gammaT = gammaTXY(1:R.l); gammaX = gammaTXY((R.l+1):(R.l+R.n)); gammaY = gammaTXY((R.l+R.n+1):end);
gammaZ = betaZ - ones(size(R.Z)) - ceil( log2(abs(R.Z)) );

% 1 and 0's
eps=1e-12;
i1 = find( abs(R.Z-1)<eps);
gammaZ(i1) = 0;
betaZ(i1) = 0;

% gammaADD
alpha = max( betaZ - gammaZ + ones(size(R.Z,1),1)*((betaTXU-gammaTXU)'),[],2 );
gammaADD = betaADD - max( betaTXY-betaG-gammaTXY, alpha);

% shift on multiplications
shiftZ = ones(size(R.Z,1),1)*gammaTXU' + gammaZ - gammaADD*ones(1,size(R.Z,1));
shiftTXY = gammaADD - gammaTXY;

% quantized realization
Rqt=R;
gammaZbis=gammaZ;
gammaZbis( find(isinf(gammaZ)) ) = 0;
Rqt.Z = round( R.Z .* (2.^gammaZbis) ) .* (2.^-gammaZbis);




% parameters
tabu = '    ';
isPnut = any(any( tril(R.P,-1)) ); % is the lower triangular part of R.P non null ???

%===================================
% input(s)/states/output(s) strings
% output(s)
if (R.p==1)
    strY = 'y';
else
    %strY = [ setstr( ones(R.p,1)*'y' ) setstr( ones(R.p,1)*'[' ) num2str((0:R.p-1)') setstr( ones(R.p,1)*']' ) ];
    strY = [ setstr( ones(R.p,1)*'y' ) num2str((0:R.p-1)') ];
end
% states
strXn = [ setstr( ones(R.n,1)*'xn' ) setstr( ones(R.n,1)*'[' ) num2str((0:R.n-1)') setstr( ones(R.n,1)*']' ) ];
strXnp = [ setstr( ones(R.n,1)*'xnp' ) setstr( ones(R.n,1)*'[' ) num2str((0:R.n-1)') setstr( ones(R.n,1)*']' ) ];
%strXn = [ setstr( ones(R.n,1)*'xn' ) num2str((0:R.n-1)')  ];
%strXnp = [ setstr( ones(R.n,1)*'xnp' ) num2str((0:R.n-1)') ];

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
    strT = [ setstr( ones(R.l,1)*'T' ) num2str((0:R.l-1)') ];
end
% accumulator
strAcc = [ setstr( ones(R.l+R.n+R.p,1)*'Acc') num2str((0:R.l+R.n+R.p-1)') ];

%==========
% prototype

% output(s)
code= 'cFp';
if (R.p>1) code = [code '*']; end
code = [ code ' ' funcName '( ' ];

% input(s)
if (R.m==1)
    code = [ code 'cFp u)' ];
else
    code = [ code 'cFp* u)' ];
end


%=============
% computations

% beginning
code = strvcat( code, '{');

% declarations states
code = strvcat( code, [ tabu '// states' ]);
codeX=[];
for i=1:R.n
    codeX = strcat( codeX, ['cFp(0,' num2str(betaX(i)) ',' num2str(gammaX(i)) ')' ] );
    if i<R.n
        codeX = strcat( codeX, ',');
    end
end
code = strvcat( code, [ tabu 'static cFp xn[' num2str(R.n) '] = { ' codeX ' };' ]);
code = strvcat( code, [ tabu 'static cFp xnp[' num2str(R.n) '] = { ' codeX ' };' ]);

% declaration outputs
code = strvcat( code, [ tabu '// outputs']);
code = strvcat( code, [ tabu 'cFp ' strY(1,:) '(0,' num2str(betaY), ',' num2str(gammaY) ');' ]);


% intermediate variables J.T = M.X(k) + N.U(k)
if (R.l>0)
    code = strvcat( code, ' ', [ tabu '// intermediate variables' ] );
end
for i=1:R.l
    code = strvcat( code, [ tabu 'cAcc ' strAcc(i,:) '(' num2str(betaADD(i)) ',' num2str(betaG(i)) ',' num2str(gammaADD(i)) ');' ]);
    code = strvcat( code, [ tabu 'cFp ' strT(i,:) '(0, ' num2str(betaT(i)) ',' num2str(gammaT(i)) ');' ]);
    code = strvcat( code, fpscalprod(   [ -R.J(i,1:i-1) R.M(i,:) R.N(i,:) ],...
                                        strvcat( strT(1:i-1,:), strXn, strU  ),...
                                        betaZ(i,[1:i-1 R.l+1:end]),...
                                        gammaZ(i,[1:i-1 R.l+1:end]),...
                                        shiftZ(i,[1:i-1 R.l+1:end]),...
                                        strAcc(i,:) ) );
    if shiftTXY(i)
        code = strvcat( code, [ tabu strT(i,:) '= ' strAcc(i,:) ' >> ' num2str(shiftTXY(i)) ';' ],' ');
    else
        code = strvcat( code, [ tabu strT(i,:) '= ' strAcc(i,:) ';' ],' ');
    end
end

% output Y(k) = R.X(k) + code.U(k) + L.T
code = strvcat( code, ' ', [ tabu '// output(s)' ] );
for i=1:R.p
    code = strvcat( code, [ tabu 'cAcc ' strAcc(R.l+R.n+i,:) '(' num2str(betaADD(R.l+R.n+i)) ',' num2str(betaG(R.l+R.n+i)) ',' num2str(gammaADD(R.l+R.n+i)) ');' ]);
    code = strvcat( code, fpscalprod(   R.Z(R.l+R.n+i,:) ,...
                                        strvcat( strT, strXn, strU),...
                                        betaZ(R.l+R.n+i,:),...
                                        gammaZ(R.l+R.n+i,:),...
                                        shiftZ(R.l+R.n+i,:),...
                                        strAcc(R.l+R.n+i,:) ) );
    if shiftTXY(i+R.l+R.n)
        code = strvcat( code, [ tabu strY(i,:) '= ' strAcc(R.l+R.n+i,:) ' >> ' num2str(shiftTXY(i+R.l+R.n)) ';' ],' ');
    else
        code = strvcat( code, [ tabu strY(i,:) '= ' strAcc(R.l+R.n+i,:) ';' ],' ');
    end
end

% states X(k) = P.X(k) + Q.U(k) + K.T
code = strvcat( code, ' ', [ tabu '// states' ] ); 
for i=1:R.n
    code = strvcat( code, [ tabu 'cAcc ' strAcc(R.l+i,:) '(' num2str(betaADD(R.l+i)) ',' num2str(betaG(R.l+i)) ',' num2str(gammaADD(R.l+i)) ');' ]);
    code = strvcat( code, fpscalprod(   R.Z(R.l+i,:) ,...
                                        strvcat( strT, strXn, strU),...
                                        betaZ(R.l+i,:),...
                                        gammaZ(R.l+i,:),...
                                        shiftZ(R.l+i,:),...
                                        strAcc(R.l+i,:) ) );
    if shiftTXY(i+R.l)
        codeS = [ ' >> ' num2str(shiftTXY(i+R.l)) ];
    else
        codeS = '';
    end
    if (isPnut)
        code = strvcat( code, [ tabu strXnp(i,:) '= ' strAcc(R.l+i,:)  codeS ';' ],' ');
    else
        code = strvcat( code, [ tabu strXn(i,:) '= ' strAcc(R.l+i,:) codeS ';' ],' ');
    end          
end

% permutation
if (isPnut)
    code = strvcat( code, ' ', [ tabu '//permutations' ] );
    code = strvcat( code, [ tabu 'cFp ptemp[' R.n '] = xn;' ]);
    code = strvcat( code, [ tabu 'xn = xnp;' ]);
    code = strvcat( code, [ tabu 'xnp = ptemp;' ]);
end


% end
code = strvcat(code, [ tabu 'return y;' ]);
code = strvcat(code, '}');
        
        




        
        