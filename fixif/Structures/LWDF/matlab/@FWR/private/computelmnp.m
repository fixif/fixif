%Purpose:
% Compute the dimension $l$, $m$, $n$ and $p$ of a FWR object (from its parameters $J$, $K$, ..., $S$) and check the dimensions
%
%Syntax:
% R=updatelmnp(R)
%
%Parameters:
% R: FWR object
%
%
% $Id: computelmnp.m 208 2009-01-05 13:52:19Z fengyu $


function R=computelmnp(R)

% check dimensions
% P (n,n)
[p1,p2] = size(R.P);
if (p1~=p2)
    error ('error with the dimension of P')
else
    R.n=p1;
end    
% J (l,l)
[j1,j2] = size(R.J);
if (j1~=j2)
    error ('error with the dimension of J')
else
    R.l=j1;
end
% K (n,l)
[k1,k2] = size(R.K);
if ( (k1~=R.n) | (k2~=R.l) )
    error ('error with the the dimension of K')
end
% L (p,l)
[l1,l2] = size(R.L);
if (l2~=R.l)
    error ('error with the dimension of L')
else
    R.p=l1;
end
% M (l,n)
[m1,m2] = size(R.M);
if ( (m1~=R.l) | (m2~=R.n) )
    error ('error with the dimension of M')
end
% N (l,m)
[n1,n2] = size(R.N);
if (n1~=R.l)
    error ('error with the dimension of N')
else
    R.m=n2;
end   
% Q (n,m)
[q1,q2] = size(R.Q);
if ( (q1~=R.n) | (q2~=R.m) )
    error ('error with the dimension of Q')
end
% R (p,n)
[r1,r2] = size(R.R);
if ( (r1~=R.p) | (r2~=R.n) )
    error ('error with the dimension of R')
end
% S (p,m)
[s1,s2] = size(R.S);
if ( (s1~=R.p) | (s2~=R.m) )
    error ('error with the dimension of S')
end



%Description:
% 	\begin{center}\I{Internal function}\end{center}
%	Compute the size $l$, $m$, $n$ and $p$ of a FWR realization.\\
%	It also checks the concordance of the size of matrices $J$, $K$, $L$, $M$, $N$, $P$, $Q$, $R$, $S$ . 
