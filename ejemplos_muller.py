import cmath
import math

def muller_verbose(f, p0, p1, p2, tol=1e-10, max_iter=50, nombre=""):
    """
    Encuentra una raíz de la función f usando el método de Muller e imprime el progreso.
    """
    print(f"\n--- Probando Función: {nombre} ---")
    print(f"{'Iter':<5} | {'Aproximación de Raíz':<30} | {'f(p3)':<20}")
    print("-" * 65)
    
    iteration = 0
    while iteration < max_iter:
        f0, f1, f2 = f(p0), f(p1), f(p2)
        h0, h1 = p0 - p2, p1 - p2
        e0, e1 = f0 - f2, f1 - f2
        
        det = h0 * h1 * (h0 - h1)
        if det == 0: break
            
        a = (e0 * h1 - e1 * h0) / det
        b = (e1 * h0**2 - e0 * h1**2) / det
        c = f2
        
        disc = cmath.sqrt(b**2 - 4 * a * c)
        den = b + disc if abs(b + disc) > abs(b - disc) else b - disc
        
        if den == 0: z = 0
        else: z = -2 * c / den
            
        p3 = p2 + z
        f3 = f(p3)
        
        print(f"{iteration:<5} | {str(p3):<30} | {abs(f3):.2e}")
        
        if abs(z) < tol or abs(f3) < tol:
            print(f"Convergió a: {p3}")
            return p3
            
        # Lógica de actualización de puntos: mantener los más recientes y cercanos
        points = sorted([p0, p1, p2], key=lambda p: abs(p - p3))
        p0, p1 = points[0], points[1]
        p2 = p3
        iteration += 1
        
    print("Se alcanzó el máximo de iteraciones.")
    return p2

if __name__ == "__main__":
    # 1. Función Racional: (x^2 - 4) / (x - 1) = 0 -> Raíces en x=2, x=-2
    f_racional = lambda x: (x**2 - 4) / (x - 1) if x != 1 else 1e9
    muller_verbose(f_racional, 1.5, 2.5, 3.0, nombre="Racional (x^2-4)/(x-1)")

    # 2. Logarítmica + Polinomial: ln(x) + x^2 - 5 = 0 -> Raíz cerca de 2.1
    f_log = lambda x: cmath.log(x) + x**2 - 5
    muller_verbose(f_log, 1.0, 2.0, 3.0, nombre="Logarítmica ln(x) + x^2 - 5")

    # 3. Función Radical: sqrt(x) - cos(x) = 0 -> Raíz cerca de 0.64
    f_radical = lambda x: cmath.sqrt(x) - cmath.cos(x)
    muller_verbose(f_radical, 0.1, 0.5, 1.0, nombre="Radical sqrt(x) - cos(x)")

    # 4. Raíces Cercanas: (x - 1)(x - 1.001) = 0 -> Raíces en 1 y 1.001
    f_cluster = lambda x: (x - 1) * (x - 1.001)
    muller_verbose(f_cluster, 0.5, 0.8, 0.9, nombre="Raíces Cercanas (x-1)(x-1.001)")

    # 5. Raíz Compleja Pura: x^2 + x + 1 = 0 -> Raíces en -0.5 +/- 0.866i
    f_quad_compleja = lambda x: x**2 + x + 1
    muller_verbose(f_quad_compleja, 0, 1, 2, nombre="Cuadrática x^2 + x + 1")
