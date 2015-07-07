function  [gamma_a,gamma_eta]=dispsensitivities(A,B,C, dispstr)
% display input/output sensitivities and stability radius for 
% FWL filter realization (A,B,C)
%
% gamma_a is H-infinity norm of dS/dA sensitivity matrix
% gamma_eta is the stability radius measure
%
% JFW 7/6/11

nk=size(A,2); % state dimansion

disp('================================================')
disp(['input/output sensitivities - ',dispstr])
disp('')

% get sensitivity matrices  
% sensitivity dG/dA
SAA=[A,        B*C;
    zeros(nk,nk),A]; % 
SA=ss(SAA,[zeros(nk,nk);eye(nk)],[eye(nk),zeros(nk,nk)],0,-1);% put into state space discrete time form
gamma_a=norm(SA,'inf');
disp(['||S_A||_infty:         ',num2str(gamma_a)])
disp(['||S_A||_2:             ',num2str(norm(SA))])
 
% sensitivity dG/dB
SB=ss(A, eye(nk) ,C,0,-1);% put into state space discrete time form
disp(['||S_A||_2:             ',num2str(norm(SB))])

% sensitivity dG/dC
SC=ss(A, B, eye(nk),0,-1);% put into state space discrete time form
disp(['||S_A||_2:             ',num2str(norm(SC))])
 
% stability radius
eta=ss(A, eye(nk), eye(nk),0,-1);% put into state space discrete time form
gamma_eta=norm(eta,'inf');
disp(['|| inv(zI-A) ||_infty: ',num2str(gamma_eta)])
 
disp('================================================')

end

