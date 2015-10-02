function [ SIF ] = LWDF_cascade_stages(SIF1, SIF2)
%The function LWDF_cascade_stages takes two SIF matrices and cascades them 
%to such a system, that the output of system 1 is the input of the system 2

%Note that we assume that these SIFs are in the intermidiate form, i.e.
%matrices J may be not lower-triangular and the inputs and outputs of the
%sustems are all zeroes. Therefore all the actual inouts and outputs are in
%the intermidiate variables. For finalizing the cascades, we must call a
%function LWDF_cascade_finalize, which will connect the intermidiate input,
%which was not set before, to the input variable, and the same with the
%output.

%Therefore, in order to connect two systems like that all we need is to set
%the element J(sys2_input, sys1_output) to 1. 

[nt1, nt1] = size(SIF1.J);
[nx1, nt1] = size(SIF1.K);
[ny1, nt1] = size(SIF1.L);
[nt1, nu1] = size(SIF1.N);

[nt2, nt2] = size(SIF2.J);
[nx2, nt2] = size(SIF2.K);
[ny2, nt2] = size(SIF2.L);
[nt2, nu2] = size(SIF2.N);

ny = 1;
nu = 1;


%Getting the index of the element sys1_output
sys1_output = nt1;

%Getting the index of the element sys2_input
sys2_input = nt1 + 1;

J = [SIF1.J, zeros(nt1, nt2); zeros(nt2, nt1), SIF2.J];
K = [SIF1.K, zeros(nx1, nt2); zeros(nx2, nt1), SIF2.K];
%L = [SIF1.L, zeros(ny1, nt2); zeros(ny2, nt1), SIF2.L];
M = [SIF1.M, zeros(nt1, nx2); zeros(nt2, nx1), SIF2.M];
P = [SIF1.P, zeros(nx1, nx2); zeros(nx2, nx1), SIF2.P];
%R = [SIF1.R, zeros(ny1, nx2); zeros(ny2, nx1), SIF2.R];

L = zeros(ny, nt1 + nt2);
R = zeros(ny, nx1 + nx2);
N = zeros(nt1 + nt2, nu);
Q = zeros(nx1 + nx2, nu);
S = zeros(ny, nu);


%Connect the input of system 2 to the output of the system 1
J(sys2_input, sys1_output) = -1;

%Create the result SIF
SIF = FWR(J, K, L, M, N, P, Q, R, S, 'fixed', 'natural');
end

