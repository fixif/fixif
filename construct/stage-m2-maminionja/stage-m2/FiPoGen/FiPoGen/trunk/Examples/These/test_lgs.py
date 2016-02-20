# -*- coding: utf-8 -*-
'''
Created on 8 oct. 2011

On Sept. 23th 2014, the code works, for real !

@author: Benoit Lopez
'''

from ex_gen import *
import numpy as np
import scipy as sp
import random as rd
from numpy import linalg as la
from numpy.linalg import inv  #Calcule l'inverse d'une matrice
from math import sqrt #Racine carrée
from scipy import signal
from scipy.io import savemat, loadmat
np.set_printoptions(suppress = True)


def PhiKLD(A,B,C,d):
    """Retourne (Phi,K,L,D) à partir de (A,B,C,D)
    en appliquant directement la formule"""
    I=np.eye(A.shape[0]) #matrice identité de même taille que A
    IAinv = inv(A+I)
    Phi=IAinv*(A-I)
    K=sqrt(2)*IAinv*B
    L=sqrt(2)*C*IAinv
    D = d - C*IAinv*B
    return (Phi,K,L,D)


def PhiKLD_in(alpha,(Phi,K,L,D)):
    """Construit Phi_in et K_in à partir des alphas en utilisant la formule
    et L_in en utilisant la transformation pour passer de (Phi,K,L,D)
    à (Phi_in,K_in,L_in,D)"""
    n=Phi.shape[0]
    I=np.eye(n)
    #On construit la matrice Phi_in
    Phi_in=np.zeros([n,n])
    for i in range(1,n-1):
        Phi_in[i][i+1] = alpha[i]
        Phi_in[i][i-1] = -alpha[i-1]
    Phi_in[0][1] = alpha[0]
    Phi_in[n-1][n-2] = -alpha[n-2]
    Phi_in[n-1][n-1] = -alpha[n-1]
    Phi_in = np.matrix(Phi_in)

    #Le vecteur K_in
    K_in = np.zeros([n,1])
    K_in[n-1] = sqrt(2*alpha[n-1])
    K_in = np.matrix(K_in)
    (uu,V_in)=la.eig(Phi_in)
    S=[]
    for i in range(0,n):
        c=complex(rd.uniform(0.,1.),rd.uniform(0.,1.))
        while (c in S) or (c in uu):
            c=complex(rd.uniform(0.,1.),rd.uniform(0.,1.))
        S.append(c)
        if i ==0:
            B = np.matrix(inv(c*I-Phi_in)*K_in)
            A = np.matrix(L*inv(c*I-Phi)*K)
        else:
            b = np.matrix(inv(c*I-Phi_in)*K_in)
            B = np.c_[B,b]
            a = np.matrix(L*inv(c*I-Phi)*K)
            A = np.c_[A,a]
    LL = A*inv(B)
    L_in = []
    for i in range(LL.size):
        L_in.append(LL.item(i).real)
    L_in = np.matrix(L_in)
    return (Phi_in,K_in,L_in,D)
    
    
def ABCd_in(Phi,K,L,D):
    """On applique la bonne formule pour passer de (Phi_in,K_in,L_in,D)
    à (A_in,B_in,C_in,d)"""
    I=np.eye(Phi.shape[0])
    A = (I+Phi)*inv(I-Phi)
    B=sqrt(2)/2*(I+A)*K
    C=sqrt(2)/2*L*(I+A)
    d = D + C*inv(I+A)*B
    return (A,B,C,d)


def ABCd_star(A,B,C,d,Phi,K):
    I=np.eye(Phi.shape[0])
    As = np.transpose(A)
    Bs = np.transpose(inv(I-Phi))*np.transpose(C)
    Cs = sqrt(2)*np.transpose(K)
    return (As,Bs,Cs,d)


def A_decomposition_LGS(alpha,Phi_in):
    """Retourne la décomposition de A_in en produit de
    1+3*(n-1) matrices"""
    n = Phi_in.shape[0]
    Ad=[]
    #On calcule d'abord tous les beta_i et gamma_i
    beta=[-alpha[0]]
    gamma=[1/(1+alpha[0]**2)]
    for i in range(1,n-1):
        beta.append(-alpha[i]/(1-alpha[i-1]*beta[i-1]))
        if (i<n-2):
            gamma.append(1/(1-alpha[i]*beta[i]))
    beta.append(-alpha[n-1]/(1+alpha[n-1]-alpha[n-2]*beta[n-2]))
    gamma.append(1/(1+alpha[n-1]-alpha[n-2]*beta[n-2]))
    #Puis on ajoute dans la liste de la décomposition les matrices U selon la formule.
    for i in range(0,n-1):
        Ad.append(U(i+1,i,-alpha[i],n))
        Ad.append(U(i+1,i+1,gamma[i],n))
    for i in range(0,n-1):
        Ad.append(U(n-2-i,n-1-i,-beta[n-2-i],n))
    #A la fin on rajoute  la matrice (I+Phi_in)
    Ad.append(np.eye(n)+Phi_in)
    return Ad


