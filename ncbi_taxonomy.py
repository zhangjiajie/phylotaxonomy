#! /usr/bin/env python
import sys
import os
import json
import operator
from ete2 import Tree, TreeStyle, TextFace, SeqGroup
from subprocess import call
from oop import CMislabel

class sequence:
    def __init__(self, seq_id, tax_id="0"):
        #ranks[0] = species 
        #ranks[1] = genus
        #ranks[2] = family
        #ranks[3] = order
        #ranks[4] = class
        #ranks[5] = phylum   
        self.ranks = [""]*6
        self.curr_ranks_idx = 0
        self.seq_id = seq_id
        self.tax_id = tax_id
    
    def __str__(self):
        allranks=self.seq_id
        for r in self.ranks:
            allranks = allranks + "|" + r
        return allranks

    def __assignRank(self, rank, name):
        name = name.replace(" ", "_")
        if rank == "species":
            self.ranks[0] = name
        elif rank == "genus":
            self.ranks[1] = name
        elif rank == "family":
            self.ranks[2] = name
        elif rank == "order":
            self.ranks[3] = name
        elif rank == "class":
            self.ranks[4] = name
        elif rank == "phylum":
            self.ranks[5] = name 
    
    def __checkRank(self, rank_id_list, id_rank_map, id_name_map):
        for i, rank in enumerate(self.ranks):
            if rank == "":
                print("checking ranks for " + self.seq_id)
                if i == 0:
                    for rid in rank_id_list:
                        rkname = id_rank_map[rid]
                        if rkname == "forma":
                            name = id_name_map[rid]
                            self.ranks[0] = name
                            break
                        elif rkname == "varietas":
                            name = id_name_map[rid]
                            self.ranks[0] = name
                            break
                        elif rkname == "subspecies":
                            name = id_name_map[rid]
                            self.ranks[0] = name
                            break
                        
                elif i == 1:
                    for rid in rank_id_list:
                        rkname = id_rank_map[rid]
                        if rkname == "subgenus":
                            name = id_name_map[rid]
                            self.ranks[1] = name
                            break
                        
                elif i == 2:
                    for rid in rank_id_list:
                        rkname = id_rank_map[rid]
                        if rkname == "subtribe":
                            name = id_name_map[rid]
                            self.ranks[2] = name
                            break
                        elif rkname == "tribe":
                            name = id_name_map[rid]
                            self.ranks[2] = name
                            break
                        elif rkname == "subfamily":
                            name = id_name_map[rid]
                            self.ranks[2] = name
                            break
                        elif rkname == "superfamily":
                            name = id_name_map[rid]
                            self.ranks[2] = name
                            break
                        
                elif i == 3:
                    for rid in rank_id_list:
                        rkname = id_rank_map[rid]
                        if rkname == "parvorder":
                            name = id_name_map[rid]
                            self.ranks[3] = name
                            break
                        elif rkname == "infraorder":
                            name = id_name_map[rid]
                            self.ranks[3] = name
                            break
                        elif rkname == "suborder":
                            name = id_name_map[rid]
                            self.ranks[3] = name
                            break
                        elif rkname == "superorder":
                            name = id_name_map[rid]
                            self.ranks[3] = name
                            break
                elif i == 4:
                    for rid in rank_id_list:
                        rkname = id_rank_map[rid]
                        if rkname == "infraclass":
                            name = id_name_map[rid]
                            self.ranks[4] = name
                            break
                        elif rkname == "subclass":
                            name = id_name_map[rid]
                            self.ranks[4] = name
                            break
                        elif rkname == "superclass":
                            name = id_name_map[rid]
                            self.ranks[4] = name
                            break
                elif i == 5:
                    for rid in rank_id_list:
                        rkname = id_rank_map[rid]
                        if rkname == "subphylum":
                            name = id_name_map[rid]
                            self.ranks[5] = name
                            break
                        elif rkname == "superphylum":
                            name = id_name_map[rid]
                            self.ranks[5] = name
                            break
                
    def findMyRanksByTree(self, tax_tree):
        nodes = tax_tree.search_nodes(name=self.tax_id)
        if len(nodes)!=0:
            tax = nodes[0]
            self.__assignRank(tax.R, tax.N)
            while tax.up!=None:
                tax = tax.up
                self.__assignRank(tax.R, tax.N)
    
    def findMyRanksByDB(self, id_pid_map, id_rank_map, id_name_map):
        rank_id_list = []
        currid = self.tax_id
        rank_id_list.append(currid)
        while currid!="1":
            pid = id_pid_map.get(currid, "1")
            currid = pid
            rank_id_list.append(currid)
        for rid in rank_id_list:
            rk = id_rank_map[rid]
            name = id_name_map[rid]
            self.__assignRank(rk, name) 
        self.__checkRank(rank_id_list, id_rank_map, id_name_map)

