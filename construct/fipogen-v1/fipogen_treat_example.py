# -*- coding: utf-8 -*-

import tkFileDialog
from Tkinter import *
from pickle import dump

from PIL import Image, ImageTk
from os import listdir

from Functions.matlab_files_reader import MatlabDict2FilterExample_SIF
from Functions.optimization import *
from fipogen.FxP import best_oSoP_gen_from_dict


# /!\ ATTENTION /!\
# Version compatible SISO uniquement !

def erreur_finale(eps, wcpgHe, dcgHe):
	delta_y=[0,0]
	for i in range(len(eps)):
		moy=(eps[i][1]+eps[i][0])/2
		ray=(eps[i][1]-eps[i][0])/2
		delta_y[0] += -dcgHe[i]*moy - wcpgHe[i]*ray
		delta_y[1] += -dcgHe[i]*moy + wcpgHe[i]*ray
	return delta_y

def Int(s):
	if s.isdigit() or (s[1:].isdigit() and (s[0]=="+" or s[0]=="-")):
		return int(s)
	else:
		return None

def get_io_from_mat(fichier):
	# Chargement du fichier
	D = loadmat(fichier)

	# On stocke les éléments du dictionnaire dans des variables
	global u_m, u_r, dcu, wcpgu, y_m, y_r
	u_m = D["um"][0][0]
	u_r = D["ur"][0][0]
	dcu = [D["dcHu"][i][0] for i in range(len(D["dcHu"]))]
	wcpgu = D["wcpgHu"][0]

	# Rappel : on est en SISO
	y_m = u_m * dcu[-1]
	y_r = u_r * wcpgu[-1]
	return u_m, u_r, y_m, y_r, dcu, wcpgu

def ChangeIO():
	y_m = float(str_um.get()) * dcu[-1]
	y_r = float(str_ur.get()) * wcpgu[-1]
	str_y.set("⟨ y_m , y_r ⟩ = ⟨ %lf , %lf ⟩"%(y_m,y_r))

def ValiderIO():
	pass

def Browser():
	global filemat
	filemat = tkFileDialog.askopenfilename(initialdir="Examples/These/ex_bis", title='Please select a Matlab file', filetypes=[("Matlab","*.mat")])
	lbl_browser.config(text=filemat.split("/")[-1])
	lbl_browser.pack(side=LEFT)

	frame_modif_io = Frame(l, padx=5, pady=5)
	frame_modif_io.pack(side=TOP, fill=X)

	frame_modif_io_1 = Frame(frame_modif_io)
	frame_modif_io_1.pack(side=TOP, fill=X)

	frame_modif_io_2 = Frame(frame_modif_io)
	frame_modif_io_2.pack(side=TOP, fill=X)

	u_m, u_r, y_m, y_r, dcu, wcpgu = get_io_from_mat(filemat)
	Label(frame_modif_io_1,text="⟨ u_m , u_r ⟩ = ⟨").pack(side=LEFT)
	# entree_um
	global str_um
	str_um = StringVar() 
	str_um.set(str(u_m))
	entree_um = Entry(frame_modif_io_1, textvariable=str_um, width=4)
	entree_um.pack(side=LEFT)
	Label(frame_modif_io_1,text=",").pack(side=LEFT)
	# entree_ur
	global str_ur
	str_ur = StringVar()
	str_ur.set(str(u_r)) 
	entree_ur = Entry(frame_modif_io_1, textvariable=str_ur, width=4)
	entree_ur.pack(side=LEFT)
	Label(frame_modif_io_1,text="⟩").pack(side=LEFT)

	button_change_io= Button(frame_modif_io_1, text ='Changer', command = ChangeIO)
	button_change_io.pack(side=RIGHT)

	global str_y
	str_y=StringVar()
	str_y.set("⟨ y_m , y_r ⟩ = ⟨ %lf , %lf ⟩"%(y_m,y_r))
	Label(frame_modif_io_2,textvariable=str_y).pack(side=LEFT)
	button_validate_io= Button(frame_modif_io_2, text ='Valider', command = ValiderIO)
	button_validate_io.pack(side=RIGHT)

