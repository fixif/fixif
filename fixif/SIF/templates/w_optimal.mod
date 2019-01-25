#---
#--- Modele optimisation des largeurs: arith-26
#--- Auteur: Hacene Ouzia, Sorbonne Universite (01-2019) 
#---

#---
#--- DIMENSIONS 
param p integer > 0;    #-- nbr de contraintes (p)
param np integer > 0;   #-- nbr de variables (n+p)

#---
#--- ENSEMBLES 
set I := 1 .. p;        #-- Indices contraintes
set J := 1 .. np;       #-- Indices variables

#---
#--- PARAMETRES 
param u{J} integer > 0;     #-- Valeur max var w
param l{J} integer default 2; 

param E{I,J};                #-- Coefficients des contraintes ....
param eps{I};                #-- Second membre ...

param wtilde{J} integer > 0;
   #--
   #-- Il faut que 3 <= wtilde(j) < u(j), pr tt j ...
   check{j in J}:
      l[j] <  wtilde[j] and wtilde[j] < u[j];


param bsup{j in J} integer default u[j] - wtilde[j] + 1;    #-- val max de w_j - wtilde_j
param binf{j in J} integer default l[j] - wtilde[j] + 1;       #-- val min de w_j - wtilde_j


#---
#--- VARIABLES 
var w{j in J} integer >= l[j], <= u[j];  #-- word-length
var delta{J} binary;                   #-- delta


#--- 
#--- OBJECTIF 
minimize Lenght:     #-- Somme des largeurs ...
   sum{j in J} w[j]; 


#---
#--- CONTRAINTES 
subject to outerr{i in I}:        # output error
   sum{j in J} E[i,j]*2**(-w[j] + delta[j]) <= eps[i];

subject to dela{j in J}:
   w[j] - wtilde[j] + 1 <= (1 - delta[j])*bsup[j];

subject to delb{j in J}:
   w[j] - wtilde[j] >= (binf[j] - 1)*delta[j];

#---
#--- FIN Modele ...  