def A_decomposition_LCW(alpha,Phi_in):
    """Retourne la décomposition de A_in en produit de
    3*(n-1) matrices"""
    n = Phi_in.shape[0]
    Ad=[]
    #On calcule d'abord tous les beta_i et gamma_i
    beta=[-alpha[0]]
    gamma=[1/(1+alpha[0]**2)]
    for i in range(1,n-1):
        beta.append(-alpha[i]/(1-alpha[i-1]*beta[i-1]))
        if (i<n-2):
            gamma.append(1/(1-alpha[i]*beta[i]))
    beta.append(-alpha[n-1]/(1+alpha[n-1]-alpha[n-2]*beta[n-2]))
    gamma.append(1/(1+alpha[n-1]-alpha[n-2]*beta[n-2]))
    #Puis on ajoute dans la liste de la décomposition les matrices U selon la formule.
    for i in range(0,n-1):
        Ad.append(U(i+1,i,alpha[i],n))
        Ad.append(U(i+1,i+1,gamma[i],n))
    for i in range(0,n-1):
        Ad.append(U(n-2-i,n-1-i,beta[n-2-i],n))
    return Ad


def Matrice_Z_LGS(Ad,(A_in,B_in,C_in,d)):
    """A partir de la décomposition de A_in et des matrices B_in,C_in,D,
    construit les éléments (J,K,L,M,N,P,Q,R,S) qui forment Z."""
    n=Ad[0].shape[0]
    nn=len(Ad)
    I=np.matrix(np.eye(n))
    Ze=np.matrix(np.zeros([n,n]))
    J=[]
    C=[] # va stocker la colonne courante de J dans la boucle
    #la boucle suivante construit les colones N x n de la matrice J et les concatène.
    for i in range(1,nn+1):
        if i ==1 :
            C = np.r_[I,-Ad[i]]
            while len(C) < n*nn:
                C = np.r_[C,Ze]
            J=C
        else:
            C = Ze
            while len(C) < n*(i-1):
                C = np.r_[C,Ze]
            C = np.r_[C,I]
            if i != nn:
                C = np.r_[C,-Ad[i]]
            while len(C) < n*nn:
                C = np.r_[C,Ze]
            J = np.c_[J,C]
    J=np.matrix(J)
    K=Ze
    for i in range(0,nn-2):
        K = np.c_[K,Ze]
    K = np.c_[K,I]
    L = np.matrix( np.zeros( [1,n*nn] ))
    N = np.matrix(np.zeros([n*nn,1]))
    M = Ad[0]
    for i in range(0,nn-1):
        M = np.r_[M,Ze]
    P = Ze
    Q = B_in
    R = C_in
    S = d
    Z = np.r_[np.c_[-J,M,N], np.c_[K,P,Q], np.c_[L,R,S]]

    return Z,J,K,L,M,N,P,Q,R,S


def Matrice_Z_LCW(Ad,(As,Bs,Cs,d)):
    """A partir de la décomposition de A_in et des matrices B_in,C_in,D,
    construit les éléments (J,K,L,M,N,P,Q,R,S) qui forment Z."""
    n=Ad[0].shape[0]
    nn=len(Ad)
    I=np.matrix(np.eye(n))
    Ze=np.matrix(np.zeros([n,n]))
    J=[]
    C=[]
    #la boucle suivante construit les colones N x n de la matrice J et les concatène.
    for i in range(1,nn+1):
        if i ==1 :
            C = np.r_[I,-Ad[i]]
            while len(C) < n*nn:
                C = np.r_[C,Ze]
            J=C
        else:
            C = Ze
            while len(C) < n*(i-1):
                C = np.r_[C,Ze]
            C = np.r_[C,I]
            if i != nn:
                C = np.r_[C,-Ad[i]]
            while len(C) < n*nn:
                C = np.r_[C,Ze]
            J = np.c_[J,C]
    J=np.matrix(J)
    K=Ze
    for i in range(0,nn-2):
        K = np.c_[K,Ze]
    K = np.c_[K,I]
    L = np.matrix( np.zeros( [1,n*nn] ))
    N = np.matrix(np.zeros([n*nn,1]))
    M = 2 * Ad[0]
    for i in range(0,nn-1):
        M = np.r_[M,Ze]
    P = -I
    Q = Bs
    R = Cs
    S = d
    Z = np.r_[np.c_[-J,M,N], np.c_[K,P,Q], np.c_[L,R,S]]
    return Z,(J,K,L,M,N,P,Q,R,S)


def U(i,j,x,n):
    """Construit la matrice U(i,j,x) de taille n telle que
    U est la matric identité et
    le j-ème élément de la i-ème ligne vaut x."""
    U=np.eye(n)
    U[i][j]=x
    U=np.matrix(U)
    return U


