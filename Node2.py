class Node( object ):
  
  
  #fields that CherryTree requires
  #initialized with standard values
  
  name = ''
  unique_id = 0
  prog_lang="custom-colors" 
  tags="" 
  readonly="0" 
  nosearch_me="0" 
  nosearch_ch="0" 
  custom_icon_id="0" 
  is_bold="0" 
  foreground="" 
  #ts_creation="1682528820" 
  #ts_lastsave="1682530324"
  rich_text = ''
  
  #list of IDs of children
  subs = []
  
  def type(self):
    return 'Node'
  
  def __init__( self , name , unique_id , prog_lang="custom-colors" , tags="" , readonly="0" , nosearch_me="0" , nosearch_ch="0" , custom_icon_id="0" , is_bold="0" , foreground="" ):
    self.name = str(name)
    self. unique_id = unique_id
    self.prog_lang = prog_lang 
    self.tags= tags
    self.readonly = readonly
    self.nosearch_me = nosearch_me
    self.nosearch_ch = nosearch_ch
    self.custom_icon_id = custom_icon_id
    self.is_bold = is_bold
    self.foreground = foreground
    self.subs = []
  
  def add_text( self , string_1 ):
    self.rich_text += str(string_1)
    
  def add_sub( self , sub_Node ):
    self.subs.append( sub_Node )
    
  def write_Xml(self , file):
    self.name = self.name.replace('<' , '&lt;')
    self.name = self.name.replace('>' , '&gt;')
    self.name = self.name.replace('&' , '&amp;')
    self.name = self.name.replace('"' , '&quot;')
    self.name = self.name.replace('\'' , '&apos;')
    write_string = ''
    if self.rich_text != '':
      xml_text = self.rich_text.replace('<' , '&lt;')
      xml_text = xml_text.replace('>' , '&gt;')
      xml_text = xml_text.replace('&' , '&amp;')
      xml_text = xml_text.replace('"' , '&quot;')
      xml_text = xml_text.replace('\'' , '&apos;')

      write_string = '<node name="%s" unique_id="%s" prog_lang="%s" tags="%s" readonly="%s" nosearch_me="%s" nosearch_ch="%s" custom_icon_id="%s" is_bold="%s" foreground="%s" ts_creation="1682528820" \
    ts_lastsave="1682530324">\n<rich_text>%s</rich_text>\n' %( self.name , self.unique_id , self.prog_lang , self.tags , self.readonly , self.nosearch_me , self.nosearch_ch , self.custom_icon_id , self.is_bold , self.foreground , xml_text )
    else:
        write_string =  '<node name="%s" unique_id="%s" prog_lang="%s" tags="%s" readonly="%s" nosearch_me="%s" nosearch_ch="%s" custom_icon_id="%s" is_bold="%s" foreground="%s" ts_creation="1682528820" \
    ts_lastsave="1682530324">\n' %( self.name , self.unique_id , self.prog_lang , self.tags , self.readonly , self.nosearch_me , self.nosearch_ch , self.custom_icon_id , self.is_bold , self.foreground )
    
    file.write(write_string)
    if self.subs != []:
      for n in self.subs:
        n.write_Xml(file)
    file.write('</node>')