import cmath
import math

def muller(f, p0, p1, p2, tol=1e-10, max_iter=100):
    """
    Encuentra una raíz de la función f utilizando el método de Muller.
    
    Argumentos:
        f: Función rellamable (callable).
        p0, p1, p2: Aproximaciones iniciales.
        tol: Tolerancia para la convergencia.
        max_iter: Número máximo de iteraciones.
        
    Retorna:
        La raíz aproximada.
    """
    iteration = 0
    
    while iteration < max_iter:
        h0 = p0 - p2
        h1 = p1 - p2
        
        f0 = f(p0)
        f1 = f(p1)
        f2 = f(p2)
        
        e0 = f0 - f2
        e1 = f1 - f2
        
        # Resolviendo el sistema para a y b:
        # a*h0^2 + b*h0 = e0
        # a*h1^2 + b*h1 = e1
        # Usando la regla de Cramer o sustitución según Mathews & Fink (Eq. 15)
        det = h0 * h1 * (h0 - h1)
        if det == 0:
            # Retorno de emergencia si los puntos no son lo suficientemente distintos
            return p2
            
        a = (e0 * h1 - e1 * h0) / det
        b = (e1 * h0**2 - e0 * h1**2) / det
        c = f2
        
        # Discriminante
        discriminant = cmath.sqrt(b**2 - 4 * a * c)
        
        # Elegir el denominador con la mayor magnitud para estabilidad numérica
        if abs(b + discriminant) > abs(b - discriminant):
            denominator = b + discriminant
        else:
            denominator = b - discriminant
            
        if denominator == 0:
            # Evitar división por cero
            z = 0
        else:
            z = -2 * c / denominator
            
        p3 = p2 + z
        
        # Verificar convergencia
        if abs(z) < tol:
            return p3
            
        # Actualización de puntos: elegir los dos puntos más cercanos a p3 entre {p0, p1, p2}
        # para asegurar que la parábola se mantenga local a la raíz que se está aproximando.
        # Esto ayuda a manejar clusters de raíces (raíces cercanas).
        points = [p0, p1, p2]
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
    
    # 2. Trigonométrica: sin(x) - x/2 = 0 (Raíz ~ 1.8954)
    f2_c = lambda x: cmath.sin(x) - x/2
    root2 = muller(f2_c, 1, 2, 3)
    print(f"Trigonométrica sin(x) - x/2: {root2}")
    
    # 3. Exponencial: e^-x - x = 0 (Raíz ~ 0.5671)
    f3 = lambda x: cmath.exp(-x) - x
    root3 = muller(f3, 0, 0.5, 1)
    print(f"Exponencial e^-x - x: {root3}")
    
    # 4. Raíces complejas: x^2 + 1 = 0 (Raíces: +/- i)
    f4 = lambda x: x**2 + 1
    root4 = muller(f4, 0, 1, 2)
    print(f"Compleja x^2 + 1: {root4}")
