from __future__ import print_function
import sim

print('========jaccard============')
print(sim.code_sim('codes/code1.py', 'codes/code2.py', 'jaccard'))
print(sim.code_sim('codes/code1.py', 'codes/code3.py', 'jaccard'))
print(sim.code_sim('codes/code2.py', 'codes/code4.py', 'jaccard'))

print('========tree edit============')
print(sim.code_sim('codes/code1.py', 'codes/code2.py',  'tree_edit'))
print(sim.code_sim('codes/code1.py', 'codes/code3.py',  'tree_edit'))
print(sim.code_sim('codes/code2.py', 'codes/code4.py',  'tree_edit'))

print('========fake anti unification============')
print(sim.code_sim('codes/code1.py', 'codes/code2.py', 'fake_anti_uni'))
print(sim.code_sim('codes/code1.py', 'codes/code3.py', 'fake_anti_uni'))
print(sim.code_sim('codes/code2.py', 'codes/code4.py', 'fake_anti_uni'))
