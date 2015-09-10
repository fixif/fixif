from time import time

class FIPevent(object):
	
	"""
	This class defines an event that can be logged and output
	We define two different kinds of events
	
	- Object tracking events
	- User-defined events
	
	The events are logged at class level and timestamped
	
	"""
	# Definition of available events
	
	e_type = {'create':'obj_event', 'destruct':'obj_event', 'log':'simple_event'}
	
	e_obj_origin = {'user_input':'obj_event', 'external':'obj_event', 'func':'obj_event'}
	
	e_desc = {'convert'}
	
	e_src_func = ''
	e_src_subclass = ''
	
	def __init__(self, **kwargs):
		
		pass;
		
		#if e_type
		
	def log_event(self):
		
		event_timestamp = time()
		
		pass;
		
		"""
		Put the event in global log
		"""
	
	def __repr__(self):
		
		pass;
		
		"""
		Output human-readable string from event
		"""