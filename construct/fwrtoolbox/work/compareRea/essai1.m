[num,den]=butter(4,0.05);
H=tf(num,den,1);

R1 = DFIq2FWR(H);
R2 = SS2FWR( canon(ss(H),'companion') );
R3 = SS2FWR( balreal(ss(H)) );
R4 = rhoDFIIt2FWR( H, [0.4 0.5 0.6 0.7], 1, 0.06*ones(1,4), 1);

[R1q, DZ1 ] = quantizedFWR( R1, 16,16,10,16,32,0);
[R2q, DZ2 ] = quantizedFWR( R2, 16,16,10,16,32,0);
[R3q, DZ3 ] = quantizedFWR( R3, 16,16,10,16,32,0);
[R4q, DZ4 ] = quantizedFWR( R4, 16,16,10,16,32,0);



[M1 MZ1] = MsensH(R1);
[M2 MZ2] = MsensH(R2);
[M3 MZ3] = MsensH(R3);
[M4 MZ4] = MsensH(R4);


% norm(H-tf(R1q))
% norm( MZ1.*DZ1, 'fro')
% norm(H-tf(R2q))
% norm( MZ2.*DZ2, 'fro')
% norm(H-tf(R3q))
% norm( MZ3.*DZ3, 'fro')
% norm(H-tf(R4q))
% norm( MZ4.*DZ4, 'fro')


S=zeros(4,16);
for i=5:16
    try
        S(2,i) = implementationArea(R2, i,i,10,i,2*i,0);
        [R2q, DZ2 ] = quantizedFWR( R2, i,i,10,i,2*i,0);
        Dist(2,i) = norm(H-tf(R2q));
    catch
    end
    
    try
        S(1,i) = implementationArea(R1, i,i,10,i,2*i,0);
        [R1q, DZ1 ] = quantizedFWR( R1, i,i,10,i,2*i,0);
        Dist(1,i) = norm(H-tf(R1q));
    catch
    end

    try
        S(3,i) = implementationArea(R3, i,i,10,i,2*i,0);
        [R3q, DZ3 ] = quantizedFWR( R3, i,i,10,i,2*i,0);
        Dist(3,i) = norm(H-tf(R3q));
    catch
    end
    
    try
        S(4,i) = implementationArea(R4, i,i,10,i,2*i,0);
        
        [R4q, DZ4 ] = quantizedFWR( R4, i,i,10,i,2*i,0);
        Dist(4,i) = norm(H-tf(R4q));
        catch    
    end
end


plot(S(1,:),Dist(1,:),'b*');
hold on;
plot(S(2,:),Dist(2,:),'g*')
plot(S(3,:),Dist(3,:),'r*');
plot(S(4,:),Dist(4,:),'y*');
