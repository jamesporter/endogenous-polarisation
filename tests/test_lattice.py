from unittest import TestCase
from models import lattice as lt


class TestLattice(TestCase):
    def setUp(self):
        pass

    def test_lattice_simple(self):
        self.assertEqual(lt.get_neighbours(4,3,3), [0,1,2,3,5,6,7,8] )
        self.assertEqual(lt.get_neighbours(6,5,5), [0,1,2,5,7,10,11,12] )
        self.assertEqual(lt.get_neighbours(0,5,5), [24, 20, 21, 4, 1, 9, 5, 6])