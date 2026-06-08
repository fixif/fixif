function [ SIF ] = LWDF_cascade_adaptors(J1,K1,L1,M1,N1,P1,Q1,R1,S1, J2,K2,L2,M2,N2,P2,Q2,R2,S2 )
%LWDF_cascade_adaptors cascades two adapters: first of type 'A' and second 
%of type 'B'
%Input:
% J1,K1,...,S1 - SIF representation of system1
% J2,K2,...,S2 - SIF representation of system2
%
%Output:
%SIF - cascade if system1 and system2. 
%ATTENTION: we set number of inputs and outputs to 1 and leave the
%corresponding rows zeros. All the information is contained in Temporary
%variables and X - state variables. Inputs and Outputs must be later
%connected with corresponding temporary variables.
%
%System 1 is of type 'A', which means two inputs and two outputs.
%System 2 is of type 'B', whoch means one input and one output.
%
%The function connects output2 of system1 to the input of system2, and
%output of system2 to the input2 of system1.
%This is achived with placing '-1' in final matrix J at following 
%coordinates:
%   J(sys2_input, sys1_output2) = -1;
%   J(sys1_input2, sys2_output) = -1;
%



[nt1, nt1] = size(J1);
[nx1, nt1] = size(K1);
[ny1, nt1] = size(L1);
[nt1, nu1] = size(N1);

[nt2, nt2] = size(J2);
[nx2, nt2] = size(K2);
[ny2, nt2] = size(L2);
[nt2, nu2] = size(N2);

%we set there is only one input u(k) for the system
nu1 = 1;
nu2 = 0;
ny1 = 1;
ny2 = 0;

% When we cascade the stage, we always have that
% system 1 is of type A and system 2 is of type B
% and we connect them
% sys1_output2 = sys2_input and sys2_output = sys1_input2

%Getting index of element sys1_output2
sys1_output2 = nt1;

%Getting index of element sys_2_input
sys2_input = nt1 + 1;

%Getting index of element sys1_input2
sys1_input2 = 2;

%Getting index of element sys2_output
sys2_output = nt1 + nt2;


J = [J1, zeros(nt1, nt2); zeros(nt2, nt1), J2];
K = [K1, zeros(nx1, nt2); zeros(nx2, nt1), K2];
L = zeros(1, nt1 + nt2);
M = [M1, zeros(nt1, nx2); zeros(nt2, nx1), M2];
P = [P1, zeros(nx1, nx2); zeros(nx2, nx1), P2];
R = zeros(1, nx1 + nx2);
N = zeros(nt1 + nt2, 1);
Q = zeros(nx1 + nx2, 1);
S = zeros(1, 1);
% 
% N = [N1, zeros(nt1, nu2); zeros(nt2, nu1), N2];
% Q = [Q1, zeros(nx1, nu2); zeros(nx2, nu1), Q2];
% S = [S1, zeros(ny1, nu1); zeros(ny2, nu1), S2];

%Connecting inputs
J(sys2_input, sys1_output2) = -1;
J(sys1_input2, sys2_output) = -1;


if istril(J) ~= 1
    %Here matrix J is not lower-triangular
    %We permute its rows returning it to lower-triangular form
    %Order of permutation is ontained by topological sort with DFS method
    
    SIF = FWR(J, K, L, M, N, P, Q, R, S, 'fixed', 'natural');
    [~,~, post, ~,~, ~] = dfs(sparse(J - eye(size(J))), 1, 1);
    %post - containes order of permutation
    SIF = SIFreorganize(SIF, post);

end

end

