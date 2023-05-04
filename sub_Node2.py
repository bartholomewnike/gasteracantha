from Node2 import Node

class sub_Node(Node):
  
  parent_id = 0
  
  def set_Parent( self , parent ):
    self.parent_id = parent
  def type(self):
    return 'sub_Node'