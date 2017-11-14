import binascii
import hashlib
from sys import argv

def findTreeRoot(leaves, i, path):
    if len(leaves) == 1:
        return leaves[0]
    elif len(leaves) % 2 == 1:
        leaves.append(leaves[-1])

    group_leaves = list(zip(leaves[::2], leaves[1::2]))

    branch = group_leaves[i//2]
    k = (i + 1) % 2
    path.append(['L', 'R'][k] + branch[k])

    parents = [getParent(left, right) for left, right in group_leaves]
    return findTreeRoot(parents, i // 2, path)

def findRoot(leaf, path):
    path.append(leaf)
    try:
        line = input('')
    except EOFError:
        return leaf
    _dir, sibling = line[:1], line[1:]
    go = {'L': getParent(sibling, leaf), 'R': getParent(leaf, sibling)}
    return findRoot(go[_dir], path)

def getParent(left, right):
    x = binascii.unhexlify(left + right)
    return hashlib.sha1(x).hexdigest()

if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == 'root':
            path = []
            print('Root:', findRoot(input(''), path))
        elif argv[1] == 'tree':
            index = int(input(''))
            depth = int(input(''))
            leaves = []
            path = []
            while True:
                try:
                    leaves.append(input(''))
                except EOFError:
                    break
            root = findTreeRoot(leaves, index, path)
            node = path[::-1][depth - 1]
            print('Merkle node + root:', node + root)
