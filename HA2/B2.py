from functools import reduce
from pcapfile import savefile
from itertools import chain

def ipadress_to_int(ipadress):
    return reduce(lambda x, y: int(x) << 8 | int(y), ipadress.split('.'))

def read_packets(filepath):
    testcap = open(filepath, 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

    packets = list((
        pkt.packet.payload.src.decode('UTF8'),
        pkt.packet.payload.dst.decode('UTF8')
        ) for pkt in capfile.packets)

    return list(zip(*packets))

def learning_phase(packets, target_adress, mix_adress, m):
    sources, destinations = packets
    R, R_other, i, last = [], [], 0, False

    while not last:
        i = sources.index(target_adress, i)
        mix_start = sources.index(mix_adress, i)
        try: mix_end = destinations.index(mix_adress, mix_start)
        except ValueError: last = True
        r = set(destinations[mix_start : mix_end])
        if all(r.isdisjoint(ri) for ri in R):
            R.append(r)
        else:
            R_other.append(r)
        i = mix_end

    return R, R_other

def excluding_phase(R, R_rest):
    for r in R_rest:
        indices = [ i for i, ri in enumerate(R) if r & ri != set() ]
        if len(indices) == 1:
            index = indices[0]
            R[index] &= r

    R = list(set().union(*R))
    return R

if __name__ == "__main__":
    filepath, target_adress, mix_adress, m = input(), input(), input(), int(input())
    packets = read_packets(filepath)
    R, R_rest = learning_phase(packets, target_adress, mix_adress, m)
    targets = excluding_phase(R, R_rest)

    print('m:', m, 'found:', len(targets))
    print(sum(map(ipadress_to_int, targets)))