class seq_db:
    def __init__(self):
        self.tax_tree = ""
        self.name_taxid_map = {}
        self.seq_list = []
    
    def __str__(self):
        str1 = ""
        for seq in self.seq_list:
            str1 = str1 + seq.__str__() + "\n"
        return str1
    
    def init_db_from_file(self, sfin):
        fin = open(sfin)
        lines = fin.readlines()
        fin.close()
        for line in lines:
            line = line.strip()
            toks = line.split("|")
            if len(toks) == 7:
                seq = sequence(seq_id = toks[0])
                seq.ranks = toks[1:]
                seq.ranks.reverse()
                self.seq_list.append(seq)
            else:
                print("incomplete rank for seq" + toks[0])
                
    def build_with_tax_tree(self, stax_tree, sname_taxid):
        self.tax_tree = Tree(stax_tree, format = 1)
        fname_taxid = open(sname_taxid)
        lines = fname_taxid.readlines()
        fname_taxid.close()
        for line in lines:
            line = line.strip()
            toks = line.split();
            self.name_taxid_map[toks[0]] = toks[1]
        
        for seqname in self.name_taxid_map.keys():
            taxid = self.name_taxid_map[seqname]
            seq = sequence(seq_id = seqname, tax_id = taxid)
            seq.findMyRanksByTree(self.tax_tree)
            self.seq_list.append(seq)
    
    def build_with_db(self, s_id_name, s_id_pid_rank, sname_taxid):
        fname_taxid = open(sname_taxid)
        lines = fname_taxid.readlines()
        fname_taxid.close()
        for line in lines:
            line = line.strip()
            toks = line.split()
            self.name_taxid_map[toks[0]] = toks[1]
        
        id_pid_map = {}
        id_rank_map = {}
        id_name_map = {}
        f_id_pid_rank = open(s_id_pid_rank)
        lines = f_id_pid_rank.readlines()
        f_id_pid_rank.close()
        for line in lines:
            line = line.strip()
            toks = line.split("|")
            id_pid_map[toks[0]] = toks[1]
            id_rank_map[toks[0]] = toks[2]
        
        f_id_name = open(s_id_name)
        lines = f_id_name.readlines()
        f_id_name.close()
        for line in lines:
            line = line.strip()
            toks = line.split("|")
            id_name_map[toks[0]] = toks[1]
        
        for seqname in self.name_taxid_map.keys():
            taxid = self.name_taxid_map[seqname]
            seq = sequence(seq_id = seqname, tax_id = taxid)
            seq.findMyRanksByDB(id_pid_map, id_rank_map, id_name_map)
            self.seq_list.append(seq)
         
    def to_file(self, sfout):
        fout = open(sfout, "w")
        for seq in self.seq_list:
            fout.write(seq.__str__() + "\n")
        fout.close()
        
    def get_seq_by_name(self, seq_name):
        for seq in self.seq_list:
            if seq.seq_id == seq_name:
                return seq
        return None    
    
    def get_all_rank_names(self):
        rk_name_set = set()
        for seq in self.seq_list:
            rks = seq.ranks
            for i, rk in enumerate(rks):
                if rk!="":
                    rk_name_set.add((rk, i))
        return rk_name_set
    
    def get_non_species_rank_names(self):
        rk_name_set = set()
        for seq in self.seq_list:
            rks = seq.ranks
            for i, rk in enumerate(rks):
                if rk!="":
                    if i!=5:
                        rk_name_set.add((rk, i))
        return rk_name_set
    
    
    def rank_stas(self, seq_list):
        """find the most abundant ranks for sequence object list"""
        rank_stas = [["",0]] * 6
        numseq = float(len(seq_list))
        for i in range(6):
            rank_num_map = {}
            for seq in seq_list:
                rkname = seq.ranks[i]
                if rkname in rank_num_map:
                    rank_num_map[rkname] = rank_num_map[rkname] + 1
                else:
                    rank_num_map[rkname] = 1
            sorted_rank_num_map = sorted(rank_num_map.iteritems(), key=operator.itemgetter(1), reverse = True)
            maxrank = list(sorted_rank_num_map[0])# = float(sorted_rank_num_map[0][1])/numseq
            maxrank[1] = float(maxrank[1]) / numseq
            rank_stas[i] = maxrank
        #rank_stas.reverse()
        #print(rank_stas)
        return rank_stas
    
    def rank_abundance(self, seq_list, rank_name, rank_num):
        num_seqs = float(len(seq_list))
        cnt = 0.0
        for seq in seq_list:
            ranks = seq.ranks
            if ranks[rank_num] == rank_name:
                cnt = cnt + 1.0
        return cnt/num_seqs

