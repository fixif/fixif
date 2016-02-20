%Purpose:
% Perform a $L_2$-scaling on the FWR
%
%Syntax:
% R = l2scaling(R, Wcii)
% [U,Y,W] = l2scaling(R)
%
%Parameters:
% R: FWR object
% U,Y,W : transformation matrices applied on R
% Wcii : vector (size $(1,l+n)$) of controllability gramians desired
%	   : if 'Wcii' is omitted, strict $L_2$-scaling is applied ( 'Wcii=ones(1,n+l)' )
%
% $Id: l2scaling.m 208 2009-01-05 13:52:19Z fengyu $


function [R,Y,W] = l2scaling(R, Wcii)

% args
if nargin<2
	Wcii=ones(1,R.l+R.n);
end
if size(Wcii,2)==1
	Wcii=Wcii';
end

% build U,W
U = sqrt( diag(diag( R.Wc )./ Wcii(R.l+1:R.l+R.n)' ) );
if R.l>0
	W = sqrt( diag(diag( inv(R.J)*(R.N*R.N' + R.M*R.Wc*R.M')*inv(R.J)' )./Wcii(1:R.l)' ) );
else
	W = [];
end

% ind where U or W is null (-> ie non-commandable states)
epsilon=1e-15;
indU=find(diag( R.Wc )<epsilon);
Hnorm=norm(ss(R));
if ~isempty(indU)
	for i=indU'
		U(i,i) = Hnorm/sqrt(R.Wo(i,i)*Wcii(R.l+i));
	end
end
indW=find(diag( inv(R.J)*(R.N*R.N' + R.M*R.Wc*R.M')*inv(R.J)' )<epsilon);
if ~isempty(indW)
	Woii=inv(R.J)'*(R.L'*R.L + R.K'*R.Wo*R.K)*inv(R.J);
	for i=indW'
		W(i,i) = Hnorm/sqrt( Woii(i,i)*Wcii(i) );
	end
end


% Y
Y = eye(R.l);
%Y= inv(W);

% final transformation
if nargout==1
	R = transform(R, U,Y,W);
else
	R = U;
end


if rcond(Y)<1e-10
	display('warning');
end

%Description:
% 	Perform a $L_2$-scaling.\\
% 	The scaling forces the transfer functions from the inputs to the states and the intermediate variables to have a unitary $L_2$-norm. Theses norms are given by the diagonal terms of $W_c$ and $J^{-1}\pa{NN^\top+MW_cM^\top}J^{-\top}$.\\
% 	The $L_2$-scaling is a $\mt{U}\mt{Y}\mt{W}$-transformation where $\mt{U}$ and $\mt{W}$ are diagonal with:
% 	\begin{eqnarray}
% 		\pa{\mt{U}}_{ii} &=& \sqrt{\pa{W_c}_{ii}} \\
% 		\pa{\mt{W}}_{ii} &=& \sqrt{\pa{J^{-1}\pa{NN^\top+MW_cM^\top}J^{-\top}}_{ii}}
% 	\end{eqnarray}
%
%	It is also possible to assign some particular values for the diagonal terms of the two gramians.

%See also: <@FWR/relaxedl2scaling>

%References:
%	\cite{Feng09a} Y. Feng, P. Chevrel, and T. Hilaire. A practival strategy of an efficient and sparse FWL implementation of LTI filters. In submitted to ECC'09, 2009.\\
%	%\cite{Hila09a}	T. Hilaire. Low parametric sensitivity realizations with relaxed l2-dynamic-range-scaling constraints. submitted to IEEE Trans. on Circuits \& Systems II, 2009.