def JSS_trans(D):
    """Calcul la décomposition en fraction continue"""
    n = len(D)
    Ol = []
    El = []
    for i in range(0,n):
        if i%2 ==0:
            Ol.append(D[i])
            El.append(0.0)
        else:
            El.append(D[i])
            Ol.append(0.0)
    O=np.poly1d(Ol) #Polynôme des monômes pair
    E=np.poly1d(El) #Polynôme des monômes impair
    r=[]
    j=len(D)
    while j>1:
        if len(O)>len(E):
            LMo=[]
            Ro=[]
            for i in range(0,len(O)+1):
                if i<len(O):
                    Ro.append(O[i])
                    LMo.append(0.0)
                else:
                    LMo.append(O[i])
            LMo.reverse()
            LMo = np.poly1d(LMo)
            Ro.reverse()
            Ro = np.poly1d(Ro)
            (Q,R) = np.polydiv(LMo,E)
            r.append(Q[1])
            O=Ro+R
        else:
            LMe=[]
            Re=[]
            for i in range(0,len(E)+1):
                if i<len(E):
                    Re.append(E[i])
                    LMe.append(0.0)
                else:
                    LMe.append(E[i])
            LMe.reverse()
            LMe = np.poly1d(LMe)
            Re.reverse()
            Re = np.poly1d(Re)
            (Q,R) = np.polydiv(LMe,O)
            r.append(Q[1])
            E=Re+R
        j-=1
    r.reverse()
    #On trouve les alpha à partir des r en utilisant la formule
    alpha=[]
    for i in range(0,len(r)-1):
       alpha.append(sqrt(1.0/(r[i]*r[i+1])))
    alpha.append(1.0/(r[-1]))
    #On retourne les alpha qui serviront à construire Phi_in et K_in
    return alpha


def LGS(b,a=None):
    """Retourne la forme SIF de la structure LGS correspondant au filtre donné"""
    if a == None :
       A,B,C,d=b["A"],b["B"],b["C"],b["D"]
    else :
        #Par la fonction de scipy.signal on obtient le state-space associé
        (A,B,C,d)=signal.tf2ss(b,a)
    A = np.matrix(A) ; B = np.matrix(B) ; C = np.matrix(C); d = np.matrix(d)
    #On calcule ensuite (Phi,K,L,D) qu'on reconverti en fonction de transfert
    (Phi,K,L,D)=PhiKLD(A,B,C,d)
    num,den=signal.ss2tf(Phi,K,L,D)
    #On calcule les alpha par la JSS-transformation
    alpha=JSS_trans(den)
    #On calcule les PhiKLD_in
    (Phi_in,K_in,L_in,D)=PhiKLD_in(alpha,(Phi,K,L,D))
    #On peut calculer les (A,B,C,d)_in et la
    #décomposition de A_in en produit de matrice.
    (A_in,B_in,C_in,d)=ABCd_in(Phi_in,K_in,L_in,D)
    #print signal.ss2tf(A_in,B_in,C_in,d)
    Ad = A_decomposition_LGS(alpha,Phi_in)
    for Mat in Ad:
        print M2tex(Mat)
    #On construit les matrices qui forment Z
    Z,J,K,L,M,N,P,Q,R,S= Matrice_Z_LGS(Ad,(A_in,B_in,C_in,d))
    return Z,J,K,L,M,N,P,Q,R,S


def LCW(b,a):
    """Retourne la forme SIF de la structure LCW correspondant au filtre donné"""
    #Par la fonction de scipy.signal on obtient le state-space associé
    (A,B,C,d)=signal.tf2ss(b,a)
    print A.shape
    A = np.matrix(A) ; B = np.matrix(B) ; C = np.matrix(C); d = np.matrix(d)
    #On calcule ensuite (Phi,K,L,D) qu'on reconverti en fonction de transfert
    (Phi,K,L,D)=PhiKLD(A,B,C,d)
    num,den=signal.ss2tf(Phi,K,L,D)
    #On calcule les alpha par la JSS-transformation
    alpha=JSS_trans(den)
    #On calcule les PhiKLD_in
    (Phi_in,K_in,L_in,D)=PhiKLD_in(alpha,(Phi,K,L,D))
    #On peut calculer les (A,B,C,d)_in et la
    #décomposition de A_in en produit de matrice.
    (A_ib,B_ib,C_ib,d)=ABCd_in(Phi_in,K_in,L_in,D)
    (As,Bs,Cs,d) = ABCd_star(A_ib,B_ib,C_ib,d,Phi_in,K_in)
    Ad = A_decomposition_LCW(alpha,Phi_in)
    #On construit les matrices qui forment Z
    Z,Z_tuple= Matrice_Z_LCW(Ad,(As,Bs,Cs,d))
    return Z,Z_tuple
    


'''
Script de test
'''
#On génère un filtre et on obtient ses coeffs
#b,a=signal.iirfilter(5, [0.4, 0.6], rp=0.1, rs=0.01, output='ba')
D_abcd=loadmat("ex_bis/ABCD.mat")
Z,J,K,L,M,N,P,Q,R,S = LGS(D_abcd)
#ZZ,ZZ_tuple=LCW(b,a)
#savemat('ex_bis/Z=LGS.mat',{'Z':Z,'J':J,'K':K,'L':L,'M':M,'N':N,'P':P,'Q':Q,'R':R,'S':S})

