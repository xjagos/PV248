from numpy import linalg
import math
from unittest import TestCase

def volume(*args):
    #kazdy bod jako samostatny argument typu list
    # vezmu prvni odectu od ostatnich
    #nasypu do matice, spocitam determinant
    # vydelim faktorialem poctu argumentu  - 1
    m = []
    for a in args[1:]:
        if (len(args[0]) != len(a) or (len(a) != (len(args) - 1))):
            raise ValueError
        m.append([x - y for x, y in zip(a, args[0])])
    return (linalg.det(m) / math.factorial(len(args) - 1))

class TestVolume(TestCase):
    def test_dimensionAndPointsMismatched(self):
        with self.assertRaises(ValueError):
            volume([0, 0], [1, 0], [1, 1], [0, 1])

    def test_wrongPoint(self):
        with self.assertRaises(ValueError):
            volume([0, 0], [1, 0], [1, 1, 1])

    def test_goodTriangleResult(self):
        self.assertEqual(volume([0, 0], [1, 0], [0, 1]), 0.5, "Spatny vysledek")

    def test_goodTetrahedronResult(self):
        self.assertEqual(volume([0,0,0],[2,0,0],[0,3,0],[1,1,2]),2, "Spatny vysledek")

