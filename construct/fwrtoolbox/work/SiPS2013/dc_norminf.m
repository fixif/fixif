function [dc, b] = dc_norminf(H)
dc = dcgain(H);
[Yimp Timp] = impulse(H);
b = squeeze(sum(abs(Yimp)))';

% de manière équivalente
%sum=zeros(1,9);for k=0:1e3;sum=sum+abs(H2.C*H2.A^k*H2.B);end