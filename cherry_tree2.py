from Node2 import Node
from sub_Node2 import sub_Node
#take in file input; create nodes with names and text in a CherryTree file


class cherry_tree( object ):
  
  #keep track of the currently created node; this might have an effect on CherryTree functions
  node_num = 1
  nodes_list = []
  nodes_names_list = []
   
  def __init__( self , file_name ):
    self.file_name = file_name
    self.node_num = 1
    self.nodes_list =[]
    self.nodes_names_list = []
  
  def add_Node( self , name , unique_id = 0 , prog_lang="custom-colors" , tags="" , readonly="0" , nosearch_me="0" , nosearch_ch="0" , custom_icon_id="0" , is_bold="0" , foreground="" ):
    #ability to define a unique id; this could cause other functions to display strange behavior
    if unique_id == 0:
      unique_id = self.node_num
    
    node_1 = Node( name , unique_id , prog_lang="custom-colors" , tags="" , readonly="0" , nosearch_me="0" , nosearch_ch="0" , custom_icon_id="0" , is_bold="0" , foreground="" )
    self.node_num = self.node_num + 1 
    self.nodes_list.append( node_1 )
    self.nodes_names_list.append(name)
    
  def add_sub_Node( self , parent_id , name , unique_id = 0, prog_lang="custom-colors" , tags="" , readonly="0" , nosearch_me="0" , nosearch_ch="0" , custom_icon_id="0" , is_bold="0" , foreground="" ):
    
    if unique_id == 0:
      unique_id = self.node_num
      
    node_2 = sub_Node( name , unique_id , prog_lang="custom-colors" , tags="" , readonly="0" , nosearch_me="0" , nosearch_ch="0" , custom_icon_id="0" , is_bold="0" , foreground="" )
    self.node_num = self.node_num + 1
    node_2.set_Parent( parent_id )
    self.nodes_list.append( node_2 )
    self.nodes_names_list.append(name)
    self.nodes_list[parent_id-1].add_sub(self.nodes_list[unique_id-1])
    
  def add_text( self , text , node ):
    self.nodes_list[node-1].add_text(text)
    
  def build_It(self):
    f = open( self.file_name , 'a' , encoding = 'utf-8')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<cherrytree>\n')

    parent_list = []
    
    for n in self.nodes_list:
      if n.type() == 'Node':
        parent_list.append(n)
      
    for n1 in parent_list:
      n1.write_Xml(f)

    f.write('</cherrytree>')
    f.close()    