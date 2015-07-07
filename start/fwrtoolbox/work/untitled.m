N=100;
R=zeros(N,1);
L1=R;
L2=R;

i=1;
for i=linspace(amin,amax)
    H=tf(1,[1 a],-1,'Variable','z^-1');
    [Yimp Timp] = impulse(H,1e5); 
    L1(i) = sum(abs(Yimp));
    L2(i) = sqrt(sum(Yimp.^2));
    i=i+1;
end

plot( linspace(amin,amax),L1);
figure
plot( linspace(amin,amax),L2);
figure
plot( linspace(amin,amax), L1./L2);