#! /usr/bin/env python
from ete2 import Tree, TreeStyle, TextFace
from ncbi_taxonomy import sequence
from ncbi_taxonomy import seq_db
from ncbi_taxonomy import phylogeny_annotator
from ncbi_taxonomy import epa_parser, leave_one_test
import json

#seq = sequence(seq_id="1", tax_id="360663")
#t = Tree("output3.txt", format = 1)
#seq.findMyRanksByTree(t)
#print(seq)

#sdb = seq_db()
#sdb.build_with_tax_tree("output3.txt", "taxalist.txt")
#sdb.build_with_db(s_id_name="clean_names.txt", s_id_pid_rank="clean_nodes.txt", sname_taxid="taxalist.txt")
#sdb.to_file("ola_db3.txt")


#sdb2 = seq_db()
#sdb2.init_db_from_file("test.db.txt")
#print(sdb2.get_non_species_rank_names())
#sdb2.rank_stas(sdb2.seq_list)
#sdb2.findLCR(sdb2.seq_list)
#print(sdb2)

#t = Tree("reference_tree.newick", format=1)
#t = Tree("output3.txt", format = 1)
#print(t)
#print(t.dist)
#print(t.features)
#t.add_feature("B", "r1f1")

"""
allnodes = t.get_descendants()
for node in allnodes:
    if hasattr(node, 'R'):
        node.add_face(TextFace(node.R), column=0, position = "branch-right")
    if hasattr(node, 'N'):
        node.add_face(TextFace(node.N), column=1, position = "branch-right")
t.show()
"""

#print(t.features)
#print(t.children[0].features)
#print(t.children[0].B)
#tt = Tree("test.tree.tre", format = 1)
#print(tt)
#tt.show()

#pa = phylogeny_annotator("test.tree.tre", "test.db.txt", t=0.7)
#pa = phylogeny_annotator("reference_tree.newick", "ola_db3.txt", t=0.7)
#pa.annotate_all_branches_bu()
#pa.annotate_all_branches_td()
#pa.annotate_td()
#pa.correct_leaf_ranks()
#pa.correct_for_non_species_ranks()
#pa.show_tree_with_rank()
#pa = phylogeny_annotator("reference_tree.newick", "ola_db3.txt")

#pa.annotate_all_branches()
#pa.findNewRankFromAnnotatedTree()
#pa.annotate()
#pa.findNewRankFromAnnotatedTree()
#epp = epa_parser(tree_of_life = pa, splacement_json = "RAxML_portableTree.EPA_ALLENTRIES.jplace")
#epp.exam_all_placements()
#epp.dump("jsonout.txt")
#epp = epa_parser(splacement_json = "RAxML_portableTree.EPA_ALLENTRIES.jplace", sncbi_taxonomy = "ola_db3.txt")
#epp.annotate_phylogeny(method = "2", output = "olaf3.jplace")

#epp2 = epa_parser(splacement_json = "olaf3.jplace", sncbi_taxonomy = "ola_db3.txt", hasTaxonomy = True)
#epp2.exam_all_placements()

#d = json.load(open("jsonout.jplace"))
#bid_tax_map = d["taxonomy"]
#print(d["tree"])
#for bid in bid_tax_map.keys():
#    print(bid_tax_map[bid])
lot = leave_one_test(salignment= "olaf_full.phylip", stree = "olaf_full.tre", staxonomy = "ola_db3.txt")
lot.find_errors()