class phylogeny_annotator:
    
    def __init__(self, sphylogeny, s_seq_db, t=0.95):
        self.tree_input = sphylogeny
        self.taxonomy_file = s_seq_db
        self.threshold = t
        self.root = Tree(sphylogeny, format=1)
        self.seqs = seq_db()
        self.seqs.init_db_from_file(s_seq_db)
        self.max_rank = 5 
        rks = self.seqs.get_all_rank_names()
        self.all_rank_names = []
        for rk in rks:
            self.all_rank_names.append(rk[0])
        self.nid_freq_map = {} # nid : [[r0name, f0],[r1name, f1],...,[r5name,f5]]
        self.nid_assigned_map = {} # nid : True or False, indicate if this node rank has been fully determined
        self.nid_ranks_map = {} #  nid : [r0name, r1name, ... ,r5name]
        self.nid_ranknum_map = {} #  nid : final_rank_num
    
    def __get_child_ranks(self, internal_node, rank_num):
        """input:internal node, rank_num; output: rankname frequency map """
        leaves = internal_node.get_leaves()
        rname_cnt_map = {}
        for leaf in leaves:
                seq = self.seqs.get_seq_by_name(leaf.name)
                rank_name = seq.ranks[rank_num]
                if rank_name in rname_cnt_map:
                        rname_cnt_map[rank_name] = rname_cnt_map[rank_name] + 1
                else:
                        rname_cnt_map[rank_name] = 1 
        return rname_cnt_map
    
    def __sum_rank_num(self):
        s = 0
        for nid in self.nid_ranknum_map.keys():
            s = s + self.nid_ranknum_map[nid]
        return s
    
    def __count_miss_labled(self):
        cnt = 0
        leave = self.root.get_leaves()
        for leaf in leave:
            oriranks = self.seqs.get_seq_by_name(leaf.name).ranks
            #oriranks.reverse()
            if self.nid_ranks_map[leaf.nid] != oriranks:
                print(leaf.name)
                print("Correct:" + str(self.nid_ranks_map[leaf.nid]))
                print("Misslab:" + str(oriranks))
                cnt = cnt + 1
        return cnt
    
    def annotate_all_branches_bu(self):
        i = 0 
        n_v_map = {} # node id map to vector with probabilities,
        rank_map = {} # node id to rank number map, rank starting from 0
        for node in self.root.traverse("postorder"):
            i = i + 1
            if node.is_leaf():
                seq = self.seqs.get_seq_by_name(node.name)
                rank_num = 0
                rank_name = seq.ranks[rank_num]
                rname_cnt_map = {}
                rname_cnt_map[rank_name]=1.0
                n_v_map[i] = rname_cnt_map       
                rank_map[i] = rank_num       
                node.add_feature("nid", i)
            else:
                childs = node.get_children()
                lchild = childs[0].nid
                rchild = childs[1].nid
                #decide which rank to go
                if rank_map[lchild] == rank_map[rchild]:
                    rname_cnt_map_l = n_v_map[lchild]
                    rname_cnt_map_r = n_v_map[rchild]
                    sorted_rname_cnt_map_l = sorted(rname_cnt_map_l.iteritems(), key=operator.itemgetter(1), reverse = True)
                    sorted_rname_cnt_map_r = sorted(rname_cnt_map_r.iteritems(), key=operator.itemgetter(1), reverse = True)
                    if sorted_rname_cnt_map_l[0][0] == sorted_rname_cnt_map_r[0][0]:
                        rank = rank_map[lchild]
                    else:
                        rank = rank_map[lchild] + 1;
                    if rank > self.max_rank:
                        rank = self.max_rank
                else:
                    rank = max(rank_map[lchild], rank_map[rchild])
                    
                rname_cnt_map = self.__get_child_ranks(node, rank)
                num_leaves = sum(rname_cnt_map.values())

                for rkname in rname_cnt_map.keys():
                    if rkname == "":
                        continue
                    else:
                        rname_cnt_map[rkname] = float(rname_cnt_map[rkname])/num_leaves
           
                n_v_map[i] = rname_cnt_map
                rank_map[i] = rank
                node.add_feature("nid", i)
            
        #assigning taxa rank:
        pvalue = 0
        ch = self.root.get_children()
        self.root.add_feature("rankname", "God")
        self.root.add_feature("pv", 1) #record the max prob of each nodes
        rank_map[self.root.nid] = 666 #change this to be the max rank of childs + 1 
        while len(ch) != 0:
            maxrank = 0
            for node in ch:
                rank_num = rank_map[node.nid]
                if rank_num >= maxrank:
                    maxrank = rank_num 
                    
            high_rank_nodes = []
            for node in ch:
                rank_num = rank_map[node.nid]
                if rank_num == maxrank:
                    high_rank_nodes.append(node)
                   
            for node in high_rank_nodes:
                ch.remove(node)
                
            #process
            for node in high_rank_nodes:
                assign_flag = 0
                nodefather = node.up
                father_rank_num = rank_map[nodefather.nid]
                if father_rank_num == maxrank:
                    node.add_feature("rankname", nodefather.rankname)
                    node.add_feature("pv", nodefather.pv)
                    pvalue = pvalue + node.pv
                    #print("assigning node id: " + str(node.nid) + " with " + str(nodefather.rankname))
                    assign_flag = 1
                else:
                    rname_cnt_map = n_v_map[node.nid]
                    sorted_rname_cnt_map = sorted(rname_cnt_map.iteritems(), key=operator.itemgetter(1), reverse = True)
                    for rname_cnt in sorted_rname_cnt_map:
                        if rname_cnt[0] in self.all_rank_names:
                            node.add_feature("rankname", rname_cnt[0])
                            node.add_feature("pv", rname_cnt[1])
                            #Tomas: why we do the following in the first place? I removed it cause it is a bug in curr version 
                            #self.all_rank_names.remove(rname_cnt[0])
                            #print("assigning node id: " + str(node.nid) + " with " +rname_cnt[0])
                            assign_flag = 1
                            pvalue = pvalue + node.pv
                            break
                    
                if assign_flag == 0:
                    node.add_feature("rankname", node.up.rankname)
                    node.add_feature("pv", node.up.pv)
                    pvalue = pvalue + node.pv
                    #print("assigning node id: " + str(node.nid) + " with " +node.up.rankname)
                    
            for node in high_rank_nodes:
                ch = ch + node.get_children()
        return pvalue        
    
    def tomas(self):
        flouri = CMislabel(self.tree_input, self.taxonomy_file)
        self.root = flouri.t 
        self.nid_ranks_map = flouri.nid_ranks
        return flouri.score()
    
    def tomas_rooted(self):
        flouri = CMislabel(self.tree_input, self.taxonomy_file, self.root)
        self.nid_ranks_map = flouri.nid_rank    
    
    def assign_all_descendent_node_rank(self, node, rank_num, rank_name):
        descent_nodes = node.get_descendants()
        descent_nodes.append(node)
        find_error = False
        for nodei in descent_nodes:
            if nodei.is_leaf():
                if True: #node.is_correct == "yes":
                    seq = self.seqs.get_seq_by_name(nodei.name)
                    ranks = self.nid_ranks_map[nodei.nid]
                    ranks[rank_num] = rank_name
                    self.nid_ranks_map[nodei.nid] = ranks
                    if seq.ranks[rank_num] != rank_name:
                        nodei.add_feature("is_correct", "No")
                        find_error = True
            else:
                ranks = self.nid_ranks_map[nodei.nid]
                ranks[rank_num] = rank_name
                self.nid_ranks_map[nodei.nid] = ranks
        if find_error:
            #recalculate all frequency vectors
            seq_util = seq_db()
            for nodei in node.traverse(strategy = "preorder"):
                leaves = nodei.get_leaves()
                seqs = []
                for leaf in leaves:
                    seqs.append(self.seqs.get_seq_by_name(leaf.name))
                    freq_table = seq_util.rank_stas(seqs)
                    self.nid_freq_map[nodei.nid] = freq_table
    
    def annotate_all_branches_td(self):
        self.nid_freq_map = {} # nid : [[r0name, f0],[r1name, f1],...,[r5name,f5]]
        self.nid_assigned_map = {} # nid : True or False, indicate if this node rank has been fully determined
        self.nid_ranks_map = {} #  nid : [r0name, r1name, ... ,r5name]
        self.nid_ranknum_map = {} #  nid : final_rank_num
        all_leaves = self.root.get_leaves()
        for leaf in all_leaves:
            leaf.add_feature("is_correct", "yes")
        #traversal the tree to calculate the frequence profile for each node/branch
        seq_util = seq_db()
        i = 0
        for node in self.root.traverse(strategy = "preorder"):
            i = i + 1
            node.add_feature("nid", i)
            self.nid_assigned_map[i] = False
            ranks = ["-"] * 6
            self.nid_ranks_map[i] = ranks
            leaves = node.get_leaves()
            seqs = []
            for leaf in leaves:
                seqs.append(self.seqs.get_seq_by_name(leaf.name))
            freq_table = seq_util.rank_stas(seqs)
            self.nid_freq_map[i] = freq_table
        
        #traversal the tree preorder
        for node in self.root.traverse(strategy = "preorder"):
            freq_table = self.nid_freq_map[node.nid]
            ranks = self.nid_ranks_map[node.nid]
            assigning_rank_idx = 0
            if node.is_root():
                self.nid_ranknum_map[node.nid] = -1
            else:
                next_rank_idx = self.nid_ranknum_map[node.up.nid] + 1
                flag = True
                while flag:
                    if next_rank_idx < 6:
                        rk_freq = freq_table[next_rank_idx]
                        if rk_freq[1] == 1.0:
                            self.assign_all_descendent_node_rank(node, next_rank_idx, rk_freq[0])
                            #curr_rank_idx = curr_rank_idx + 1
                            next_rank_idx = next_rank_idx + 1
                        else:
                            childs = node.get_children()
                            lchild = childs[0]
                            rchild = childs[1]
                            lfreq_table = self.nid_freq_map[lchild.nid]
                            rfreq_table = self.nid_freq_map[rchild.nid]
                            lrk_freq = lfreq_table[next_rank_idx]
                            rrk_freq = rfreq_table[next_rank_idx]
                            if rk_freq[1] < lrk_freq[1] and rk_freq[1] < rrk_freq[1]:
                                flag = False
                            else: #should check all possibilties here 
                                if lrk_freq[0] == rrk_freq[0] and rk_freq[1]>self.threshold:
                                    self.assign_all_descendent_node_rank(node, next_rank_idx, rk_freq[0])
                                    next_rank_idx = next_rank_idx + 1
                                else:
                                    flag = False
                    else:
                        #assign taxonomy to species level
                        assigning_rank_idx = 5
                        rk_freq = freq_table[assigning_rank_idx]
                        flag = False
                        ranks[assigning_rank_idx] = rk_freq[0]
                self.nid_ranknum_map[node.nid] = next_rank_idx - 1
            self.nid_assigned_map[node.nid] = True
        return self.__sum_rank_num()
    
    def show_tree_with_rank(self):
        allnodes = self.root.get_descendants()
        for node in allnodes:
            #rk_num = rank_map[node.nid]
            #node.add_feature("rank_num", rk_num )
            ranks = self.nid_ranks_map[node.nid]
            node.add_face(TextFace(str(ranks)), column=0, position = "branch-right")
            if node.is_leaf():
                seq = self.seqs.get_seq_by_name(node.name)
                rk = seq.ranks
                #rk.reverse()
                node.add_face(TextFace(str(rk)), column=0, position = "branch-right")
        self.root.show()
    
    def rooting_by_outgroup_names(self, outgroup_names):
        all_leaves = self.root.get_leaves()
        sog_names = set(outgroup_names)
        ca1 = self.root
        #Traversal all nodes to find the common ancestor of the input outgroup_names
        for node in self.root.traverse():
            currleaves = node.get_leaves()
            currlnames = []
            for lv in currleaves:
                currlnames.append(lv.name)
            scurrnames = set(currlnames)
            if scurrnames == sog_names:
                ca1 = node
            break
        #Check if the found ca is the root, if yes, find the complmentary names of the tree
        if ca1!=self.root:
            self.root.set_outgroup(ca1)
        else:
            restnodes = []
            for leaf in all_leaves:
                if leaf.name not in sog_names:
                    restnodes.append(leaf.name)
            srestnodes = set(restnodes)
            for node in self.root.traverse():
                currleaves = node.get_leaves()
                currlnames = []
                for lv in currleaves:
                    currlnames.append(lv.name)
                scurrnames = set(currlnames)
                if scurrnames == srestnodes:
                    self.root.set_outgroup(node)
                    break
    
    def annotate_td(self):
        #find all bipartations:
        list_bipar = []
        #all_leaves = self.root.get_leaves()
        for node in self.root.traverse("postorder"):
            if not node.is_root():
                leaves = node.get_leaves()
                leave_names = []
                for leaf in leaves:
                    leave_names.append(leaf.name) 
                list_bipar.append(leave_names)
        
        #find the root:
        maxpv=0
        maxbipar = None
        for bipar in list_bipar:
            #Search the current tree to find the partitions:
            Node0 = self.root.search_nodes(name = bipar[0])[0]
            if len(bipar) == 1:
                self.root.set_outgroup(Node0)
            else:
                self.rooting_by_outgroup_names(bipar)
            pvalue = self.annotate_all_branches_td()
            print(pvalue)
            misscnt = self.__count_miss_labled()
            print(misscnt)
            if pvalue > maxpv:
                maxpv = pvalue
                maxbipar = bipar
        self.rooting_by_outgroup_names(maxbipar)
        self.annotate_all_branches_td()
        misscnt = self.__count_miss_labled()
        print(misscnt)
    
    def annotate_bu(self):
        """rooting and output"""
        #find all bipartations:
        list_bipar = []
        #all_leaves = self.root.get_leaves()
        for node in self.root.traverse("postorder"):
            if not node.is_root():
                leaves = node.get_leaves()
                leave_names = []
                for leaf in leaves:
                    leave_names.append(leaf.name) 
                list_bipar.append(leave_names)
                
        maxpv=0
        maxbipar = None
        for bipar in list_bipar:
            #Search the current tree to find the partitions:
            Node0 = self.root.search_nodes(name = bipar[0])[0]
            if len(bipar) == 1:
                self.root.set_outgroup(Node0)
            else:
                self.rooting_by_outgroup_names(bipar)
            
            pvalue = self.tomas()
            if pvalue > maxpv:
                maxpv = pvalue
                maxbipar = bipar 
                                    
        self.rooting_by_outgroup_names(maxbipar)
        self.tomas_rooted()
        # draw the tree      
        allnodes = self.root.get_descendants()
        for node in allnodes:
            #rk_num = rank_map[node.nid]
            #node.add_feature("rank_num", rk_num )
            if hasattr(node, 'rankname'):
                node.add_face(TextFace(node.rankname), column=0, position = "branch-right")
                #node.add_face(TextFace(node.rank_num), column=0, position = "branch-right")
        #self.root.show()
    
    def correct_leaf_ranks(self):
        leaves = self.root.get_leaves()
        for leaf in leaves:
            if not leaf.is_root():
                father = leaf.up
                lranks = self.nid_ranks_map[leaf.nid]
                franks = self.nid_ranks_map[father.nid]
                lsp = lranks[5]
                for i, rk in enumerate(franks):
                    lranks[i] = rk
                lranks[5] = lsp 
                self.nid_ranks_map[leaf.nid] = lranks

