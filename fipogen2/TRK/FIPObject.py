#coding=utf8

import FIPlabel

class FIPObject(object):
	
	"""
	This class contains an index of instances of subclasses of FIPObject
	"""
	
	idx_subclass = {}
	
	def __init__(self, tgt_subclassname, father_obj = None):
		
		#Create label
		self.trk_info = FIPlabel(self, self.__class__.__name__, tgt_subclassname, father_obj)
		
		# Add instance to instance index
		FIPObject.idx_subclass.get(tgt_subclassname, []).append(self)
		
	def __repr__(self):
		
		sep = '---\n'
		
		print self.__class__.__name__ + " index \n"
		print sep
		
		for str_subclass in FIPObject.idx_subclass:
		
		    print str_subclass + ' : ' + str(len(FIPObject[str_subclass])) + " objects indexed \n"
		     
		    print sep
		     
		    for obj in FIPObject[str_subclass]:
		     	
		     	print obj.trk_label.obj_name + '\n'
		
            print sep