def DestDir():
	global destdir
	destdir = tkFileDialog.askdirectory(initialdir=fenetre, title='Please select a destination directory')
	lbl_destdir.config(text="[...]/"+destdir.split("/")[-1])
	lbl_destdir.pack()

def DestDir2():
	global destdir2
	destdir2 = tkFileDialog.askdirectory(initialdir=fenetre, title='Please select a destination directory')
	lbl_destdir2.config(text="[...]/"+destdir2.split("/")[-1])
	lbl_destdir2.pack()

def DestDir3():
	global destdir3
	destdir3 = tkFileDialog.askdirectory(initialdir=fenetre, title='Please select a destination directory')
	lbl_destdir3.config(text="[...]/"+destdir3.split("/")[-1])
	lbl_destdir3.pack()

def SrcDir():
	global srcdir
	srcdir = tkFileDialog.askdirectory(initialdir=fenetre, title='Please select a source directory')
	lbl_srcdir.config(text="[...]/"+srcdir.split("/")[-1])
	lbl_srcdir.pack()

def GenConstraint():
	inf = Int(entree_inf.get())
	sup = Int(entree_sup.get())
	if destdir and filemat and (inf or sup):
		if inf != None and sup != None and (inf != sup): # les deux arguments sont donnés
			if inf > sup:
				sup = sup + inf
				inf = sup - inf
				sup = sup - inf
			for i in range(inf, sup+1):
				text=contraintes_AMPL(filemat, i)
				file_out = open(destdir+"/contraintes_"+filemat.split("/")[-1].split(".")[0]+"_"+str(i)+".dat", 'w')
				file_out.write(text)
				file_out.close()
		else: # au moins un argument est donné
			if inf!= None:
				text=contraintes_AMPL(filemat,inf)
			else:
				text=contraintes_AMPL(filemat,sup)
			file_out = open(destdir+"/contraintes_"+filemat.split("/")[-1].split(".")[0]+".dat", 'w')
			file_out.write(text)
			file_out.close()
	else:
		print "Argument manquant"
		if not destdir :
			print "\t- Vous devez sélectionner un dossier de destination"
		if not filemat :
			print "\t- Vous devez sélectionner un fichier Matlab"
		if not (inf or sup):
			print "\t- Vous devez spécifier au moins une borne"

def GenSoP():
	if srcdir and destdir2 and filemat:
		files = listdir(srcdir) # on liste les fichiers dans le dossier source
		st = ""
		for f in files:
			if f.split(".")[-1] == "sol":
				# Q&D : on lit les largeurs obtenues par l'optimisation
				W_var=[]
				fichier = open(srcdir+"/"+f, 'r')
				line = ""
				while line.strip("\n") != "Wx":
					line = fichier.readline()
					if "Objective" in line:
						w = float(line.split(":")[-1].strip("\n"))
				line = fichier.readline()
				nb_var=0
				while line.strip("\n") != "Wy":
					W_var.append(int(float(line.strip("\n"))))
					nb_var += 1
					line = fichier.readline()
				line = fichier.readline()
				while line.strip("\n") != '':
					W_var.append(int(float(line.strip("\n"))))
					nb_var += 1
					line = fichier.readline()
				w /= nb_var
				fichier.close()


				# à partir des largeurs des variables on détermine les largeurs des coeff
				WL_cst, WL_var = wordlengths_cst_var_post_optim(filemat,W_var)
				DWL = {"W_var":W_var, "WL_cst":WL_cst, "WL_var":WL_var, "formatting":True}
				print DWL
				DSIF = MatlabDict2FilterExample_SIF(filemat, dicos=DWL)
				# on génère les osops en considérant les largeurs obtenues ou calculées
				OSOP =best_oSoP_gen_from_dict(DSIF)

				eps = []
				for osop in OSOP:
					eps.append(osop._Top._total_error.inter)
					#print eps[-1]
					#print osop._var_final.FPF
				
				D = loadmat(filemat)
				dcge = D["dcHe"][0]
				wcpge = [D["wcpgHe"][i][0] for i in range(len(D["wcpgHe"]))]
				err_fin = erreur_finale(eps, wcpge, dcge)
				print err_fin
				st += "{0} {1}\n".format(w, max(abs(err_fin[0]),abs(err_fin[1])))

				fichier = open(destdir2+"/"+f.replace("contraintes", "osops").replace("sol","pkl"), "w")
				dump(OSOP, fichier)
				fichier.close()
		file_gnuplot = open(destdir2+"/datas_{0}.dat".format(filemat.split("/")[-1].split(".")[0]), "w")
		file_gnuplot.write(st)
		file_gnuplot.close()
	else:
		print "Argument manquant"
		if not srcdir :
			print "\t- Vous devez sélectionner un dossier source (contenant un ou plusieurs fichiers solutions)"
		if not filemat :
			print "\t- Vous devez sélectionner un fichier Matlab "
		if not destdir2:
			print "\t- Vous devez sélectionner un dossier de destination (qui contiendra les fichiers d'oSoPs générés)"