class epa_parser:
    def __init__(self, splacement_json, hasTaxonomy = False, sncbi_taxonomy = None, threshold=0.9):
        self.staxonomy = sncbi_taxonomy
        self.god = None
        fin = open(splacement_json)
        self.jdata = json.load(fin)
        fin.close()
        self.placements = self.jdata["placements"] #each placement is a map with two keys: 'n' - sequence name and 'p' - the placement info vector
        #each placement info vector has 5 fields, position 0 is the branch name, position 2 is the likelihood weight
        self.tree = self.jdata["tree"]
        self.tree = self.tree.replace("{", "[&&NHX:B=")
        self.tree = self.tree.replace("}", "]")
        if hasTaxonomy:
            self.bid_taxonomy_map = self.jdata["taxonomy"]
            self.leafid_taxonomy_map = self.jdata["original_taxonomy"]
        else:
            self.god = phylogeny_annotator(self.tree, sncbi_taxonomy, threshold)
        if self.god != None:
            self.seqs = self.god.seqs
        elif sncbi_taxonomy != None:
            self.seqs = seq_db()
            self.seqs.init_db_from_file(sncbi_taxonomy)
            
    def annotate_phylogeny(self, method = "1", output = ""):
        if method == "1": #max-likelihood top down approach by Jiajie 
            self.god.annotate_td()
            self.god.correct_leaf_ranks()
            if output!="":
                self.dump_taxonomy(output)
            else:
                self.god.show_tree_with_rank()
        elif method == "2":#something bottom up approach by Tomas
            #tomas = CMislabel(self.tree, self.staxonomy)
            #pa = phylogeny_annotator(self.tree, self.staxonomy)
            #pa.root = tomas.t
            #pa.nid_ranks_map = tomas.nid_ranks
            #self.god = pa
            self.god.annotate_bu()
            if output!="":
                self.dump_taxonomy(output)
            else:
                self.god.show_tree_with_rank()
    
    def dump_taxonomy(self,sfout):
        nid_ranks_map = self.god.nid_ranks_map
        print(nid_ranks_map)
        bid_ranks_map = {}
        leaf_ranks_map = {} 
        for node in self.god.root.traverse("postorder"):
            #ranks = nid_ranks_map[node.nid]
            ranks = nid_ranks_map.get(node.nid, ["-", "-", "-", "-", "-","-"])
            #print rootnode
            if hasattr(node, "B"):
                bid = node.B
                bid_ranks_map[bid] = ranks
                if node.is_leaf():
                    leaf_ranks_map[bid] = self.seqs.get_seq_by_name(node.name).ranks
        self.jdata["taxonomy"] = bid_ranks_map
        self.jdata["original_taxonomy"] = leaf_ranks_map
        self.bid_taxonomy_map = bid_ranks_map
        fout = open(sfout, "w")
        json.dump(self.jdata, fout)
    
    def sum_lw_in_rank(self, rank_num, rank_name, e_lw_map):
        lwsum = 0.0
        #all_nodes = self.god.root.get_descendants()
        #print("checking rank num: " + repr(rank_num) + " rank name:" + rank_name)
        if rank_name == "" or rank_name == "-":
            return 0.0
        else:
            for bid in self.bid_taxonomy_map.keys():
                if self.bid_taxonomy_map[bid][rank_num] == rank_name:
                    lw = e_lw_map[int(bid)]
                    lwsum = lwsum + lw
            #for node in all_nodes:
            #    if self.god.nid_ranks_map[node.nid][rank_num] == rank_name:
            #        if hasattr(node, "B"):
            #            lw = e_lw_map[int(node.B)]
            #            lwsum = lwsum + lw
            return lwsum
    
    def placement_stas(self, p):
        seq_name = p['n'][0]
        place_vectors = p['p']
        edge_lw_map = {}
        for pv in place_vectors:
            edge_lw_map[pv[0]] = pv[2]
        #print(edge_lw_map)
        seq = self.seqs.get_seq_by_name(seq_name)
        human_ranks = seq.ranks
        lw_per_rank = []
        for i, rank in enumerate(human_ranks):
            lw_per_rank.append(self.sum_lw_in_rank(rank_num=i, rank_name=rank, e_lw_map = edge_lw_map))
        
        print(seq_name)
        print("Original taxonomy lables:            " +  human_ranks[0] + ">" + human_ranks[1] + ">"  + human_ranks[2] + ">"  + human_ranks[3] + ">"  + human_ranks[4] + ">"  + human_ranks[5])
        print("LH-weight for each rank:" + str(lw_per_rank))
        return human_ranks, lw_per_rank
    
    def exam_all_placements(self):
        for place in self.placements:
            h_ranks, h_lws = self.placement_stas(place)
            b_ranks, b_lws, bestplace_bid = self.find_most_likely_ranks(place)
            flag = self.check_for_mislabels(h_ranks, h_lws, b_ranks, b_lws)
            if flag:
                print("Potential misslabeled!!")
                self.calculate_mislabels_distance(h_ranks, bestplace_bid)
            print("----------------------------------------------------------------------------------------------------------------------")
    
    def find_most_likely_ranks(self, p):
        #seq_name = p['n'][0]
        place_vectors = p['p']
        edge_lw_map = {}
        for pv in place_vectors:
            edge_lw_map[pv[0]] = pv[2]
        bestplace_bid = place_vectors[0][0]
        bestranks = self.bid_taxonomy_map[str(bestplace_bid)]
        lw_per_rank = []
        for i, rank in enumerate(bestranks):
            lw_per_rank.append(self.sum_lw_in_rank(rank_num=i, rank_name=rank, e_lw_map = edge_lw_map))
        
        print("Best EPA placement taxonomy lables:    " +  bestranks[0] + ">" + bestranks[1] + ">"  + bestranks[2] + ">"  + bestranks[3] + ">"  + bestranks[4] + ">"  + bestranks[5])
        print("LH-weight for each rank:" + str(lw_per_rank))
        if str(bestplace_bid) in self.leafid_taxonomy_map:
            ori_ranks = self.leafid_taxonomy_map[str(bestplace_bid)]
            print("Best EPA placement on leaf:    " + ori_ranks[0] + ">" + ori_ranks[1] + ">"  + ori_ranks[2] + ">"  + ori_ranks[3] + ">"  + ori_ranks[4] + ">"  + ori_ranks[5])
            leaf_lw = edge_lw_map[bestplace_bid]
            print("Best EPA placement on leaf has LH-weight:    " + str(leaf_lw))
        return bestranks, lw_per_rank, str(bestplace_bid)
    
    def check_for_mislabels(self, human_ranks, human_lws, best_ranks, best_lws):
        error_flag = False
        for i, human_rank in enumerate(human_ranks):
            human_lw = human_lws[i]
            best_rank = best_ranks[i]
            best_lw = best_lws[i]
            if (human_rank != best_rank) and best_lw > human_lw:
                error_flag = True
                break
        return  error_flag
    
    def calculate_mislabels_distance(self, human_ranks, bestplace_bid):
        t = Tree(self.tree, format = 1)
        bestnode = t.search_nodes(B=bestplace_bid)[0]
        #print("Best node: " + str(bestnode))
        #find all nodes that match the original labels 
        distance = []
        node_distance = []
        for i, rank in enumerate(human_ranks):
            curr_rank_nodes = []
            for bid in self.bid_taxonomy_map.keys():
                curr_ranks = self.bid_taxonomy_map[bid]
                if curr_ranks[i] == rank:
                    if i == 5:
                        curr_rank_nodes.append(t.search_nodes(B=str(bid))[0])
                    else:
                        #if curr_ranks[i+1] == "-":
                        curr_rank_nodes.append(t.search_nodes(B=str(bid))[0])
            num_nodes = float(len(curr_rank_nodes))
            sumdis = 0.0
            sumnodedis = 0.0
            if num_nodes!=0.0:
                for node in curr_rank_nodes:
                    sumdis = sumdis + bestnode.get_distance(node)
                    sumnodedis = sumnodedis + bestnode.get_distance(node,  topology_only=True)
                distance.append(sumdis/num_nodes)
                node_distance.append(sumnodedis/num_nodes)
            else:
                distance.append(0.0)
                node_distance.append(0.0)
        print("Average distance from best EPA-placement to original labeled ranks: \n        " + str(distance))
        print("Average node distance from best EPA-placement to original labeled ranks: \n        " +str(node_distance))
        return distance, node_distance

