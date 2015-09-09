#coding=utf8

class FIPLabel(object):
    
    """
    This class is used to label objects, that can be indexed in a FIPindex
    """
    
    is_debug_print = True # print label at end of __init__
    
    # Contains subclass:free_num items
    free_num ={}

    def __repr__(self):
        
        fmt = '{0:20} = {1:20}'
        
        # TODO use a dict, but not for the end of routine
        
        label_list = ['obj_class', 'obj_subclass', 'obj_id', 'obj_num', 'obj_name']
        
        for lbl in label_list:
            print fmt.format(lbl, self.trk_label[lbl])
        
        if self.trk_label['obj_father'] is not None:
            father_name = self.trk_label['obj_father'].trk_label['obj_name']
        else:
            father_name = 'None'
            
        print fmt.format('obj_father', father_name, '\n')
        
        str_list_offsprings = []
        
        if self.trk_label['obj_offsprings']:
            
            for offspring_obj in self.trk_label['obj_offsprings']:
                
               str_list_offsprings.append(offspring_obj.trk_label['obj_name'])
            
        else: 
            
            str_list_offsprings.append('None')
        
        print fmt.format('obj_offsprings', str_list_offsprings[0])
        
        for str_offspring in str_list_offsprings[1:]:
        
            print fmt.format('', str_offspring)
    
    def __init__(self, tgt_subclass, father = None):
        
        self.trk_label = {}
        
        str_allbaseclass = []
        
        for str_baseclass in self.__class__.__bases__:
            str_allbaseclass.append(str_baseclass.__name__)
        

        
        self.trk_label['obj_class'] = ' '.join(str_allbaseclass)
        
        self.trk_label['obj_subclass'] = tgt_subclass
        self.trk_label['obj_id'] = id(self)
        
        # set obj num, init if not, increment
        FIPLabel.free_num.setdefault(self.trk_label['obj_subclass'], 0)
        
        self.trk_label['obj_num'] = FIPLabel.free_num[self.trk_label['obj_subclass']]

        FIPLabel.free_num[self.trk_label['obj_subclass']] += 1

        self.trk_label['obj_name'] = self.trk_label['obj_subclass'] + "_" + str(self.trk_label['obj_num'])

        self.trk_label['obj_father'] = father

        self.trk_label['obj_offsprings'] = []
    
        if FIPLabel.is_debug_print: FIPLabel.__repr__(self)
    
    def add_offspring(self, offspring):
        
        self.trk_label['offsprings'].append(offspring)
        

        