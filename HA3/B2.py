from functools import reduce

def mul_sum(array):
  return reduce(lambda x, y: x * y, array)

def threshold_scheme(k, n):
    f1 = f([20, 20, 11, 6])
    print(f1(2))
    print(f1(3))
    print(f1(4))
    print(f1(5))
    print(f1(6))

def lagrange_interpolation(t, f):
    return sum([f[i](i) * mul_sum([j / (j - i) for j in t if not i == j]) for i in t])


def f(c):
  return lambda x: sum([c[i] * x ** i for i in range(len(c))])

threshold_scheme(4, 6)
print(lagrange_interpolation([2, 3, 8], {2: f([1]), 3: f([2]), 8: f([3]) }))
