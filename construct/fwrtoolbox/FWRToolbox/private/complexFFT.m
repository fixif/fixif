%Purpose:
% Create FFT with complex coefficients (for FFT2FWR)
% (matrices J,L,N and S are used)
%
%Syntax:
% [J,L,N,S] = complexFFT(n, toSimplify)
%
%Parameters:
% J,L,N,S: FWR matrices with complex coefficients
% n: size of the FFT
% toSimplify: 1 (default) if the simplification (level=1) is done at each recursive step
%
% $Id: complexFFT.m 197 2008-12-23 15:16:19Z hilaire $


function [J,L,N,S] = complexFFT(n, toSimplify)

% args
if nargin<2
	toSimplify=1;
end


if n==2
	J = ones(0,0);
	L = ones(2,0);
	N = ones(0,2);
	S = [1 1; 1 -1];
elseif fix(log2(n))~=log2(n)
	error('n is not a power of 2')
else
	if mod( log2(n),2 )==0
		k = sqrt(n);
		[Jk,Lk,Nk,Sk] = complexFFT(k, toSimplify);
		[J,L,N,S] = assemble( Jk,Lk,Nk,Sk,Jk,Lk,Nk,Sk, toSimplify);
	else
		k = 2^floor(log2(n)/2);
		[Jk,Lk,Nk,Sk] = complexFFT(k, toSimplify);
		[J2k,L2k,N2k,S2k] = assemble( ones(0,0),ones(2,0),ones(0,2),[1 1; 1 -1],Jk,Lk,Nk,Sk, toSimplify);
		[J,L,N,S] = assemble( Jk,Lk,Nk,Sk,J2k,L2k,N2k,S2k, toSimplify);
	end
end


%
function [J,L,N,S] = assemble(J1,L1,N1,S1,J2,L2,N2,S2, toSimplify)

l1=size(J1,1); l2=size(J2,1);
r=size(S1,1); s=size(S2,1);
n=r*s;
% time depends on size n
if n<=16
	% faster if n<=16
	J = [ kron( eye(r), J2) zeros(l2*r,2*n+l1*s) ;
		-kron( eye(r), L2) eye(n) zeros(n,n+l1*s) ;
		zeros(n,l2*r) -twiddleM(s,n) eye(n) zeros(n,l1*s) ;
		zeros(l1*s,l2*r+n) -kron( N1,eye(s) ) kron(J1,eye(s)) ];
	N = [  kron( eye(r), N2)*strideM(r,n) ;
		kron(eye(r), S2)*strideM(r,n) ;
		zeros(n+l1*s,n)];
	L = [ zeros(n,l2*r+n) kron( S1, eye(s) ) kron( L1, eye(s) ) ];
	S = zeros(n,n);
else
	% faster for big matrix
%	J = zeros(l2*r+2*n+l1*s);
	J = sparse([],[],[],l2*r+2*n+l1*s,l2*r+2*n+l1*s,ceil(7/3*(l2*r+2*n+l1*s))+1);	% 7/3*... to be exact
	J(1:l2*r,1:l2*r) = kron( eye(r), J2);
	J(l2*r+1:l2*r+n,1:l2*r) = -kron( eye(r), L2);
	J(l2*r+1:l2*r+n,l2*r+1:l2*r+n) = eye(n);
	J(l2*r+n+1:l2*r+2*n,l2*r+1:l2*r+n) = -twiddleM(s,n);
	J(l2*r+n+1:l2*r+2*n,l2*r+n+1:l2*r+2*n) = eye(n);
	J(l2*r+2*n+1:l2*r+2*n+l1*s,l2*r+n+1:l2*r+2*n) = -kron( N1,eye(s) );
	J(l2*r+2*n+1:l2*r+2*n+l1*s,l2*r+2*n+1:l2*r+2*n+l1*s) = kron(J1,eye(s));
	
%	N = zeros(l2*r+2*n+l1*s,n);
	N = sparse([],[],[],l2*r+2*n+l1*s,n,2*n+1);		% 2*n to be exact
	N(1:l2*r,:) = kron( eye(r), N2)*strideM(r,n);
	N(l2*r+1:l2*r+n,:) = kron(eye(r), S2)*strideM(r,n);
	
%	L = zeros(n,l2*r+2*n+l1*s);
	L = sparse([],[],[],n,l2*r+2*n+l1*s,2*n+1);		% 2*n to be exact
	L(1:n,l2*r+n+1:l2*r+2*n) = kron( S1, eye(s) );
	L(1:n,l2*r+2*n+1:l2*r+2*n+l1*s) = kron( L1, eye(s) );
	S = sparse([],[],[],n,n,0);
end

if toSimplify
	R = FWR( J, zeros(0,size(J,1)), L, zeros(size(J,1),0), N, zeros(0,0), zeros(0,n), zeros(n,0), S);
	Rs=simplify(R);
	J=Rs.J;
	L=Rs.L;
	N=Rs.N;
	S=Rs.S;
end


%Description:
%	This function is called by \funcName{FFT2FWR}

%See also: <FFT2FWR>, <@FWR/simplify>, <strideM>, <twiddleM>

