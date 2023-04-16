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
                G = generate_k_colorable_graph(k, n, 0.7)
                # Apply FitFirst coloring
                colors = fit_first(G)
                # Apply colors to G
                for node in G.nodes:
                    G.nodes[node]['group'] = colors[node]

                # Check that the coloring is valid
                for n in G.nodes:
                    neighbors = G.neighbors(n)
                    for neighbor in neighbors:
                        self.assertNotEqual(G.nodes[n]['group'], G.nodes[neighbor]['group'])


if __name__ == '__main__':
    unittest.main()