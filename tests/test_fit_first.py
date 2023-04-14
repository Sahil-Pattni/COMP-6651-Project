import sys
sys.path.append('..')
import unittest
from src.utils import generate_k_colorable_graph
from src.coloring.fit_first import fit_first

class FitFirstTest(unittest.TestCase):
    def test_fit_first(self):
        for k in [2,3]:
            for n in [5, 10, 20]:
                # Generate a random graph
                G, _ = generate_k_colorable_graph(k, n, 0.7)
                # Apply FitFirst coloring
                G_ = fit_first(G)
                # Check that the coloring is valid
                for n in G_.nodes:
                    neighbors = G_.neighbors(n)
                    for neighbor in neighbors:
                        self.assertNotEqual(G_.nodes[n]['group'], G_.nodes[neighbor]['group'])


if __name__ == '__main__':
    unittest.main()