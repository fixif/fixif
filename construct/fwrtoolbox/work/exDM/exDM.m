%##########################################################################
%
%   ConceptionFiltre.m :
%
%   Fichier de calcul des coefficients du filtre
%
%   Entrées :
%
%   Sortie :  %       - NumCas (4*3) : Numérateurs des filtres cascadés
%       - DenCas (4*3) : Dénominateurs des filtres cascadés
%       - Num (1*9) : Numérateur du filtre non-cascadé
%       - Den (1*9) : Dénominateur du filtre non-cascadé
%
%   Fonction :
%       - Calcul des coefficients du filtre
%       - Calcul des coefficients du filtre cascadé
%
%##########################################################################

   Fe = 12000;                  % Frequence d'echantillonnage

   % Spécification du filtre 
     Fp1 = 1200;                 % Fréquence basse de la bande passante
   Fp2 = 2400;                 % Fréquence haute de la bande passante
   Fs1 = 1080;                 % Fréquence basse de la bande atténuée
   Fs2 = 2520;                 % Fréquence haute de la bande atténuée
      Wp = [2*Fp1/Fe 2*Fp2/Fe];   % Fréquences hautes et basses de la bande passante
   Ws = [2*Fs1/Fe 2*Fs2/Fe];   % Fréquences hautes et basses de la bande atténuée
   Rp = 3;                     % Atténuation dans la bande passante
   Rs = 30;                    % Atténuation dans la bande atténuée
        % Calcul de l'ordre du filtre
     [Nf, Wn] = buttord(Wp, Ws, Rp, Rs);      % Butterworth
    disp(strcat(sprintf('\n Ordre du filtre - Butterworth : '), num2str(2 * Nf) ));

   [Nf, Wn] = Cheb1ord(Wp, Ws, Rp, Rs);     % Chebyshev type I
    disp(strcat(sprintf('\n Ordre du filtre - Chebyshev type I : '), num2str(2 * Nf) ));       
	[Nf, Wn] = Cheb2ord(Wp, Ws, Rp, Rs);    % Chebyshev type II
    disp(strcat(sprintf('\n Ordre du filtre - Chebyshev type II : '), num2str(2 * Nf) ));       
	[Nf, Wn] = ellipord(Wp, Ws, Rp, Rs);    % Elliptique
    disp(strcat(sprintf('\n Ordre du filtre - Elliptique : '), num2str(2 * Nf) ));  
      % Calcul des coefficients du filtre - choisir le filtre d'ordre
   % minimal      
   [Num,Den] = ellip(Nf, Rp, Rs, Wn);
     % Calcul des coefficients du filtre cascadé
   