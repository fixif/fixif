%GEVERSMODEL2
% model 3.2 for Gevers and Li filter in Chapter 3.8
% also [Williamson 1986]
%
% JFW 7/6/11

function [G]=geversmodel2

% These are the matrices given in Gevers & Li.
% The matrix is so poorly condistioned that this matrix is unstable
% Ag=[ 5.6526 , -13.3818 , 16.9792 , -12.1765 , 4.6789 , -0.7526;
%           1 ,        0 ,        0 ,        0 ,      0 ,       0;
%           0 ,        1 ,        0 ,        0 ,      0 ,       0;
%           0 ,        0 ,        1 ,        0 ,      0 ,       0;
%           0 ,        0 ,        0 ,        1 ,      0 ,       0;
%           0 ,        0 ,        0 ,        0 ,      1 ,       0]; 
% Bg=[      1 ,        0 ,        0 ,        0 ,      0 ,       0]';
% Cg=[ 0.1511 , -0.45581 ,   0.3855 ,   0.1160 , -0.3074,  0.1165]*1e-2;
% Dg=0.4708e-2;
% 
% G=ss(Ag,Bg,Cg,Dg,1);

% This is the filter given in Williamson (1986)
 q0 = 0.0047079;
 q1 = -0.0251014;
 q2 = 0.0584417;
 q3 = -0.0760820;
 q4 = 0.0584417; 
 q5 = -0.0251014;
 q6 = 0.0047079;

 p0 = 1
 p1 = -5.6526064;
 p2 = 13.3817570;
 p3 = -16.9792460;
 p4 = 12.1764710;
 p5 = -4.6789191;
 p6 = 0.7525573;
 Gw=tf([q0,q1,q2,q3,q4,q5,q6],[p0,p1,p2,p3,p4,p5,p6],1);
 G=ss(Gw);
 
return