def GenSoP_isoWL():
	inf_isow = Int(entree_inf_isow.get())
	sup_isow = Int(entree_sup_isow.get())
	if inf_isow and sup_isow and filemat and destdir3:

		D = loadmat(filemat)
		Z=D["Z"]
		nt = int(D["l"])
		nx = int(D["n"])
		nu = int(D["m"])
		ny = int(D["p"])
		u_m = D["um"][0][0]
		u_r = D["ur"][0][0]
		dcu = [D["dcHu"][i][0] for i in range(len(D["dcHu"]))]
		wcpgu = D["wcpgHu"][0]
		dce = D["dcHe"][0]
		wcpge = [D["wcpgHe"][i][0] for i in range(len(D["wcpgHe"]))]


		M_cst={} # clés : indices (i,j) du coefficient non trivial de la matrice Z, valeurs : msb correspondant
		delta={} # clés : indice du SoP, valeurs : delta correspondant

		st = ""
		# pour chaque largeur dans l'intervalle donnée
		for  w in range(inf_isow, sup_isow+1):
			print "\nlargeur : "+str(w)+"\n"
			# pour chaque SoP
			for i in range(nt+nx+ny):
				d={}
				# pour chaque produit
				for j in range(nt+nx+nu):
					if (i<nt):
						if i != j:
							if (Z[i][j] != 0):
								C=Constant(Z[i][j],wl=20)
								d[j] = C
					else:
						if (Z[i][j] !=0):
							C=Constant(Z[i][j],wl=20)
							d[j] = C
				if len(d.keys()) > 1 or (len(d.keys()) == 1 and d[d.keys()[0]].value != 1 ):
					for j in range(nt+nx+nu):
						if j in d.keys():
							M_cst[i,j] = d[j].FPF.msb
					if len(d.keys()) > 1:
						if rounding_mode == "truncature":
							delta[i] = int(floor(log(len(d.keys())-1,2)))+1
						else:
							delta[i] = int(floor(log(len(d.keys()),2)))+1
					else:
						delta[i] = 0

			m_var_out = []
			for i in range(nt+nx+ny):
				# calcul de la plus grande valeur représentable dans l'intervalle
				if abs(u_m*dcu[i] - u_r*wcpgu[i]) > abs(u_m*dcu[i] + u_r*wcpgu[i]):
					diff_out = u_m*dcu[i] - u_r*wcpgu[i]
				else:
					diff_out = u_m*dcu[i] + u_r*wcpgu[i]
				# calcul du msb de cette plus grance valeur
				m_var_out.append(coef2msb(diff_out))
			m_var_in = m_var_out[: (nt+nx)] + [coef2msb(u_m - u_r)]

			# calcul de l'erreur de calcul...
			E_m = [] 
			E_r = []

			# troncature
			for i in range(nt+nx+ny):
				if i in delta.keys():
					tmp = m_var_out[i] - delta[i]
					e = float(-2**m_var_out[i] + 2**(tmp))
					for j in range(nt+nx+nu):
						if (i,j) in M_cst.keys():
							e_tmp = M_cst[i,j] + m_var_in[j]+1
							if tmp > e_tmp:
								e += -2**tmp + 2**e_tmp
					if e != float(-2**m_var_out[i] + 2**(tmp)):
						e *= 2**(-w)
						E_m.append(e)
						E_r.append(-e)
					else:
						E_m.append(0.)
						E_r.append(0.)
				else:
					E_m.append(0.)
					E_r.append(0.)

			Dy_m = 0.
			Dy_r = 0.
			for i in range(nt+nx+ny):
				Dy_m += dce[i] * E_m[i]
				Dy_r += wcpge[i] * E_r[i]


			#st += "{0} {1} {2}\n".format(w, Dy_m, Dy_r)

			W_var = [w for k in range(nt+nx+ny)]
			WL_cst, WL_var = wordlengths_cst_var_post_optim(filemat,W_var, iso_wl=False)
			DWL = {"W_var":W_var, "WL_cst":WL_cst, "WL_var":WL_var, "formatting":True}
			print DWL
			DSIF = MatlabDict2FilterExample_SIF(filemat, dicos=DWL)
			# on génère les osops en considérant les largeurs obtenues ou calculées
			OSOP =best_oSoP_gen_from_dict(DSIF)

			eps = []
			for osop in OSOP:
				eps.append(osop._Top._total_error.inter)

			D = loadmat(filemat)
			dcge = D["dcHe"][0]
			wcpge = [D["wcpgHe"][i][0] for i in range(len(D["wcpgHe"]))]
			err_fin = erreur_finale(eps, wcpge, dcge)
			print err_fin
			st += "{0} {1}\n".format(w, max(abs(err_fin[0]),abs(err_fin[1])))

			fichier = open(destdir3+"/osops_{0}_w{1}.pkl".format(filemat.split("/")[-1].split(".")[0], w), "w")
			dump(OSOP, fichier)
			fichier.close()

		file_gnuplot = open(destdir3+"/isow_{0}.dat".format(filemat.split("/")[-1].split(".")[0]), "w")
		file_gnuplot.write(st)
		file_gnuplot.close()
	# - créer W_var avec la meme largeur
	# - créer WL_cst et WL_var avec les bonnes clés et la même largeur

