function [ J,K,L,M,N,P,Q,R,S] = LWDF_adaptorSIF(gamma, type)
%LWDF_adaptorSIF constructs an adapter of one of two types depending on the 
%value of the variable type:
%   type = A: adaptor with two inputs, two outputs and a delay 
%   type = B: adaptor with one input and one output with a delay and 
%             loop in the DFG
% Depending on the value of gamma there exist 4 types of adapters [ref]
if(abs(gamma) > 1)
    error('Gamma is not in the range [-1,1]')
end

                                                                                                                                                                                                                                                                 
    %Type 1
if gamma > 0.5 && gamma < 1
    alpha = 1 - gamma;
    switch type
        case 'A'
          J = [1 0 0 0 0 0; 
                 0 1 0 0 0 0;
                 -1 1 1 0 0 0;
                 0 -1 -alpha 1 0 0;
                 0 0 1 -1 1 0;
                 0 0 0 0 0 1];
            K = -[0 0 0 -1 0 0];
            L = -[0 0 0 0 0 0];
            M = [0; 0; 0; 0; 0; 1];
            N = [0; 0; 0; 0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
        case 'B'
            J = [1 0 0 0;
                 -1 1 0 0;
                 0 -alpha 1 0;
                 0 1 -1 1];
            K = -[0 0 -1 0];
            L = -[0 0 0 0];
            M = [0; -1; 1; 0];
            N = [0; 0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
    end
end

  %Type 2
if gamma > 0 && gamma <= 0.5
    alpha = gamma;
    switch type
        case 'A'
            J = [1 0 0 0 0;
                 0 1 0 0 0;
                 1 -1 1 0 0;
                 0 -1 -alpha 1 0;
                 0 0 0 0 1];
            K = -[-1 0 -alpha 0 0];
            L = -[0 0 0 0 0];
            M = [0; 0; 0; 0; 1];
            N = [0; 0; 0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
        case 'B'
            J = [1 0 0;
                1 1 0;
                0 -alpha 1];
            K = -[-1 -alpha 0];
            L = -[0 0 0];
            M = [0; 1; 1];
            N = [0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
           
    end
end

  %Type 3
if gamma >= -0.5 && gamma < 0
    alpha = abs(gamma);
    switch type
        case 'A'
            J = [1 0 0 0 0;
                 0 1 0 0 0;
                 -1 1 1 0 0;
                 0 1 -alpha 1 0;
                 0 0 0 0 1];
            K = -[1 0 -alpha 0 0];
            L = -[0 0 0 0 0];
            M = [0; 0; 0; 0; 1];
            N = [0; 0; 0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
        case 'B'
            J = [1 0 0;
                 -1 1 0;
                 0 -alpha 1];
            K = -[1 -alpha 0];
            L = -[0 0 0];
            M = [0; -1; -1];
            N = [0; 0; 0;];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
    end
end

  %Type 4
if gamma > -1 && gamma < -0.5
    alpha = 1 + gamma;
    switch type
        case 'A'
            J = [1 0 0 0 0 0;
                 0 1 0 0 0 0;
                 1 -1 1 0 0 0;
                 0 1 -alpha 1 0 0;
                 0 0 1 -1 1 0;
                 0 0 0 0 0 1];
            K = -[0 0 0 -1 0 0];
            L = -[0 0 0 0 0 0];
            M = [0; 0; 0; 0; 0; 1];
            N = [0; 0; 0; 0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
        case 'B'
            J = [1 0 0 0;
                 1 1 0 0;
                 0 -alpha 1 0
                 0 1 -1 1];
            K = -[0 0 -1 0];
            L = -[0 0 0 0];
            M = [0; 1; -1; 0];
            N = [0; 0; 0; 0];
            P = [0];
            Q = [0];
            R = [0];
            S = [0];
    end
end
            
        



end

