% definition of constant 
m_var_23_h = 0.000768;
m_var_25_h = 0.000338;
m_var_27_h = 0;
m_var_29_h = 0.000261;
m_var_31_h = 0.000467;
% end of definition of constant 
nombreSource = 1 ;
nombreSortie = 6 ;
nombreNoeudInter = 0 ;
nombreNoeud = 7 ;
TabNumeroSortie= [ 2 3 4 5 6 7 ];
TabNumeroEntree= [ 1 ];
TabNumeroInter = [ ];

%-----  Ajout des dynamics des entrees -----------
load('sample_fir31_andrei.mat');
Noeud(1).DynOver = input;
Noeud(1).Dyn = [ -5.7881, 5.7799 ];

%-----  Ajout des Probabilités de débordement des noeuds  -----------
Noeud(1).Deb = -1;
Noeud(2).Deb = -1;
Noeud(3).Deb = 1e-05;
Noeud(4).Deb = 1e-05;
Noeud(5).Deb = 1e-05;
Noeud(6).Deb = 1e-05;
Noeud(7).Deb = 1e-05;

%-----  Definition des listSucc de chaque Noeud -----------
Noeud(1).Suc= [ 2 3 4 5 6 7 ];

%-----  Definition  des fonctions de transfert partielles -----------
H(6).Blocks = [0 0; ];
H(6).Num = [ 1.*m_var_31_h 1.*m_var_29_h 1.*m_var_27_h 1.*m_var_25_h 1.*m_var_23_h ];
H(6).Den = [ 1 ];
H(6).tf  = tf(H(6).Num, H(6).Den, 1, 'variable', 'z^-1');

H(5).Blocks = [0 0; ];
H(5).Num = [ 1.*m_var_31_h 1.*m_var_29_h 1.*m_var_27_h 1.*m_var_25_h 1.*m_var_23_h ];
H(5).Den = [ 1 ];
H(5).tf  = tf(H(5).Num, H(5).Den, 1, 'variable', 'z^-1');

H(4).Blocks = [0 0; ];
H(4).Num = [ 0 1.*m_var_29_h 1.*m_var_27_h 1.*m_var_25_h 1.*m_var_23_h ];
H(4).Den = [ 1 ];
H(4).tf  = tf(H(4).Num, H(4).Den, 1, 'variable', 'z^-1');

H(3).Blocks = [0 0; ];
H(3).Num = [ 0 0 1.*m_var_27_h 1.*m_var_25_h 1.*m_var_23_h ];
H(3).Den = [ 1 ];
H(3).tf  = tf(H(3).Num, H(3).Den, 1, 'variable', 'z^-1');

H(2).Blocks = [0 0; ];
H(2).Num = [ 0 0 0 1.*m_var_25_h 1.*m_var_23_h ];
H(2).Den = [ 1 ];
H(2).tf  = tf(H(2).Num, H(2).Den, 1, 'variable', 'z^-1');

H(1).Blocks = [0 0; ];
H(1).Num = [ 0 0 0 0 1.*m_var_23_h ];
H(1).Den = [ 1 ];
H(1).tf  = tf(H(1).Num, H(1).Den, 1, 'variable', 'z^-1');

%-----  Definition  des fonctions de transfert globales -----------
Hg(1,2).tf = H(6).tf;
Hg(1,3).tf = H(5).tf;
Hg(1,4).tf = H(4).tf;
Hg(1,5).tf = H(3).tf;
Hg(1,6).tf = H(2).tf;
Hg(1,7).tf = H(1).tf;
%**********fin **********

