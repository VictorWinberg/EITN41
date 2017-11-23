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

target_adress, mix_adress, m = input(), input(), int(input())

packets = [ {
    'src': get_ip_src(pkt),
    'dst': get_ip_dst(pkt)}
    for pkt in capfile.packets
]

batches = []
prevMix = 1

for packet in packets:
    isMix = int(packet['src'] == mix_adress)
    if(prevMix != isMix): batches.append([])

    p = [ packet['src'], packet['dst'] ]
    batches[-1].append(p[isMix])

    prevMix = isMix
    # print ('{}\t{}'.format(packet['src'], packet['dst']))

batches = list(zip(batches[::2], batches[1::2]))
R_all = []

for batch in batches:
    src, dst = batch
    if target_adress in src:
        R_all.append(dst)

R_disjoint = [ set(R_all[0]) ]
for R_i in R_all:
    if all(set(R_i).isdisjoint(R_j) for R_j in R_disjoint):
        R_disjoint.append(set(R_i))

R_rest = [ set(R) for R in R_all if set(R) not in R_disjoint ]

for R in R_rest:
    for i, R_i in enumerate(R_disjoint):
        R_i_disjoint = R & R_i == set()
        R_j_disjoint = [R & R_j == set() for j, R_j in enumerate(R_disjoint) if i != j]
        if not R_i_disjoint and all(R_j_disjoint):
            R_disjoint[i] &= set(R)

R_disjoint = list(set().union(*R_disjoint))
print('m:', m, ', found:', len(R_disjoint), 'of', len(R_all))

print(sum(map(ipadress_to_int, R_disjoint)))