filemat = None
destdir = None
srcdir = None
destdir2 = None
destdir3 = None

# à modifier
rounding_mode = "truncature"

fenetre = Tk()
fenetre.geometry("500x700+1500+250") 

canvas = Canvas(fenetre, width=500, height=70, background='white')
txt = canvas.create_text(15, 35, text="FiPo", font=("Helvectica", "50"), fill="#000000", anchor=W)
txt = canvas.create_text(115, 35, text="Gen", font=("Helvectica", "50"), fill="#0090d3", anchor=W)
image = Image.open("server/views/logo.png")  
photo = ImageTk.PhotoImage(image) 
canvas.create_image(288, 36, anchor=W, image=photo)
canvas.pack(side=TOP)

global_frame = Frame(fenetre)
global_frame.pack(fill=BOTH)

# Gestion Fichiers

l = LabelFrame(global_frame, text="Sélectionner le fichier")
l.pack(side=TOP, fill=X, padx=15, pady=0)

frame_browser = Frame(l, padx=5, pady=5)
frame_browser.pack(side=TOP, fill=X)

lbl_browser = Label(frame_browser,text=0) 
file_browser = Button(frame_browser, text ='Parcourir', command = Browser)
file_browser.pack(side=LEFT)



# Traitement (uniquement optim pour le moment)