class ncbi_taxa:
    
    def __init__(self):
        self.__tax_tree_root=None
        self.__id_name_map = {}
        self.__id_rank_map = {}
    
    def init_tax_tree(self, sftree, sfname, sfrank):
        self.__tax_tree_root = Tree(sftree, format=8)
        fname = open(sfname)
        frank = open(sfrank)
        
        lines = fname.readlines()
        for line in lines:
            line = line.strip()
            items = line.split("|")
            self.__id_name_map[items[0]]=items[1]
        fname.close()
        
        lines = frank.readlines()
        for line in lines:
            line = line.strip()
            items = line.split("|")
            self.__id_rank_map[items[0]]=items[2]
        frank.close()
    
    def extract_sub_tax_tree(self, sname_tax, sfout):
        seqname_taxid_map = {}
        taxid = []
        fname_tax = open(sname_tax)
        lines = fname_tax.readlines()
        for line in lines:
            line = line.strip()
            items = line.split()
            seqname_taxid_map[items[0]]=items[1]
            taxid.append(items[1])
        fname_tax.close()
        self.__tax_tree_root.prune(taxid)
        
        #annotate all nodes for ranks and names
        rootid = self.__tax_tree_root.name
        rootname = self.__id_name_map.get(rootid, "noNCBIname")
        rootname = rootname.replace(" ", "_")
        rootrank = self.__id_rank_map.get(rootid, "noNCBIrank")
        rootrank = rootrank.replace(" ", "_")
        self.__tax_tree_root.add_feature("N", rootname)
        self.__tax_tree_root.add_feature("R", rootrank)
        
        
        allnodes = self.__tax_tree_root.get_descendants()
        for node in allnodes:
            nodeid = node.name
            nodename = self.__id_name_map.get(nodeid, "noNCBIname")
            noderank = self.__id_rank_map.get(nodeid, "noNCBIrank")
            nodename = nodename.replace(" ","_")
            noderank = noderank.replace(" ","_")
            node.add_feature("N", nodename)
            node.add_feature("R", noderank)
            
        self.__tax_tree_root.write(outfile=sfout, format=8, features=["N","R"])
        print(self.__tax_tree_root)

