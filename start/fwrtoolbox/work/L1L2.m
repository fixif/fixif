close all
N=10;
NbU=1e8;
R=zeros(N,1);
L1=R;
L2=R;

amin=1e-3;
amax=1-1e-3;

i=1;
u=rand(NbU,1)*2-1;


for a=linspace(amin,amax,N)
    H=tf(1,[1 a],-1,'Variable','z^-1');
    [Yimp Timp] = impulse(H,1e5);
    L1(i) = sum(abs(Yimp));
    L2(i) = sqrt(sum(Yimp.^2));
    
    
    y = filter(H.num{1},H.den{1},u);
    figure;
    hist(y,1000);
    legend(['a=' num2str(a)]);
    hold on;
    plot([L1(i) L1(i)],[0,200])
    plot([-L1(i) -L1(i)],[0,200])
    
    i=i+1;
end

% figure
% plot( linspace(amin,amax,N),L1);
% figure
% plot( linspace(amin,amax,N),L2);
% figure
% plot( linspace(amin,amax,N), L2./L1);