# Partie 1 (pré-optim)
l_optim1 = LabelFrame(global_frame, text="Génération des contraintes")
l_optim1.pack(side=TOP, fill=X, padx=15, pady=0)

frame_destdir = Frame(l_optim1, padx=5, pady=5)
frame_destdir.pack(side=TOP, fill=X)

lbl_destdir = Label(frame_destdir,text=0)
Label(frame_destdir,text="Sélectionner le dossier de destination").pack(side=LEFT)
destDir= Button(frame_destdir, text ='Parcourir', command = DestDir)
destDir.pack(side=RIGHT)

frame_erreur = Frame(l_optim1, padx=5, pady=5)
frame_erreur.pack(side=TOP, fill=X)
Label(frame_erreur,text="Sélectionner l'intervalle pour l'erreur (en puissance de 2)").pack(side=TOP)
Label(frame_erreur,text="de ").pack(side=LEFT)
# entree_inf
inf = StringVar() 
entree_inf = Entry(frame_erreur, width=3)
entree_inf.pack(side=LEFT)
Label(frame_erreur,text=" à ").pack(side=LEFT)
# entree_sup
sup = StringVar() 
entree_sup = Entry(frame_erreur, width=3)
entree_sup.pack(side=LEFT)

generate_cons = Button(l_optim1, text ='Générer', command = GenConstraint)
generate_cons.pack()


# Partie 2 (post-optim)
l_optim2 = LabelFrame(global_frame, text="Génération des SoP")
l_optim2.pack(side=TOP, fill=X, padx=15, pady=0)

frame_srcdir = Frame(l_optim2, padx=5, pady=5)
frame_srcdir.pack(side=TOP, fill=X)

lbl_srcdir = Label(frame_srcdir,text=0)
Label(frame_srcdir,text="Sélectionner le dossier source").pack(side=LEFT)
srcDir= Button(frame_srcdir, text ='Parcourir', command = SrcDir)
srcDir.pack(side=RIGHT)

frame_destdir2 = Frame(l_optim2, padx=5, pady=5)
frame_destdir2.pack(side=TOP, fill=X)

lbl_destdir2 = Label(frame_destdir2,text=0)
Label(frame_destdir2,text="Sélectionner le dossier de destination").pack(side=LEFT)
destDir2= Button(frame_destdir2, text ='Parcourir', command = DestDir2)
destDir2.pack(side=RIGHT)

generate_sop = Button(l_optim2, text ='Générer', command = GenSoP)
generate_sop.pack()


# iso wordlength
l_isow = LabelFrame(global_frame, text="Largeur commune")
l_isow.pack(side=TOP, fill=X, padx=15, pady=0)

frame_destdir3 = Frame(l_isow, padx=5, pady=5)
frame_destdir3.pack(side=TOP, fill=X)

lbl_destdir3 = Label(frame_destdir3,text=0)
Label(frame_destdir3,text="Sélectionner le dossier de destination").pack(side=LEFT)
destDir3= Button(frame_destdir3, text ='Parcourir', command = DestDir3)
destDir3.pack(side=RIGHT)

frame_isow = Frame(l_isow, padx=5, pady=5)
frame_isow.pack(side=TOP, fill=X)
Label(frame_isow,text="Sélectionner l'intervalle pour la largeur commune").pack(side=TOP)
Label(frame_isow,text="de ").pack(side=LEFT)
# entree_inf_isow
inf_isow = StringVar() 
entree_inf_isow = Entry(frame_isow, width=3)
entree_inf_isow.pack(side=LEFT)
Label(frame_isow,text=" à ").pack(side=LEFT)
# entree_sup_isow
sup_isow = StringVar() 
entree_sup_isow = Entry(frame_isow, width=3)
entree_sup_isow.pack(side=LEFT)

generate_isow = Button(l_isow, text ='Générer', command = GenSoP_isoWL)
generate_isow.pack()

fenetre.mainloop()











