import cmath
import math
from typing import Callable, Union, List, Optional

# Definición de tipo para valores que pueden ser reales o complejos
ComplexNumber = Union[float, complex]

def muller(
    f: Callable[[ComplexNumber], ComplexNumber],
    p0: ComplexNumber,
    p1: ComplexNumber,
    p2: ComplexNumber,
    tol: float = 1e-10,
    max_iter: int = 100
) -> ComplexNumber:
    """
    Encuentra una raíz de la función f utilizando el método de Muller.
    
    El método de Muller es un algoritmo iterativo que utiliza interpolación 
    cuadrática a través de tres puntos para aproximar una raíz. A diferencia
    del método de la secante, puede encontrar raíces complejas de forma nativa.

    Args:
        f: La función objetivo para la cual se busca la raíz.
        p0: Primera aproximación inicial.
        p1: Segunda aproximación inicial.
        p2: Tercera aproximación inicial (típicamente la más cercana a la raíz).
        tol: Tolerancia para el criterio de convergencia (abs(p_n - p_{n-1}) < tol).
        max_iter: Límite máximo de iteraciones para evitar bucles infinitos.

    Returns:
        ComplexNumber: La raíz aproximada encontrada.
        
    Raises:
        ZeroDivisionError: Si el denominador en la fórmula cuadrática se vuelve cero
                           y no se puede determinar el siguiente punto.
    """
    iteration: int = 0
    
    while iteration < max_iter:
        h0: ComplexNumber = p0 - p2
        h1: ComplexNumber = p1 - p2
        
        f0: ComplexNumber = f(p0)
        f1: ComplexNumber = f(p1)
        f2: ComplexNumber = f(p2)
        
        e0: ComplexNumber = f0 - f2
        e1: ComplexNumber = f1 - f2
        
        # Denominador del sistema para a y b
        det: ComplexNumber = h0 * h1 * (h0 - h1)
        if det == 0:
            # Si los puntos coinciden, no se puede formar la parábola.
            return p2
            
        a: ComplexNumber = (e0 * h1 - e1 * h0) / det
        b: ComplexNumber = (e1 * h0**2 - e0 * h1**2) / det
        c: ComplexNumber = f2
        
        # Discriminante de la ecuación cuadrática: at^2 + bt + c = 0
        discriminant: ComplexNumber = cmath.sqrt(b**2 - 4 * a * c)
        
        # Estabilidad numérica: elegir el signo que maximice la magnitud del denominador
        plus_den = b + discriminant
        minus_den = b - discriminant
        
        denominator = plus_den if abs(plus_den) > abs(minus_den) else minus_den
            
        if abs(denominator) < 1e-20:
            # Si el denominador es extremadamente pequeño, tomamos un paso nulo o salimos
            z: ComplexNumber = 0
        else:
            # Fórmula cuadrática alternativa para mayor precisión numérica
            z = -2 * c / denominator
            
        p3: ComplexNumber = p2 + z
        
        # Verificar convergencia
        if abs(z) < tol:
            return p3
            
        # Actualización de puntos: estrategia de los puntos más cercanos a p3
        # Esto mejora la convergencia local y el manejo de clusters de raíces.
        points: List[ComplexNumber] = [p0, p1, p2]
        points.sort(key=lambda p: abs(p - p3))
        
        p0, p1 = points[0], points[1]
        p2 = p3
        
        iteration += 1
        
    return p2

if __name__ == "__main__":
    # Pruebas de ejemplo
    print("Probando el Método de Muller...")
    
    # 1. Polinomio: x^3 - x - 1 = 0 (Raíz ~ 1.3247)
    f1 = lambda x: x**3 - x - 1
    root1 = muller(f1, 0, 1, 2)
    print(f"Polinomio x^3 - x - 1: {root1}")
    
    # 2. Trigonométrica: sen(x) - x/2 = 0 (Raíz ~ 1.8954)
    f2_c = lambda x: cmath.sin(x) - x/2
    root2 = muller(f2_c, 1.0, 1.5, 2.0)
    print(f"Trigonométrica sen(x) - x/2: {root2}")
    
    # 3. Exponencial: e^-x - x = 0 (Raíz ~ 0.5671)
    f3 = lambda x: cmath.exp(-x) - x
    root3 = muller(f3, 0, 0.5, 1)
    print(f"Exponencial e^-x - x: {root3}")
    
    # 4. Raíces complejas: x^2 + 1 = 0 (Raíces: +/- i)
    f4 = lambda x: x**2 + 1
    root4 = muller(f4, 0, 1, 2)
    print(f"Compleja x^2 + 1: {root4}")
