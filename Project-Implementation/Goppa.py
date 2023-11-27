from galois import irreducible_poly, GF2
from sympy.combinatorics import galois

from sympy import Matrix
import numpy as np
from sympy.abc import x, alpha
from sympy import GF, Poly
from sympy.polys.galoistools import gf_irreducible_p
from sympy import ZZ
from galois import GF2


class GoppaCodeGenerator:

    def __init__(self, m, n, t):
        # corp cu 2 ^ m elemente
        self.q = 2
        self.m = m
        self.n = n
        self.t = t

        print(f"Goppa Code (m={self.m},n={self.n},t={self.t},q={self.q},q^m={self.q ** self.m}) parameters")

    def power_dict(self, n, irr, p):
        result = {(1,): 0}
        test_poly = Poly(1, alpha)
        for i in range(1, n - 1):
            test_poly = (Poly(Poly(alpha, alpha) * test_poly, alpha) % irr).set_domain(GF(p))
            if tuple(test_poly.all_coeffs()) in result:
                return result
            result[tuple(test_poly.all_coeffs())] = i
        return result

    def is_irreducible_poly(self, poly, p):
        return gf_irreducible_p([int(c) for c in poly.all_coeffs()], p, ZZ)

    def irreducible_poly_ext_candidate(self, m, irr_poly, p, var, non_roots=None):
        elems = [0, 1, alpha]
        for e in non_roots:
            elems.append(alpha ** e)
        return Poly(np.concatenate([np.random.choice(elems[1:], size=1, replace=True),
                                    np.random.choice(elems, size=m, replace=True)], axis=0), var)

    def get_alpha_power(self, poly, irr_poly, quotient, p, neg=False):
        poly = (Poly(poly, alpha) % irr_poly).trunc(p)
        if poly.is_zero:
            return 0
        power = quotient[tuple(poly.all_coeffs())]
        if neg:
            power = len(quotient) - power
        return alpha ** power

    def reduce_to_alpha_power(self, poly, irr_poly, quotient, p):
        return Poly([self.get_alpha_power(coeff, irr_poly, quotient, p) for coeff in poly.all_coeffs()], x)

    def first_alpha_power_root(self, poly, irr_poly, p, elements_to_check=None):
        poly = Poly([(Poly(coeff, alpha) % irr_poly).trunc(p).as_expr() for coeff in poly.all_coeffs()], x)
        test_poly = Poly(1, alpha)
        print(f"testing f:{poly}")
        for i in range(1, p ** irr_poly.degree()):
            test_poly = (Poly(Poly(alpha, alpha) * test_poly, alpha) % irr_poly).set_domain(GF(p))
            if elements_to_check is not None and i not in elements_to_check:
                continue
            value = Poly((Poly(poly.eval(test_poly.as_expr()), alpha) % irr_poly), alpha).trunc(p)
            print(f"testing alpha^{i} f({test_poly})={value}")
            if value.is_zero:
                return i
        return -1

    @staticmethod
    def from_list(list):
        if len(list.shape) == 1:
            return np.array([GF2(x) for x in list])
        return np.array([[GF2(x) for x in line] for line in list])

    def get_binary_from_alpha(self, poly, irr_poly, p):
        poly = (Poly(poly, alpha) % irr_poly).trunc(p)
        result = np.full((irr_poly.degree(),), GF2(0))
        result[:len(poly.all_coeffs())] = [GF2(e) for e in poly.all_coeffs()[::-1]]
        return result

    def gen(self):

        # alegem polinom ireductibil - grad q^m peste F2
        irr_poly = Poly(alpha ** self.m + alpha + 1, alpha).set_domain(GF(self.q))
        # verificare ireductibilitate
        if self.is_irreducible_poly(irr_poly, self.q):
            ring = self.power_dict(self.q ** self.m, irr_poly, self.q)
        else:
            ring = []
        # numarul total de polinoame -> q^m - 1 peste Fq^m
        print("irr(q_size: {}): {}".format(len(ring), irr_poly))

        # crearea radacinilor primitive
        while len(ring) < self.q ** self.m - 1:
            irr_poly = irreducible_poly(self.m, self.q, alpha)
            ring = self.power_dict(self.q ** self.m, irr_poly, self.q)
            print("irr(q_size: {}): {}".format(len(ring), irr_poly))

        print(f"ring={ring}")  # r0, r1, ..., r{q^m - 1}

        g_poly = Poly(1, x)

        roots_num = max(0, self.q ** self.m - self.n - self.t)

        g_roots = set()
        g_non_roots = list(set(range(self.q ** self.m - 1)) - set(g_roots))

        print(f"g_roots({len(g_roots)})={g_roots}")
        print(f"g_non_roots({len(g_non_roots)})={g_non_roots}")

        for i in g_roots:
            g_poly = (g_poly * Poly(x + alpha ** i, x)).trunc(self.q)

        # pentru g(x) se aleg t elementele ale corpului; exp curs: g(x) = (x - r)(x - r^14), t = 2
        if g_poly.degree() < self.t:
            small_irr = None
            for i in range(100):
                small_irr = self.irreducible_poly_ext_candidate(self.t - g_poly.degree(), irr_poly, self.q, x,
                                                                non_roots=g_non_roots)
                print(f"irr_part_of_g={small_irr}")
                if small_irr.eval(0).is_zero or small_irr.eval(1).is_zero:
                    print(f'roots in trivial case 0:{small_irr.eval(0)} 1:{small_irr.eval(1)}')
                    continue
                first_root = self.first_alpha_power_root(small_irr, irr_poly, self.q)
                if first_root > 0:
                    print(f"alpha^{first_root} is a root of g(x)={small_irr}")
                    continue
                break
            else:
                raise Exception("irr poly not found")
            g_poly = (g_poly * small_irr).trunc(self.q)

        g_poly = self.reduce_to_alpha_power(g_poly, irr_poly, ring, self.q)
        print(f"g(x)={g_poly}")
        coeffs = g_poly.all_coeffs()

        first_root = self.first_alpha_power_root(g_poly, irr_poly, self.q, elements_to_check=g_non_roots)
        if first_root > 0:
            raise Exception(f"alpha^{first_root} is a root of g(x)={g_poly}")

        # generate parity check matrix => H = CXY (notatie din curs)
        # C matrice inferior triunghiulara
        C = Matrix(self.t, self.t, lambda i, j: coeffs[j - i] if 0 <= j - i < self.t else 0)
        print(f"C={C}")
        # X matricea cu alphauri pana la puterea t - 1
        X = Matrix(self.t, self.n, lambda i, j: (alpha ** ((j * (self.t - i - 1)) % self.n)))
        print(f"X={X}")
        # Y matricea cu g(a_i)^{-1} pe diagonala
        Y = Matrix(self.n, self.n,
                   lambda i, j: self.get_alpha_power(g_poly.eval(alpha ** g_non_roots[i]), irr_poly, ring, self.q,
                                                     neg=True)
                   if i == j else 0)
        print(f"Y={Y}")

        H = C * X * Y
        H = Matrix(self.t, self.n, lambda i, j: self.get_alpha_power(H[i, j], irr_poly, ring, self.q))
        print(f"H=\n{H}")

        # transformarea din reprezentarea cu alphauri in reprezentare binara
        H_bin = np.array(
            [np.column_stack([self.get_binary_from_alpha(e, irr_poly, self.q) for e in line]) for line in
             H.tolist()]).astype(GF2)
        H_bin = self.from_list(H_bin.reshape(-1, H.shape[1]))
        print(f"H_bin=\n{H_bin}")

        G = H_bin
        
        return G, H_bin, g_poly, irr_poly


