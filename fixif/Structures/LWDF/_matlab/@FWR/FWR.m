%Purpose:
% FWR class' constructor
%
%Syntax:
% R = FWR()
% R = FWR(R1)
% R = FWR(J,K,L,M,N,P,Q,R,S, fp, block)
%
%Parameters:
% R: FWR object created
% R1: FWR object to be copied
% J,K,...,S: matrices of the realization
% fp: fixed-point or floating-point representation
%		:"fixed" (default value) or "floating"
% block: block-representation scheme. The coefficients in a same block share the same representation (same scale factor, etc...). Take the following values:
%		: "full": same representation for all coefficients of R
%		: "natural" (default value): blocks are made of matrices J,K,L,M,N,P,Q,R,S
%		: "none": each coefficient has its own representation (according to its value)
%
% $Id: FWR.m 208 2009-01-05 13:52:19Z fengyu $


function R = FWR(varargin)

if nargin==0
    % empty realization
    R.l=0; R.m=0; R.n=0; R.p=0;
    R.J=[]; R.K=[]; R.L=[]; R.M=[]; R.N=[];
    R.P=[]; R.Q=[]; R.R=[]; R.S=[]; R.Z=[];
    R = class(R,'FWR');
    
elseif nargin==1
    % copy a FWR
    if isa(varargin{1},'FWR')
        R = varargin{1};
    else
        error('error in constructor FWR - invalid argument');
    end
elseif (nargin<9) | (nargin>11)
    error('error in constructor FWR - invalid number of arguments');
else
    % create a FWR from J,K,L,...,S matrices
    R.l=0; R.m=0; R.n=0; R.p=0;
    R.J = varargin{1};
    R.K = varargin{2};
    R.L = varargin{3};
    R.M = varargin{4};
    R.N = varargin{5};
    R.P = varargin{6};
    R.Q = varargin{7};
    R.R = varargin{8};
    R.S = varargin{9};
    R.Z=[];
    % build the class
    R = class(R,'FWR');
    % compute the other parameters
    R = computelmnp(R);
    R=computeZ(R);
end


%Description:
%	Constructor of the \matlab{FWR} class.\\
%	It could create an empty object ($l=m=n=p=0$), copy an object or create a \matlab{FWR} object from matrices $J$ to $S$: in that case, the other parameters are deduced (only $0$, $1$ or $-1$ are considered as exactly implemented).

%See also: <@FWS/FWS>