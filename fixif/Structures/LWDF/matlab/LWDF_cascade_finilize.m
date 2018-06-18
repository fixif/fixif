function [ SIF ] = LWDF_cascade_finilize( SIF1, SIF2, type)
%The function LWDF_cascade_finilize uses the outputs of SIF1 and SIF2, the
%upper and lower branches of filter correspondingly, in order to produce
%the result of type "type".
%SIF1 and SIF2 represent the cascades of stages, with input already
%connected to corresponding variables, but with output still in the last
%elements of their intermidiate vectors T1 and T2 correspondingly. 
%type may have following values:
%       'LPF': produce a low-pass output
%       'HPF': produce a high-pass output
%       'HLPF': produce both outputs Y(k) = [Y_LPF(k), Y_HPF_(k)]
%
%1. for LPF Y(k) = (SIF1_out - SIF2_out) / 2
%therefore we need an additional intermidiate variable t_lpf
%since SIF_out is the last element of SIF1.T and SIF2_out is the last
%element of SIF2.T then:
%
%t_lpf = zeros(1, nt1 + nt2 + 1);
%t_lpf(1, nt1) = -1;
%t_lpf(1, nt1 + nt2) = 1;
%t_lpf(1, nt1 + nt2 + 1) = 1;
%
%2. for HPF Y(k) = (SIF1_out + SIF2_out) / 2
%therefore we need an additional intermidiate variable t_lpf
%since SIF_out is the last element of SIF1.T and SIF2_out is the last
%element of SIF2.T then:
%
%t_hpf = zeros(1, nt1 + nt2 + 1);
%t_hpf(1, nt1) = -1;
%t_hpf(1, nt1 + nt2) = -1;
%t_hpf(1, nt1 + nt2 + 1) = 1;
%
%3. for the filter returning both low-pass and high-pass results we just
%use both temporary variables and asign each output to its variable. 
%
%ATTANTION AGAIN: we assume that first component of the result vector in such case is
%low-pass, and the second - high-pass.



[nt1, nt1] = size(SIF1.J);
[nx1, nt1] = size(SIF1.K);
[ny1, nt1] = size(SIF1.L);
[nt1, nu1] = size(SIF1.N);

[nt2, nt2] = size(SIF2.J);
[nx2, nt2] = size(SIF2.K);
[ny2, nt2] = size(SIF2.L);
[nt2, nu2] = size(SIF2.N);



if nt2 == 0 
    %the case of the system of first order, with only one simple block
    %i.e. the second branch is empty.
    %here we reconnect the input with an additional temporary variable
    %and them perform similar procedure as in the case of higher-order
    %filter
    
    t_out2 = zeros(1, nt1 + 1 + 2);
    t_out2(1, nt1+1) = 1;
    M = [ SIF1.M; zeros(1, nx1)];
    N = [ SIF1.N; 1 ];
        
    if strcmp(type, 'HLPF')
        t_lpf = zeros(1, nt1 + 1 + 2);
        t_lpf(1, nt1) = -1;
        t_lpf(1, nt1 + 1) = -1;
        t_lpf(1, nt1 + 1 + 1) = 1;

        t_hpf = zeros(1, nt1 + 1 + 2);
        t_hpf(1, nt1) = -1;
        t_hpf(1, nt1 + 1) = 1;
        t_hpf(1, nt1 + 1 + 2) = 1;

        y = zeros(2, nt1 + 1 + 2);
        y(1, nt1 + 1 + 1) = -0.5;
        y(2, nt1 + 1 + 2) = -0.5;
        
        J = [SIF1.J, zeros(nt1,3); t_out2; t_lpf; t_hpf ];
        
        K = [SIF1.K, zeros(nx1, 3)];
        L = -y;
        M = [SIF1.M; zeros(3, nx1)];
        N = [SIF1.N; 1; 0; 0];
        P = [SIF1.P];
        Q = zeros(nx1, 1);
        R = zeros(2, nx1); %here ny = 2
        S = zeros(2, 1);     %here ny = 2, nu = 1 

        SIF = FWR(J, K, L, M, N, P, Q, R, S, 'fixed', 'natural');   
    end
    
else
    
    t = zeros(1, nt1 + nt2 + 1);
    if strcmp(type, 'LPF')
        t(1, nt1) = -1;
        t(1, nt1 + nt2) = -1;
        t(1, nt1 + nt2 + 1) = 1;
        y = zeros(1, nt1 + nt2 + 1);
        y(1, nt1 + nt2 + 1) = -0.5;
    else if strcmp(type, 'HPF')
            t(1, nt1) = -1;
            t(1, nt1 + nt2) = 1;
            t(1, nt1 + nt2 + 1) = 1;
            y = zeros(1, nt1 + nt2 + 1);
            y(1, nt1 + nt2 + 1) = -0.5;
        else if strcmp(type, 'HLPF')
                t_lpf = zeros(1, nt1 + nt2 + 2);
                t_lpf(1, nt1) = -1;
                t_lpf(1, nt1 + nt2) = -1;
                t_lpf(1, nt1 + nt2 + 1) = 1;

                t_hpf = zeros(1, nt1 + nt2 + 2);
                t_hpf(1, nt1) = -1;
                t_hpf(1, nt1 + nt2) = 1;
                t_hpf(1, nt1 + nt2 + 2) = 1;

                y = zeros(2, nt1 + nt2 + 2);
                y(1, nt1 + nt2 + 1) = -0.5;
                y(2, nt1 + nt2 + 2) = -0.5;
            end
        end
    end

    if ~strcmp(type, 'HLPF')   %if it is a one-output filter
        J = [SIF1.J, zeros(nt1, nt2), zeros(nt1, 1); zeros(nt2, nt1), SIF2.J, zeros(nt2, 1); t];
        K = [SIF1.K, zeros(nx1, nt2), zeros(nx1, 1); zeros(nx2, nt1), SIF2.K, zeros(nx2, 1)];
        %K = [SIF1.K, zeros(nx1, nt2), 0; zeros(nx2, nt1), SIF2.K, 0];
        L = -y;
        M = [SIF1.M, zeros(nt1, nx2); zeros(nt2, nx1), SIF2.M; zeros(1, nx1 + nx2)];
        N = [SIF1.N; SIF2.N; 0];
        P = [SIF1.P, zeros(nx1, nx2); zeros(nx2, nx1), SIF2.P];
        Q = zeros(nx1 + nx2, 1);
        S = zeros(1,1);     %here ny = 1, nu = 1 
        R = zeros(1, nx1 + nx2);

        SIF = FWR(J, K, L, M, N, P, Q, R, S, 'fixed', 'natural');

    else                        %if it is a two-output filter
        J = [SIF1.J, zeros(nt1, nt2), zeros(nt1, 2); zeros(nt2, nt1), SIF2.J, zeros(nt2, 2); t_lpf; t_hpf];
        K = [SIF1.K, zeros(nx1, nt2), zeros(nx1, 2); zeros(nx2, nt1), SIF2.K, zeros(nx2, 2)];
        L = -y;
        M = [SIF1.M, zeros(nt1, nx2); zeros(nt2, nx1), SIF2.M; zeros(2, nx1 + nx2)];
        N = [SIF1.N; SIF2.N; 0; 0;];
        P = [SIF1.P, zeros(nx1, nx2); zeros(nx2, nx1), SIF2.P];
        Q = zeros(nx1 + nx2, 1);
        R = zeros(2, nx1 + nx2);
        S = zeros(2,1);     %here ny = 2, nu = 1 

        SIF = FWR(J, K, L, M, N, P, Q, R, S, 'fixed', 'natural');   

    end
    
end  
    
    
end
    