class GF2():

    def __init__(self, n):
        self.n = int(n)

    def __add__(self, other):
        return GF2(self.n ^ other.n)

    def __sub__(self, other):
        return GF2(self.n ^ other.n)

    def __mul__(self, other):
        return GF2(self.n & other.n)

    def __truediv__(self, other):
        return self * other.inv()

    def __neg__(self):
        return self

    def __eq__(self, other):
        if isinstance(other, GF2):
            return self.n == other.n
        if self.n == int(other):
            return True
        return False

    def __abs__(self):
        return abs(self.n)

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return self.n

    def __divmod__(self, divisor):
        q, r = divmod(self.n, divisor.n)
        return (GF2(q), GF2(r))

    def flip(self):
        return GF2(1 if self.n == 0 else 0)

    def ext_euclid(self, a, b):
        if abs(b) > abs(a):
            (x, y, d) = self.ext_euclid(b, a)
            return (y, x, d)

        if abs(b) == 0:
            return (1, 0, a)

        x1, x2, y1, y2 = 0, 1, 1, 0
        while abs(b) > 0:
            q, r = divmod(a, b)
            x = x2 - q * x1
            y = y2 - q * y1
            a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

        return (x2, y2, a)

    def inv(self):
        x, y, d = self.ext_euclid(self.n, 2)
        return GF2(x)


goppa = GoppaCodeGenerator(4, 12, 2)
G, H_bin, g_poly, irr_poly = goppa.gen()
print("-----------")
print(H_bin)
print(g_poly)
print(irr_poly)
