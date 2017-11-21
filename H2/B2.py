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

nazir_adress, mix_adress, partners = input(), input(), int(input())

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
    print ('{}\t{}'.format(packet['src'], packet['dst']))

group_batch = list(zip(batch[::2], batch[1::2]))
nazir_batch = []

for group in group_batch:
    src, dst = group
    if nazir_adress in src:
        nazir_batch.append(dst)

# chain_batch = list(chain(*nazir_batch))
# count_batch = [ (chain_batch.count(x), x) for x in set(chain_batch) ]
# sort_batch = sorted(count_batch)[::-1]
#
# print(sort_batch[:partners])
# print('# of messages', len(nazir_batch))
#
# print(sum(map(ipadress_to_int, [ x[1] for x in sort_batch[:partners] ])))
