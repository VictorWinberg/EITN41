from functools import reduce
from pcapfile import savefile
from itertools import chain

def get_ip_src(pkt):
    return pkt.packet.payload.src.decode('UTF8')

def get_ip_dst(pkt):
    return pkt.packet.payload.dst.decode('UTF8')

def ipadress_to_int(ipadress):
    return reduce(lambda x, y: int(x) << 8 | int(y), ipadress.split('.'))

testcap = open(input(), 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

nazir_adress, mix_adress, m = input(), input(), int(input())

packets = [ {
    'src': get_ip_src(pkt),
    'dst': get_ip_dst(pkt)}
    for pkt in capfile.packets
]

batch = []
prevMix = 1

for packet in packets:
    isMix = int(packet['src'] == mix_adress)
    if(prevMix != isMix):
        batch.append([])

    p = [ packet['src'], packet['dst'] ]
    batch[-1].append(p[isMix])

    prevMix = isMix
    # print ('{}\t{}'.format(packet['src'], packet['dst']))

group_batch = list(zip(batch[::2], batch[1::2]))
nazir_batch = []

for group in group_batch:
    src, dst = group
    if nazir_adress in src:
        nazir_batch.append(dst)

disjoint_batch = [ set(nazir_batch[0]) ]
for batch in nazir_batch:
    if all(set(batch).isdisjoint(disjoint) for disjoint in disjoint_batch):
        disjoint_batch.append(set(batch))

joint_batch = [set(batch) for batch in nazir_batch if set(batch) not in disjoint_batch]
for suspects in disjoint_batch:
    for innocents in joint_batch:
        for blameless in suspects.intersection(innocents):
            suspects.remove(blameless)

print(len(disjoint_batch), disjoint_batch)

# print(sum(map(ipadress_to_int, disjoint_batch)))
