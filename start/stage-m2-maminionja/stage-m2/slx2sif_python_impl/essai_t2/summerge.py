# Regrouper des additionneurs successives
# script de test de la fonction

print "\nRegrouper des additionneurs successives\n"


#liste des blocs et leur type
blocks = [[1,'s'],[2,'s'],[3,'-'],[4,'-'],[5,'s'],[6,'-'],[7,'-'],[8,'s'],[9,'-'],[10,'-'],[11,'-'],[12,'-']]

#les equations
equations = [[1,2,3],[2,4,5],[12,5], [5,6,7,8], [8,9,10,11]]


# Get the block type, given its SID
# b[0] : bloc SID
# b[1] : block type
def getbtype(sid, blockslist):
  for b in blockslist:
    if b[0] == sid:
      return b[1]
# test = getblocktype(2,blocks) #should print s


# Get the inputs list of a block, given its SID
def getbinputs(sid, equationslist):
  for eq in equationslist:
    if eq[0] == sid:
      return eq[1:]

### fonctions pour regrouper les additions ####
def summerge(blockslist, equationslist):
  for eq in equationslist:
    if getbtype(eq[0], blockslist) == 's': #eq[0] : la bloc de sortie
      for input in eq[1:]:
        if getbtype(input, blockslist) == 's':
          eq.remove(input)
          eq.extend(getbinputs(input,equations))
    
#function : get sum block number
def getsumnbr(blocks):
  nbr = 0
  for b in blocks:
    if b[1] == 's':
      nbr += 1
  return nbr

	
###### fonctions affichages ##
def afficher(list):
  for line in list:
    print line

###### iteration on Sum regroupment : nbr(Sum)-1 
afficher(equations)
for i in range(1,getsumnbr(blocks)):
  summerge(blocks, equations)
  print "\n--pass", i
  afficher(equations)


# function : verify if equation is not usefull
def iseqused(sid, equations):
  inputs = []
  for eq in equations:
    for block in eq[1:]:
      if block not in inputs:
        inputs.append(block)

  if sid in inputs:
    return True
  else:
    return False


# function : delete useless intermediate equation
def cleanequations(equations):
  for eq in equations:
    if getbtype(eq[0], blocks) == 's':  #  sum and not an Outpout
      if not iseqused(eq[0], equations):
        equations.remove(eq)


#equations clean up
#print iseqused(2, equations)
#print iseqused(5, equations)
#print iseqused(8, equations)
print "\n-- eq clean up"
cleanequations(equations)
afficher(equations)
