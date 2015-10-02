function [ SIF ] = LWD_SIF_setinput(SIF)
%The function LWD_SIF_setio takes a SIF object and connects its input u(k) to
%the first intermidiate variable. This way if before the filter had all its variables
%in the temporary vector T, with inputs and outputs not connected to
%anything, then in this function we give the initiate value for the filter
%input. 
%
%We assume that adaptors were cascaded in such
%order that the input variable t_sys1_input for the Stage0 is the first
%element of the vector T.


%In order to reconnect input u(k) with t_sys1_input we need to set
% N[1,nu] = 1;           %we suppose here that nu = 1;


% [nt, nt] = size(SIF.J);
% [nx, nt] = size(SIF.K);
% [ny, nt] = size(SIF.L);
[nt, nu] = size(SIF.N);

if nu > 1
    error('Size of nu is larger than 1.')
end

SIF.N(1,1) = 1;
%SIF = set(SIF, N(1,1), 1);

end

