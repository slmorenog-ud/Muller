import unittest
import cmath
from visualizacion_muller import muller_history

class TestMullerHistory(unittest.TestCase):
    def test_history_length(self):
        f = lambda x: x**3 - x - 1
        history = muller_history(f, 0, 1, 2)
        self.assertGreater(len(history), 0)
        self.assertIn('p3', history[0])
        self.assertIn('coeffs', history[0])
        
    def test_convergence(self):
        f = lambda x: x**2 - 4 # Raíces en 2, -2
        history = muller_history(f, 1, 1.5, 3)
        last_p3 = history[-1]['p3']
        self.assertAlmostEqual(abs(last_p3), 2.0, places=5)

if __name__ == "__main__":
    unittest.main()
