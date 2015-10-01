#------
# Exponetial Nonlinear Knapsack problem 
#    . Version for several constraints 
#------------------------------------------

option solver bonmin; 

param N;  # Nbr wx variables  
param M;  # Nbr wy variables
param Q;  # Nbr of constraints  

param Ux; # Upper bound on Wx 
param Uy; # Upper bound on Wy

set Colx := 1 .. N; # Wx variable indices  
set Coly := 1 .. M; # Wy variable indices
set Rows := 1 .. Q; # Constraints indices 

param c{Colx}; 
param d{Coly};

param coefx{Rows, Colx}; 
param coefy{Rows, Coly}; 

var Wx{Colx} >=0, integer;
var Wy{Coly} >=0, integer;

minimize Obj : 
   sum{j in Colx} c[j]*Wx[j] + sum{j in Coly} d[j]*Wy[j]; 
   
subject to Const{i in Rows}:
    sum{j in Colx} coefx[i,j]*2**(-Wx[j]) + sum{j in Coly} coefy[i,j]*2**(-Wy[j]) <= 1; 
