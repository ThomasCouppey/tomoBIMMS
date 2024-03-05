import tobi
import numpy as np

ptest = [((1, 2), (3, 4)),
((1, 2), (4, 5)),
((1, 2), (5, 6)),
((1, 3), (2, 4)),]

p1 = tobi.protocol()
p1.add_patern(inj=(1,2), rec=(3,4))
p1.add_patern(rec=(4,5))
p1.add_patern(rec=(5,6))
p1.add_patern(inj=(1,3), rec=(2,4))

print(p1[1] == ((1, 2), (4, 5)))
for i, p in enumerate(p1):
    print(p == ptest[i])

p2 = tobi.simple_injection_protocol()
for p in p2:
    print(p)

p2.set_parameters(n_elec=16)
print(len(p2)== 16*(16-3))
for p in p2:
    print(p)

print()

p2.set_parameters(n_elec=8)
p2.change_electrode_id(0, 8)
for p in p2:
    print(p)


p2 = tobi.simple_injection_protocol(n_elec = 8,inj_offset=1)
p2 *= 2
p2 -= 1

for p in p2:
    print(p)