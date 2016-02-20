% tf
den = [ 1 -5.6526064 13.3817570 -16.9792460 12.1764710 -4.6789191 0.7525573 ];
num = [ 0.0047079 -0.0251014 0.0584417 -0.0760820 0.0584417 -0.0251014 0.0047079 ];
H=tf(num,den,1);


% parameters
Delta=0.25;
NbB = 11;
%fp = 'fixed';
%block = 'natural';

% Forme directe II
[A,B,C,D] = tf2ss(num,den);
R2 = SS2FWR(A,B,C,D);
R2=setFPIS(R2,'DSP16',10);
implementMATLAB(R2,'FDII');

% Forme équilibrée
Sq=balreal( ss(A,B,C,D,1) );
R3 = SS2FWR(Sq);
R3=setFPIS(R3,'DSP16',10);
implementMATLAB(R3,'balanced');

% Forme directe II en delta
[numd,dend] = z2del(num,den,Delta);
[Ad,Bd,Cd,Dd] = tf2ss(numd,dend);
R4 = SSdelta2FWR(Ad,Bd,Cd,Dd,Delta);
R4=setFPIS(R4,'DSP16',10);
implementMATLAB(R4,'FDIIdelta');
