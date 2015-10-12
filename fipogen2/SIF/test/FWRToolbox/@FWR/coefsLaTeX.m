%Purpose:
% Return a \LaTeX code to represent the fixed-point coefficients
%
%Syntax:
% str = coefsLaTeX( R)
%
%Parameters:
% str: \LaTeX code
% R: FWR object
%
%$Id$


function str = coefsLaTeX( R)

% FPIS?
if isempty(R.FPIS)
    error( 'The realization must have a valid FPIS');
end

tabu='	';
str = ['\begin{pmatrix}'];


%loop on the coefficient
for i=1:R.l+R.n+R.p
	for j=1:R.l+R.n+R.m
		
		if j==1
			coef = tabu;
		end
		if ~isinf(R.FPIS.gammaZ(i,j))
			coef = [ coef num2str(round( R.Z(i,j)*2^R.FPIS.gammaZ(i,j) ),'%+d') ];
			coef = [ coef '\cdot2^{' num2str(-R.FPIS.gammaZ(i,j)) '}' ];
		else
			coef = [ coef '0' ];
		end
		if j<R.l+R.n+R.m
			coef = [coef ' & '];
		elseif i<R.l+R.n+R.p
			coef = [ coef ' \\'];
		end

	end
	str = strvcat(str,coef);
end
		
str = strvcat( str,'\end{pmatrix}');
