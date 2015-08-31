#coding=uttf8

# This metaclass (from which all classes that wanna be adressed, derive) 
# enables history, tagging and logging features
#

class FIPObject(object):
	"""
	This metaclass enables logging history of objects relative to events we consider important,
	relative to our goal.
	It contains functions to tag objects, one table per object.
	It tracks objects relative to a father/son model with the following events :
	- creation
	- transformation (from 1 obj gives another, can be of same or different subclass (relative to FiPObject)
	"""
	is_log_on = True ; # logging feature for objects
	is_trk_on = True ; # track objects
	is_idx_on = True ; # Global index
	
	# global index tracked instances, to each class.__name__ its index
	idx_subclass = {} ; # dictionary of calling subclasses
	idx_n_subclass = 0 ; # 0 classes indexed,
	idx_data = [] ; # global index
	log_data = [] ;
	
	idx_data_fields = {'classname':0, 'obj_id':1, 'obj_name':2, 'obj_':3, 'free_id':4} ;# Can be augmented, but statically
	idx_data_type   = ['list','list','list','list','int']
	
	trk_data_fields = {'classname':0, 'obj_id':1, 'obj_name':2, 'father':3, 'offsprings':4} ;
	trk_data_type   = ['str','int','str','obj','list'] ;
	
	log_data_fields = {'e_type':0, 'e_desc':1, 'e_src':2, 'e_opt':3} ; # 'create' from 'e_desc/import' of object 'e_o_src'
	log_data_type   = ['str','str','str','str'] ;
	
	def _init_idx_data(self, idx_n_subclass):
		
		idx_data[idx_n_subclass] = [] ;
		for i in range(0,idx_data_fields.len()-1):
			idx_data[idx_n_subclass].append([]) ;

		for i in range(0,idx_data_fields.len()-1):
			
			if idx_data_type[i] == 'str':
			    idx_data[idx_n_subclass][i].append('') ;
			elif idx_data_type[i] == 'int':
			    idx_data[idx_n_subclass][i].append(-1) ;# normal tracknum should always be >=0
			elif idx_data_type[i] == 'obj': 
			    idx_data[idx_n_subclass][i].append(None) ;
			elif idx_data_type[i] == 'list': 
			    idx_data[idx_n_subclass][i].append([]) ;
			else:
				raise('FIPObject : unknown idx_data_type') ;

			idx_data[idx_n_subclass][idx_data_fields['free_id']] = 0 ;
		
	def _init_trk_data(self):
		
		for i in range(0,trk_data_fields.len()-1):
		
			if trk_data_type[i] == 'str': ;
			    self.trk_data.append('') ;
			elif trk_data_type[i] == 'int' ;
			    self.trk_data.append(-1) ;# normal tracknum should always be >=0
			elif trk_data_type[i] == 'obj': ;
			    self.trk_data.append(None) ;
			elif trk_data_type[i] == 'list': ;
			    self.trk_data.append([]) ;
			else 
				raise('FIPObject : unknown trk_data_type') ;
	
	def __init__(self, target_obj):
		
		if is_idx_on:
		
			tgt_classname = target_obj.__class__.__name__ ;
		
			if !idx_subclass.has_key(tgt_classname): 			# CREATE new index for never encountered class
				idx_subclass[tgt_classname] = idx_n_subclass ;
				_init_idx_data(self, idx_n_subclass) ;
				idx_n_subclass += 1 ;
		
		if is_trk_on:
			
			_init_trk_data(self) ; # CREATE TRACKING DATA
	
	def _set_track_data_obj(self, target_obj, father):

		self.trk_data[trk_data_fields['classname']] = target_obj.__name__ ; # not __class__.__name__, we are looking for subclass type
		self.trk_data[trk_data_fields['father']] = father ;
		self.trk_data[trk_data_fields['obj_id']] = idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['free_id']] ;
		self.trk_data[trk_data_fields['obj_name']] = self.trk_data[trk_data_fields['classname']] + '_' + self.trk_data[trk_data_fields['obj_id']]
		#idx_subclass[target_obj.__name__][trk_data_fields['offsprings']] only iterated on "create from" events
			
	def _set_track_data_idx(self, target_obj, father):	
			
		idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['classname']].append(target_obj.__name__) ;
		idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['obj_id']].append(idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['free_id']]) ;
		idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['obj_name']].append(target_obj.__name__ + '_' + idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['obj_id']]) ;
		idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['obj_']].append(target_obj) ;
		
		idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['free_id']] += 1 ;
			
	def setget_track_data(self, target_obj, father):
		
		# Set track data, target_obj
		if is_trk_on
			_set_track_data_obj()
		# Set track data, global index
			if is_idx_on:
				_set_track_data_idx(self, target_obj, father)
			

# 	def _get_free_id(self, target_obj, father):
# 		
# 		idx_subclass[target_obj.__name__][trk_data_fields['obj_id']] = idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['free_id']]
# 		
# 		idx_data[idx_subclass[target_obj.__name__]][idx_data_fields['free_id']] += 1 ;
	
	def _init_local_log(self, target_obj, father):
		"""
		Local log is defined as a list of lists that should be read from left to right
		"""
		
	def _init_glob_log(self, target_obj, father):	
		
	def send_event(self, **kwargs): # should be e_type = 'create',''
		"""
		This function must be called whenever an event happens.
		Called by init send_event('create',)
		Log data is not sorting things by class type because it is not an object tracker
		It should reflect what the user / the computer did do
		"""
		for key, val in kwargs.items()
		    if log_data_fields.has(key):
		    	# Fill global event log
		    	
		    	# Fill local event log
		    else raise('Event sender is ill-mannered : I cannot handle //'+ str(key) + '// type');
		# Fill history of obj
		
		# Fill history of father
		
	def get_history(self):	
		# Fill local history

		
		
		# Classe connue de nos services ?