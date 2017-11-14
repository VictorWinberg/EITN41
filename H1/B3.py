import binascii
import hashlib

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
    path = []
    print('Root:', findRoot(input(''), path))
    print(path[::-1])
