from pickle import load

fichier = open("Examples/These/liste_osops.pkl",'r')
L_osops = load(fichier)
fichier.close()

for l in L_osops:
	print l