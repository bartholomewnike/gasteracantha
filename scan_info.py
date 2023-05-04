#Gasteracantha
#Nicholas Bartholomew

import subprocess
import datetime
import os
from cherry_tree2 import cherry_tree

#this file will give utility and definitions for determining scan/data
#this will specifically relate to displaying information in CherryTree

def nikto_scan(target,cherry):
  f=open(target,'r')
  lines=f.readlines()
  last=lines.pop()
  num_nodes=0
  names_tups=[]
  add_info=''
  for l in lines:
    if 'Target IP' in l:
      cherry.add_Node('Nikto: '+l[12:].replace(' ',''))
      num_nodes=len(cherry.nodes_list)
      cherry.add_text(l,num_nodes)
    elif l[0]=='-': pass
    elif 'Target ' in l: cherry.add_text(l,num_nodes)
    elif 'Start ' in l: cherry.add_text(l,num_nodes)
    elif ' requests:' in l: cherry.add_text('\n'+l,num_nodes)
    elif 'End Time' in l: cherry.add_text(l+'\n'+last,num_nodes)
    else:
      ind=0
      try:
        ind=l.index(':')
      except ValueError: add_info +=l+'\n'
      else:
        name=l[2:ind]
        text=l[ind+1:]
        unique=True
        for n in names_tups:
          if name==n[0]:
            cherry.add_text(text+'\n',n[1])
            unique=False
            break
        if unique:
          cherry.add_sub_Node(num_nodes,name)
          cherry.add_text(text+'\n',len(cherry.nodes_list))
          names_tups.append((name,len(cherry.nodes_list)))
  if add_info != '':
    cherry.add_sub_Node(num_nodes,'Additional Information')
    cherry.add_text(add_info,len(cherry.nodes_list))

def nmap_scan( targets , scan_type , ports = '0'):
  
  #scan type: ping, service, os, all
  command = 'nmap ' + nmap_scan_flags(scan_type , ports)
  
  command += ' ' + targets
  file_name = create_file_name()
  command += ' >> ' + file_name
  #print(command)
  f = open(file_name , 'a')
  f.write(command + '\n')
  f.close()
  subprocess.run(command , shell=True)
  return file_name
  
def nmap_cherry(file_name , cher , remove = 1):
  #take a file with nmap scan data and put into cherrytree object
  f = open(file_name)
  lines = f.readlines()
  f.close()
  if remove == 1:
    os.remove(file_name)
  
  s1 = lines[0][:lines[0].find('>')-1]
  cher.add_Node(s1)
  
  scan_1_id = cher.nodes_names_list.index(s1) + 1
  target_id = scan_1_id
  
  lines.pop(0)
  cher.add_text(lines.pop(0) , scan_1_id )
  cher.add_text(lines.pop(-1) , scan_1_id )
  
  for l in lines:
    if 'Nmap scan report for' in l:
      cher.add_sub_Node(scan_1_id , l[l.find('for') + 3:])
      target_id = len(cher.nodes_list)
    elif l[0].isnumeric():
      if 'unrecognized' in l:
        cher.add_sub_Node(target_id , l[:l.find('.')])
        cher.add_text( l[l.find('.')+1:] + '\n' , len(cher.nodes_list))
      else:
        cher.add_sub_Node(target_id , l[:l.find('/')])
        cher.add_text( l[l.find('/')+1:] , len(cher.nodes_list))
    elif 'PORT' in l:
      pass
    elif l[0:2] == 'SF':
      cher.add_text(l,len(cher.nodes_list))
    else:
      cher.add_text(l , target_id)
      
def create_file_name():
  file_name = 'nmap_scan' + str(datetime.datetime.now()).replace(' ' , '' ) + '.txt'
  file_name = file_name.replace(':' , '')
  file_name = file_name.replace('-' , '')
  return file_name
  
def nmap_scan_flags(type , ports = '0'):
  ports = str(ports)
  command=''
  if type == "ping":
    command += '-sn'
  else:
    if ports == '0':
      command += '--top-ports '
      command += '1000 '
    else:
      command += '-p ' + ports
  if "service" in type:
    command += '-sV'
  if "os" in type:
    command += '-O'
  if "all" in type:
    command += '-A'
  return command
