class FIPlabel(object):
	
	"""
	This class is used to label objects, that can be indexed in a FIPindex
	"""
	
	def __init__(self, tgt_class, tgt_subclass, father = None):
		
		self.obj_class = tgt_class
		self.obj_subclass = tgt_subclass
		self.obj_id = id(self)
		
		# To get the current free_id we need an index
		# If it is not we cannot get a "clean" id
		
		self.obj_name = tgt_subclass + "_" + self.obj_id
		self.offsprings = []
		self.obj_father = father
	
	def add_offspring(self, offspring):
		
		self.offsprings.append(offspring)
		
	def __repr__(self):
		
		fmt = '{1:12} = {1:10}\n'
		
		print fmt.format('class', self.obj_class)
		print fmt.format('subclass', self.obj_subclass)
		print fmt.format('obj_id', str(self.obj_id))
		print fmt.format('obj_name', self.obj_name)
		
		if self.father is not None:
			father_name = self.father.trk_info.obj_name
		else:
		    father_name = 'None'
		    
		print fmt.format('obj_father', father_name, '\n')
		
		str_list_offsprings = []
		
		if self.offsprings:
			
			for offspring_obj in self.offsprings:
				
			   str_list_offsprings.append(offspring_obj.label.obj_name)
			
		else: 
			
			str_list_offsprings.append('None')
		
		print fmt.format('offsprings', str_offspring[0])
		
		for str_offspring in str_list_offsprings[1:]:
		
		    print fmt.format('', str_offspring)
		