% lmimultifilter.m

% solving multiobjective optimal realization problem using LMI's 
%
% There are 3 LMI problems solved:
% The first 2 are to get the target bounds for the 2 H-infinity subproblems
% The third LMI is the multiobjective problem
%
% JFW 7/6/11

clear all; format long; format compact
%% 3 examples

% (1) random example
if(1)
    nk=7;G=drss(nk,1,1);
end
% (2) simple 2nd order 
if(0)
    G=ss([-.5 .2;0 -.53],[0;1],[1,0],0,1);
end

% (3) Gevers & Li example
if(0)
    [G]=geversmodel2;     
    G=canon(G,'modal') % put in modal form due to conditioning problems
    %[G_bal,Hsv,TI_bal,T_bal]=balreal(G); G=G_bal;% get balanced realization
end


nk=size(G.a,2); % state dimension

A=G.a;B=G.b;C=G.c; %state space matrices

% display sensitivities and stability radius
dispsensitivities(A,B,C, 'original system') 

[G_bal,Hsv,TI_bal,T_bal]=balreal(G); % get balanced realization for comparison
[gamma_a_bal,gamma_eta_bal]=dispsensitivities(G_bal.a,G_bal.b,G_bal.c, 'balanced realization');
 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
%%
% Problem 1
% minimize S_A norm, gamma_a,   to get target for multiobjective minimization
if(1)
    
    
    % binary search on gamma
    gamma_a_max=gamma_a_bal*1.1
    gamma_a_min=0
    gamma_a=gamma_a_max
    tmin= 1
    while((gamma_a_max-gamma_a_min)>1e-8)
        
        M=[A, B*C, zeros(nk,nk); 
            zeros(nk,nk),A,eye(nk)/gamma_a; 
            eye(nk),zeros(nk,2*nk)]; 
        
        setlmis([])
        
        % DECISION VARIABLES 
        XQ=lmivar(1,[2*nk 1;nk 1]) % diag([X,Q])
                                   % type=1: Symmetric matrices with a 
                                   %         block-diagonal structure
        
        % DEFINE LMIs
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % 1st LMI: M1' XQ M1 < XQ
        lmiterm([1 1 1 XQ],M',M)     % M' XQ M
        
        % rhs
        lmiterm([-1 1 1 XQ],1,1)     %  XQ
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % 2nd LMI: 0<XQ
        % rhs
        lmiterm([-2 1 1 XQ],1,1)     %  XQ
         
        LMISYS1 = getlmis;
        
        % now solve
        [tmin,pfeas] = feasp(LMISYS1);
        if (tmin<0),
            gamma_a_max=gamma_a;
        else
            gamma_a_min=gamma_a;
        end
        gamma_a=(gamma_a_max+gamma_a_min)/2
        
    end
    gamma_a_opt=gamma_a_max
    
    Qf=dec2mat(LMISYS1,pfeas,XQ);
    
    % get  realization solution
    Q_0=Qf(2*nk+1:3*nk,2*nk+1:3*nk); % extract optimal Q from XQ
    T=inv(sqrtm(Q_0)) % Q=inv (T'T)
    
    % display sensitivities
    dispsensitivities(inv(T)*A*T,inv(T)*B,C*T, 'H-infty optimal S_A') 

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
% Problem 2
% maximize stability radius , 1/gamma_a, to get target for multiobjective minimization
if(1)

    
    % binary search on gamma
    gamma_eta_max=gamma_eta_bal*1.1
    gamma_eta_min=0;
    gamma_eta=gamma_eta_max;
    tmin= 1;
    while((gamma_eta_max-gamma_eta_min)>1e-8)
        
        M=[A,  eye(nk)/gamma_eta; 
            eye(nk),zeros(nk,nk)]; 
        
        setlmis([])
        
        % DECISION VARIABLES 
        YQ=lmivar(1,[nk 1;nk 1]) % diag([Y,Q])
                                   % type=1: Symmetric matrices with a 
                                   %         block-diagonal structure
        
        % DEFINE LMIs
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % 1st LMI: M1' XQ M1 < XQ
        lmiterm([1 1 1 YQ],M',M)     % M' XQ M
        
        % rhs
        lmiterm([-1 1 1 YQ],1,1)     %  XQ
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % 2nd LMI: 0<XQ
        % rhs
        lmiterm([-2 1 1 YQ],1,1)     %  XQ
         
        LMISYS2 = getlmis;
        
        % now solve
        [tmin,pfeas] = feasp(LMISYS2);
        if (tmin<0),
            gamma_eta_max=gamma_eta;
        else
            gamma_eta_min=gamma_eta;
        end
        gamma_eta=(gamma_eta_max+gamma_eta_min)/2
        
    end
    gamma_eta_opt=gamma_eta_max
    
    Qf=dec2mat(LMISYS2,pfeas,YQ);
    
    % get solution realization 
    Q_0=Qf(nk+1:2*nk,nk+1:2*nk); % extract optimal Q from YQ
    T=inv(sqrtm(Q_0)) % Q=inv (T'T)
    
    % display sensitivities
    dispsensitivities(inv(T)*A*T,inv(T)*B,C*T, 'max stability radius'); 

end 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
%% 
% Problem 3 - Main MO problem
% minimize weighted ensitivity  for S_B and S_C sensitivity minimization st
% ||S_A||<gamma_a  ||(zI - A_T)^{-1}||<gamma_eta
if(1)
    % from previous run of Problem 1&2 for Gevers & Li model
    % gamma_a_opt=1.717005874231044e+002; 
    %gamma_eta_opt=1.315295080295927e+002;
    
    % free parameters for MO problem
    gamma_a=2*gamma_a_opt;
    gamma_eta=3*gamma_eta_opt;
    lambda_b=6;
    lambda_c=2;
    

    disp('************* Main Problem ***************')
    
    Wo=dlyap(A', C'*C);
    Wc=dlyap(A,  B*B');
    
    S_AA=[A,  B*C;
        zeros(nk,nk),A ];
    S_AB=[ zeros(nk,nk); eye(nk)/gamma_a];
    S_AC=[ eye(nk),zeros(nk,nk)];
    S_AD=[ zeros(nk,nk)];
    IB=[  eye(nk)/gamma_eta];
    IC=[ eye(nk) ];
    S_AD=[ zeros(nk,nk)];
    
    setlmis([])
    
    % DECISION VARIABLES
    %  
    X=lmivar(1,[2*nk 1]);
    Y=lmivar(1,[nk 1]);
    P=lmivar(1,[nk,1]);
    Q=lmivar(1,[nk,1]); 
    
    % DEFINE LMIs
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % 1st LMI:
    % rhs [P  I; I  Q]>0
    lmiterm([-1 1 1 P],1,1)     %
    lmiterm([-1 2 1 0],1) % I
    lmiterm([-1 2 2 Q],1,1)     %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % 2nd LMI:  M1' XQ M1 < XQ
    lmiterm([2 1 1 X],S_AA',S_AA)     % S_AA' X S_AA
    lmiterm([2 1 1 Q],S_AC',S_AC)     % S_AC' X S_AC
    lmiterm([2 2 1 X],S_AB',S_AA)     % S_AB' X S_AA
    lmiterm([2 2 2 X],S_AB',S_AB)     % S_AB' X S_AB
    % rhs
    lmiterm([-2 1 1 X],1,1)     %  X
    lmiterm([-2 2 2 Q],1,1)     %  Q
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % 3rd LMI:  A1' YQ A1 < YQ
    lmiterm([3 1 1 Y],A',A)       % A' Y A
    lmiterm([3 1 1 Q],IC',IC)     % Q
    lmiterm([3 2 1 Y],IB',A)      % Y A
    lmiterm([3 2 2 Y],IB',IB)     % Y
    % rhs
    lmiterm([-3 1 1 Y],1,1)     %  Y
    lmiterm([-3 2 2 Q],1,1)     %  Q
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % 4-5thLMI: 0<X 0<Y
    % rhs
    lmiterm([-4 1 1 X],1,1)     %  X
    lmiterm([-5 1 1 Y],1,1)     %  Y 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    LMISYS3 = getlmis;
    
    n = decnbr(LMISYS3);
    c = zeros(n,1);
    for j=1:n,
        [Xj,Yj,Pj,Qj] = defcx(LMISYS3,j,X,Y,P,Q);
        c(j) = trace(Pj*Wo*lambda_b) + trace(Qj*Wc*lambda_c);
    end
    options=zeros(1,5);
    options(1)=1e-13;
    options(2)=1e6;
    options(3)=-1;
    [etaopt,popt] = mincx(LMISYS3,c,options);
    
    Xopt=dec2mat(LMISYS3,popt,X);
    Yopt=dec2mat(LMISYS3,popt,Y);
    Popt=dec2mat(LMISYS3,popt,P);
    Qopt=dec2mat(LMISYS3,popt,Q);
    
    
    % checks
    
    %XQf=[Xopt,zeros(2*nk,nk);zeros(nk,2*nk),Qopt];
    %M=[G.a, G.b*G.c, zeros(nk,nk); zeros(nk,nk),G.a,eye(nk)/gamma_a; eye(nk),zeros(nk,2*nk)];
    %eig(M'*XQf*M - XQf)
    %PP=[P2opt,eye(nk);eye(nk),P3opt]
    %eig(PP)
    %Popt*Qopt
    %Popt-inv(Qopt)
    %trace(Popt*Wo) + trace(Qopt*Wc)
    %etaopt-etamin
    
    T_opt=sqrtm(Popt);% optimal realization
    
    % analysis
    disp('*********************************')
    disp('Optimal LMI')
    % display sensitivities
    dispsensitivities(inv(T_opt)*A*T_opt,inv(T_opt)*B,C*T_opt, 'Multi-objective');
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