class leave_one_test:
    """This class will do a leave one test on every sequence in the alignment"""
    def __init__(self, salignment, stree, staxonomy):
        self.salign = salignment
        self.stre = stree
        self.taxonomy = staxonomy
        self.tree = Tree(stree)
        self.alignment = SeqGroup(sequences=salignment, format='phylip_relaxed')
        
    
    def prune_one_tax(self, taxa_name):
        #self.tree.delete(taxa_name)
        #target_node = self.tree.search_nodes(name = taxa_name)
        self.tree.prune([taxa_name])
        self.tree.write(outfile = taxa_name + ".tre", format = 5)
        jsonfile = self.run_epa(newtree = taxa_name + ".tre")
        epar = epa_parser(splacement_json= jsonfile, sncbi_taxonomy = self.taxonomy)
        epar.annotate_phylogeny(method = "1", output = jsonfile + ".m1" )
        epp2 = epa_parser(splacement_json = jsonfile + ".m1", sncbi_taxonomy = "self.taxonomy", hasTaxonomy = True)
        epp2.exam_all_placements()
        
    
    def run_epa(self, newtree):
        # -s test.phy -t olaf_full.tre -n test -f v -m GTRGAMMA
        call(["./raxmlHPC-SSE3","-m","GTRGAMMA","-f", "v","-s",self.salign,"-n",newtree,"-t", newtree])
        os.remove("RAxML_classificationLikelihoodWeights." + newtree)
        os.remove("RAxML_entropy." + newtree)
        os.remove("RAxML_labelledTree." + newtree)
        os.remove("RAxML_classification." + newtree)
        os.remove("RAxML_info." + newtree)
        os.remove("RAxML_originalLabelledTree." + newtree)
        return "RAxML_portableTree." + newtree + ".jplace" 
    
    def find_errors(self):
        for seq in self.alignment:
            self.tree = Tree(self.stre)
            seqname = seq[0]
            self.prune_one_tax(seqname)

if __name__ == "__main__":
        if len(sys.argv) != 6: 
            print("usage: ./ncbi_taxonomy.py <tree_of_life.tre> <id_name.txt> <id_rank.txt> <name_tax.txt> <outputfile>")
            sys.exit()
        t = ncbi_taxa()
        t.init_tax_tree(sys.argv[1], sys.argv[2], sys.argv[3])
        t.extract_sub_tax_tree(sys.argv[4], sys.argv[5])
