import pprint
#pprint.pprint(table)

o2 = open("data/test.s","w")
o2.write(".text\n")

import ctypes #import c_uint32
import struct
f = open("i386-opc.tbl")
table = {}
c = 0
import binascii

def addopecode(name,c,v,v2):
    v3 = binascii.unhexlify(v2)
    f2 = "test_%s" % (name.replace("-","_").replace(".","_") + v + "_" + str(c))
    f3 = "data/"+f2 + ".dat"
    o2.write("%s :\n" % (f2))
    o2.write(".incbin \"%s\"\n" % f3)
    o = open(f3,"wb")
    o.write(v3)
    # pad the rest with zeros 
    b2 = (0).to_bytes(8-len(v2), byteorder='little')
    o.write(b2)
    o.close()

for x in f.readlines():
    x = x.rstrip()
    if x.startswith("//"):
        continue
    a = x.split(",")
    c = c + 1
    if len(a) > 3:
        v = a[2].rstrip().lstrip()
        name = a[0]
        #table[v]=a[0]

        ex=eval(a[3]) # extention opcode
        operands=eval(a[1])
        length=eval(a[4])

        v2 = v[2:] # strip off the 0x
        if (len(v2) % 2) != 0 : # pad with zeros to make even number
            addopecode(name,str(c)+"a",v,"0"+v2)
            addopecode(name,str(c)+"b",v,v2 + "0")
        else:
            addopecode(name,str(c)+"c",v,v2)

o2.write(".end\n")
o2.close()
f.close()
