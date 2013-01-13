#! /usr/bin/env python
import json
import os 
import glob
from collections import deque 
from ete2 import Tree
from ete2 import SeqGroup
from subprocess import call
tempfiles=[]
alpha = 0.01
target_tax = "6656"

#tax_id|parent tax_id|rank
def parseNodesDump(sfin_node, sfin_name, sfout):
    nodes_rank_map = {}
    nodes_name_map = {}
    father_son_map = {}
    fin = open(sfin_node)
    lines = fin.readlines()
    fin.close()
    
    print("Number nodes:" + repr(len(lines)))
    for line in lines:
        line = line.strip()
        toks = line.split("|")
        son = toks[0]
        father = toks[1]
        rank = toks[2]
        
        nodes_rank_map[son] = rank
        if father != son:
            if father in father_son_map:
                father_son_map[father].append(son)
            else:
                father_son_map[father] = [son]
    cnt = 0
    for key in list(father_son_map.keys()):
        sons = father_son_map[key]
        cnt = cnt + len(sons)
    print("Nodes count:" + repr(cnt))
    print("Nodes rank count:" + repr(len(nodes_rank_map.keys())))
    
    fnames = open(sfin_name)
    lines = fnames.readlines()
    fnames.close()
    
    for line in lines:
        line = line.strip()
        items = line.split("|")
        nodes_name_map[items[0]]=items[1]
    
    #construct the NCBI taxonomic tree
    t0 = Tree()
    t0.add_feature("id", "1")
    t0.add_feature("rank", "god")
    t0.add_feature("name", "root")
    k = 0
    nodesque = deque([t0])
    while len(nodesque)!=0:
         p = nodesque.popleft()
         sons = father_son_map.get(p.id, [])
         k=k+1
         if len(sons)!=0:
             for son in sons:
                 newnode = p.add_child()
                 newnode.add_feature("id", son)
                 newnode.add_feature("rank", nodes_rank_map.get(son,"no_rank"))
                 newnode.add_feature("name", nodes_name_map.get(son,"no_name"))
                 nodesque.append(newnode)
    print(k)    
    t0.write(outfile="tree_of_life.tree", format=8, features=["rank","id"])


def parseNodesDump_idonly(sfin_node):
    father_son_map = {}
    fin = open(sfin_node)
    lines = fin.readlines()
    fin.close()
    
    print("Number nodes:" + repr(len(lines)))
    for line in lines:
        line = line.strip()
        toks = line.split("|")
        son = toks[0]
        father = toks[1]
        rank = toks[2]
        if father != son:
            if father in father_son_map:
                father_son_map[father].append(son)
            else:
                father_son_map[father] = [son]
    cnt = 0
    for key in list(father_son_map.keys()):
        sons = father_son_map[key]
        cnt = cnt + len(sons)
    print("Nodes count:" + repr(cnt))
    t0 = Tree()
    t0.add_feature("name", "1")
    k = 0
    nodesque = deque([t0])
    while len(nodesque)!=0:
         p = nodesque.popleft()
         sons = father_son_map.get(p.name, [])
         k=k+1
         if len(sons)!=0:
             for son in sons:
                 newnode = p.add_child(name = son)
                 nodesque.append(newnode)
    print(k)    
    t0.write(outfile="tree_of_life_id.tree", format=8)



#parseNodesDump("clean_nodes.txt","clean_names.txt","")
parseNodesDump_idonly(sfin_node="clean_nodes.txt")
