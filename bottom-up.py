#!/usr/bin/python
import sys, operator
from ete2 import Tree, TreeStyle, TextFace


def init_ranks (rank_file):
  ranklist = open(rank_file).readlines();

  ranklist = map (lambda s: s.strip(),    ranklist)  # strip whitespaces and \n from strings
  ranklist = map (lambda s: s.split('|'), ranklist)  # split it A|B|..|Z to [A,B,...,Z]
  ranklist = map (lambda x: map (lambda y: '-' if y == '' else y, x), ranklist) # substitute '' with '-'

  rl_len = len (ranklist[0])
  rankdict = {}
  for x in ranklist: rankdict[x[0]] = x[1:]
  print(rankdict)
  return (rankdict, rl_len)

def tree_comp_freq (t, rankdict):
  correctness = {}

  nid = 0
  for v in t.traverse (strategy = "postorder"):
    freqs = {}

    # if current node is a leaf assign a rank of 0 and place the first rank in the list
    if v.is_leaf():
      rank = 0
      #freqs[rankdict[v.name][rank]] = 1.0
      freqs_sorted = [ (rankdict[v.name][rank],1.0)]
      v.add_feature("rank", rank)
      v.add_feature("freqs", freqs_sorted)
      correctness[v.name] = 1.0
      #print freqs_sorted
    
    # if current node is an internal node then it's rank is
    #    1) children_rank + 1 : if both children have the same rank, or
    #    2) max (children_ranks)
    # 
    else:
      children = v.get_children()
      ranklist = [u.rank for u in children]
      if ranklist[0] == ranklist[1]:
        v.add_feature("rank", ranklist[0] + 1)
      else:
        v.add_feature("rank", max(ranklist))

      leaves     = v.get_leaves()
      leaf_names = v.get_leaf_names()
      
      factor  = sum (correctness[key] for key in correctness if key in leaf_names)

      # compute frequencies of ranks based on the correctness of each leaf
      nLeaves = len(leaves)
      freqs = {}
      for u in leaves:
        key = rankdict[u.name][v.rank]
        if key in freqs:
          freqs[key] = freqs[key] + correctness[u.name]
        else:
          freqs[key] = correctness[u.name]

      # compute correctness weight
      for u  in leaves:
        key = rankdict[u.name][v.rank]
        correctness[u.name] = freqs[key] / factor 

      for key in freqs:
        freqs[key] = freqs[key] / factor

#      for elm in freqs:
#        freqs[elm] = freqs[elm] / float(nLeaves)
      freqs_sorted = sorted(freqs.iteritems(), key = operator.itemgetter(1), reverse = True)
      v.add_feature("freqs", freqs_sorted)
    # if v.name == "I": return
    v.add_feature ("nid", nid)
    nid = nid + 1
  return (t, correctness)

def assign_ranks (t, rankdict, correctness):
  nodes =  [v for v in t.get_tree_root().traverse (strategy = "preorder")][0:]
  root = t.get_tree_root()
  for v in nodes:
    freqs_len = len (v.freqs)
    if freqs_len == 0:
      if v == root:
        root.add_feature ("rankname", "-")
      else:
        v.add_feature ("rankname", v.up.rankname)
    else:
      if freqs_len > 1 and v.freqs[0][1] == v.freqs[1][1]:
        i = 1
        candidate_ranks = [ v.freqs[0][0] ]
        while i < freqs_len and v.freqs[0][1] == v.freqs[i][1]:
          candidate_ranks.append (v.freqs[i][0])
          i = i + 1
        leaves = v.get_leaf_names()
        candidate_nodes = [u for u in leaves if rankdict[u][v.rank] in candidate_ranks]
        prob = -1 
        for u in candidate_nodes:
          if correctness[u] > prob:
            best = u
            prob = correctness[u]
        v.add_feature ("rankname", rankdict[best][v.rank])
      else:
        v.add_feature ("rankname", v.freqs[0][0])

def print_ranks (t, rankdict, ranks_len):
  root = t.get_tree_root()
  first_elm = rankdict[rankdict.keys()[0]]
  z = first_elm[root.rank + 1:]

  z.reverse()
  z = z + [root.rankname]
  root.add_feature("rankseq",z )     # TODO: fix this with
  nodes = [v for v in root.traverse (strategy = "preorder")][1:]

  for v in nodes:
    x = [u for u in v.up.rankseq]
    if v.rank == v.up.rank:
      if x[-1] != v.rankname:
        print "CONFLICTING RANKS.. selecting the highest]"
    else:
      x = x + [ '-' for c in range (v.up.rank - v.rank - 1)]
      x.append(v.rankname)
    v.add_feature ("rankseq", x)
    if v.nid == 236:
      print v.rank
      print v.rankname
      print v.name
      print ranks_len
      print v.up.rankseq
      print root.rankseq
      print root.rank
    print str (v.nid) + " : " + str (x + ['-' for x in range(ranks_len - (ranks_len - v.rank))] ) 


if __name__ == "__main__":
#  if len(sys.argv) != 6:
#    print ("usage: ./script <tree_of_life> <id_name> <id_rank> <name_tax> <outputfile>
#    sys.exit()

  t = Tree ('reference_tree.newick', format = 1)
  #print t

  ret = init_ranks ('ola_db3.txt')
  rankdict  = ret[0]
  ranks_len = ret[1]

  ret = tree_comp_freq(t, rankdict)

  t = ret[0]
  correctness = ret[1]
  
  assign_ranks (t, rankdict, correctness)
  #print_ranks(t, rankdict, ranks_len)

  #t.show()

