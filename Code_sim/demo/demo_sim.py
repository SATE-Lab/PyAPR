from __future__ import print_function
from Code_sim.demo import sim


# def code_sim():
print('========jaccard============')
# print(sim.code_sim('./Code_sim/demo/codes/code3.py', './Code_sim/demo/codes/code4.py', 'jaccard'))
# print(sim.code_sim('codes/code1.py', 'codes/code2.py', 'jaccard'))
print(sim.code_sim('codes/code3.py', 'codes/code4.py', 'jaccard'))

print('========tree edit============')
# print(sim.code_sim('./Code_sim/demo/codes/code3.py', './Code_sim/demo/codes/code4.py', 'tree_edit'))
# print(sim.code_sim('codes/code1.py', 'codes/code2.py', 'tree_edit'))
print(sim.code_sim('codes/code3.py', 'codes/code4.py', 'tree_edit'))

print('======fake anti unification==')
# print(sim.code_sim('./Code_sim/demo/codes/code3.py', './Code_sim/demo/codes/code4.py', 'fake_anti_uni'))
# print(sim.code_sim('codes/code1.py', 'codes/code2.py', 'fake_anti_uni'))
print(sim.code_sim('codes/code3.py', 'codes/code4.py', 'fake_anti_uni'))
