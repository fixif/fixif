function [ SIF ] = LWDF2SIF(LWDF, filterOrder, outputType)
%The function LWDF2SIF converts a Lattice Wave digital filter to its
%Specialized Implicit Form analogue. 
%Inputs:
%   -LWDF structure
%   -filterOrder - filter order, must be an EVEN number
%   -outputType - inidicates what output we desire:
%       * 'LPF' - lowpass filter
%       * 'HPF' - highpass filter
%       * 'HLPF' - 2 output gilter, with Low-pass section in first component
%                 and highpass in second
%   
%
%The input structure LWDF must contain the filds:
%   LWDF.wdaCodes 
%   LWDF.gamma
%where wdaCodes is an array of 2 strings, which describe which adaptors are
%used and at what positions. The following adaptor/delay combinations are
%recognized:
%   't' - a single delay element
%   's' - one 2-port and one delay element
%   'S' - one 2-port with cascaded delay elements
%   'd' - two 2-ports with two delay elements
%   'D' - two 2-ports with two times two cascaded delay elements
%   'x' - only an interconnection in this slot
%LWDF.gamma gives the coefficient values for the 2-ports.

SIF1 = FWR();   %top branch
SIF2 = FWR();   %lower branch

[~, n] = size(LWDF.wdaCodes);

%creating SIF for the top branch
for i = 1:n
    switch(LWDF.wdaCodes(1,i))
        case 's'
            [ J,K,L,M,N,P,Q,R,S] = LWDF_adaptorSIF(LWDF.gamma(1,i,1), 'B');
            SIF1 = FWR(J,K,L,M,N,P,Q,R,S, 'fixed', 'natural');
        case 'd'
            %generating SIF for the first adapter in current stage
            [ J_A,K_A,L_A,M_A,N_A,P_A,Q_A,R_A,S_A] = LWDF_adaptorSIF(LWDF.gamma(1,i,1), 'A');
           %generating SIF for the second adapter in current stage
            [ J_B,K_B,L_B,M_B,N_B,P_B,Q_B,R_B,S_B] = LWDF_adaptorSIF(LWDF.gamma(2,i,1), 'B');
            %generating SIF for the current stage
            SIF_currentStage= LWDF_cascade_adaptors(J_A,K_A,L_A,M_A,N_A,P_A,Q_A,R_A,S_A, J_B,K_B,L_B,M_B,N_B,P_B,Q_B,R_B,S_B);
            %cascading current stage with the upper branch
            SIF1 = LWDF_cascade_stages(SIF1, SIF_currentStage);
    end
end
%connecting the input of the system with the corresponding temp variable
%for the top branch
SIF1 = LWD_SIF_setinput(SIF1);


%creating SIF for the lower branch
for i = 1:n
    switch(LWDF.wdaCodes(2,i))
        case 's'
            error('This can not happen');
        case 'd'
            %generating SIF for the first adapter in current stage
            [ J_A,K_A,L_A,M_A,N_A,P_A,Q_A,R_A,S_A] = LWDF_adaptorSIF(LWDF.gamma(1,i,2), 'A');
           %generating SIF for the second adapter in current stage
            [ J_B,K_B,L_B,M_B,N_B,P_B,Q_B,R_B,S_B] = LWDF_adaptorSIF(LWDF.gamma(2,i,2), 'B');
            
            if(size(SIF2.Z) == 0)    %if this is the first stage on this branch
                SIF2 = LWDF_cascade_adaptors(J_A,K_A,L_A,M_A,N_A,P_A,Q_A,R_A,S_A, J_B,K_B,L_B,M_B,N_B,P_B,Q_B,R_B,S_B);
            else
                %generating SIF for the current stage
                SIF_currentStage= LWDF_cascade_adaptors(J_A,K_A,L_A,M_A,N_A,P_A,Q_A,R_A,S_A, J_B,K_B,L_B,M_B,N_B,P_B,Q_B,R_B,S_B);
                %cascading current stage with the upper branch
                SIF2 = LWDF_cascade_stages(SIF2, SIF_currentStage);
            end
            
    end
end
%connecting the input of the system with the corresponding temp variable
%for the top branch
[m, n] = size(SIF2.Z);
if m ~= 0
    SIF2 = LWD_SIF_setinput(SIF2);
end
    


%connecting the top and the lower branches
SIF = LWDF_cascade_finilize(SIF1, SIF2, outputType);


end

