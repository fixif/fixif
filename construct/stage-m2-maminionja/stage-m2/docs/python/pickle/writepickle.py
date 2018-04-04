 #!/usr/bin/env python

import pickle

dico = { "nom":"Ravoson", "prenom":"Maminionja"}

file = open("dicosave.pkl","wb")
pickle.dump(dico,file)
file.close()
