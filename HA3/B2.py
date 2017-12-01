from functools import reduce

def input_ints():
  return list(map(int, input().split('=')[1].split(',')))

def mul_sum(array):
  return reduce(lambda x, y: x * y, array)

def lagrange_interpolation(t, f):
  fz = [f[i] * mul_sum([j / (j - i) for j in t if not i == j]) for i in t]
  return int(sum(fz))

def f(c):
  return lambda x: sum([c[i] * x ** i for i in range(len(c))])

coefficients = input_ints()
f1 = f(coefficients)

n_points = input_ints()
f_1 = sum([f1(1), *n_points])

t = [1] + input_ints()
points = [f_1] + input_ints()

print(lagrange_interpolation(t, { t[i]: points[i] for i in range(len(t)) }))
