
% dummy class from the FWR toolbox

function R = FWR(varargin)


if nargin==0
    % empty realization
    R.l=0; R.m=0; R.n=0; R.p=0;
    R.J=[]; R.K=[]; R.L=[]; R.M=[]; R.N=[];
    R.P=[]; R.Q=[]; R.R=[]; R.S=[];
    R = class(R,'FWR');
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
    % build the class
    R = class(R,'FWR');
end
