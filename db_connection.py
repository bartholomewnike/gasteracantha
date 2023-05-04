import sqlite3
import subprocess
from cherry_tree2 import cherry_tree

def database_info(scan_name , cherry , database_location = ''):

  #base program assumes scan is done running whether aborted or completed
  if database_location=='': database_location='spiderfoot.db'
  
  connection = sqlite3.connect(database_location)
  cursor = connection.cursor()
  scan_id = cursor.execute('SELECT guid FROM tbl_scan_instance WHERE name = ?',(scan_name,)).fetchall()
  scan_id = scan_id[0][0]
  module_names = cursor.execute('SELECT module FROM tbl_scan_results WHERE scan_instance_id = ? GROUP BY module', (scan_id,)).fetchall()
  #list of tuples
  rows = cursor.execute('SELECT module , type , data , risk , false_positive , confidence , visibility,hash FROM tbl_scan_results WHERE scan_instance_id = ?' , (scan_id ,)).fetchall()
  correlation_results=cursor.execute('SELECT id,title,rule_risk,rule_id,rule_name,rule_descr,rule_logic FROM tbl_scan_correlation_results WHERE scan_instance_id=?',(scan_id,)).fetchall()
  #list of (...,...)
  correlation_events=cursor.execute('SELECT * FROM tbl_scan_correlation_results_events').fetchall()
  module_id = []
  module_types = []

  i = 0
  cherry.add_Node(scan_name + ': ' + scan_id)
  scan_node_id = len(cherry.nodes_list)
  
  num_nodes=len(cherry.nodes_list)
  
  while i < len(module_names):

    if module_names[i][0][:4]=='sfp_': cherry.add_sub_Node(scan_node_id , module_names[i][0][4:])
    else: cherry.add_sub_Node(scan_node_id , module_names[i][0])
    module_id.append(len(cherry.nodes_list))
    #[[type , id , count] , [type,id,count],...],[...],...]
    module_types.append([])
    i += 1
  i = 0
  
  while i < len(rows):
    n = 0
    id = len(cherry.nodes_list)
    is_unique = True
    #find module node id
    index_of = module_names.index((rows[i][0],))
        
    #check if type is a node for module
    while n < len(module_types[index_of]):
       #checking type against type
      if module_types[index_of][n][0] == rows[i][1]:
            
        is_unique = False
        #giving data nodes a name of count
        cherry.add_sub_Node(module_types[index_of][n][1] , module_types[index_of][n][2])
        id3 = len(cherry.nodes_list)
        module_types[index_of][n][2] += 1
            
        cherry.add_text(str(rows[i][2]) , id3)
        cherry.add_text(str(rows[i][2]) , module_types[index_of][n][1])
        cherry.add_sub_Node(id3 , 'Risk: ' + str(rows[i][3]))
        cherry.add_sub_Node(id3 , 'False Positive: ' + str(rows[i][4]))
        cherry.add_sub_Node(id3 , 'Confidence: ' + str(rows[i][5]))
        cherry.add_sub_Node(id3 , 'Visibility: ' + str(rows[i][6]))
        
        if len(rows[i])>7:
          mmm=0
          while mmm<len(correlation_events):
            if rows[i][7]==correlation_events[mmm][1]:
              
              hash=correlation_events[mmm][0]
              mmm=len(correlation_events)
              mnm=0
              while mnm<len(correlation_results):
                if correlation_results[mnm][0]==hash:
                  cherry.add_sub_Node(id3,correlation_results[mnm][4])
                  for data in correlation_results[mnm]:
                    cherry.add_text(str(data),len(cherry.nodes_list))
                    
                    if correlation_results[mnm][2]=='INFO':
                      #cherry.nodes_list[index_of+num_nodes].foreground='#26a269'
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#26a269'
                      cherry.nodes_list[id3-1].foreground='#26a269'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#26a269'
                    elif correlation_results[mnm][2]=='LOW':
                      #cherry.nodes_list[index_of+num_nodes].foreground='#1a5fb4'
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#1a5fb4'
                      cherry.nodes_list[id3-1].foreground='#1a5fb4'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#1a5fb4'
                    elif correlation_results[mnm][2]=='MEDIUM':
                      #cherry.nodes_list[index_of+num_nodes].foreground='#f8e45c'
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#f8e45c'
                      cherry.nodes_list[id3-1].foreground='#f8e45c'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#f8e45c'
                    elif correlation_results[mnm][2]=='HIGH':
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#ff0000'
                      cherry.nodes_list[id3-1].foreground='#ff0000'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#ff0000'
                mnm+=1
            mmm+=1
        n = len(module_types[index_of])
      n += 1
    if is_unique:
         
      cherry.add_sub_Node(module_id[index_of] , rows[i][1])
      id2 = len(cherry.nodes_list)
      module_types[index_of].append([rows[i][1] , id2 , 2])
        
      cherry.add_sub_Node(id2 , 1)
      id3 = len(cherry.nodes_list)
        
      cherry.add_text(str(rows[i][2]) , id3)
      cherry.add_text(str(rows[i][2]) , module_types[index_of][n][1])
      cherry.add_sub_Node(id3 , 'Risk: ' + str(rows[i][3]))
      cherry.add_sub_Node(id3 , 'False Positive: ' + str(rows[i][4]))
      cherry.add_sub_Node(id3 , 'Confidence: ' + str(rows[i][5]))
      cherry.add_sub_Node(id3 , 'Visibility: ' + str(rows[i][6]))
      if len(rows[i])>7:
          mmm=0
          while mmm<len(correlation_events):
            if rows[i][7]==correlation_events[mmm][1]:
              
              hash=correlation_events[mmm][0]
              mmm=len(correlation_events)
              mnm=0
              while mnm<len(correlation_results):
                if correlation_results[mnm][0]==hash:
                  cherry.add_sub_Node(id3,correlation_results[mnm][4])
                  for data in correlation_results[mnm]:
                    cherry.add_text(str(data),len(cherry.nodes_list))
                    
                    if correlation_results[mnm][2]=='INFO':
                      #cherry.nodes_list[index_of+num_nodes].foreground='#26a269'
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#26a269'
                      cherry.nodes_list[id3-1].foreground='#26a269'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#26a269'
                    elif correlation_results[mnm][2]=='LOW':
                      #cherry.nodes_list[index_of+num_nodes].foreground='#1a5fb4'
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#1a5fb4'
                      cherry.nodes_list[id3-1].foreground='#1a5fb4'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#1a5fb4'
                    elif correlation_results[mnm][2]=='MEDIUM':
                      #cherry.nodes_list[index_of+num_nodes].foreground='#f8e45c'
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#f8e45c'
                      cherry.nodes_list[id3-1].foreground='#f8e45c'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#f8e45c'
                    elif correlation_results[mnm][2]=='HIGH':
                      cherry.nodes_list[index_of+num_nodes].foreground='#ff0000'
                      cherry.nodes_list[id2-1].foreground='#ff0000'
                      cherry.nodes_list[id3-1].foreground='#ff0000'
                      cherry.nodes_list[len(cherry.nodes_list)-1].foreground='#ff0000'
                mnm+=1
            mmm+=1
    i += 1