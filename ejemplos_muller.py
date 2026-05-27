import cmath
from muller import muller

def ejecutar_ejemplos():
    print("="*50)
    print("MÉTODO DE MULLER: SUITE DE EJEMPLOS")
    print("="*50)

    ejemplos = [
        {
            "nombre": "Polinomio (Raíz Real)",
            "func": lambda x: x**3 - x - 1,
            "puntos": (0, 1, 2),
            "esperado": 1.3247
        },
        {
            "nombre": "Ecuación Cuadrática (Raíces Complejas)",
            "func": lambda x: x**2 + 1,
            "puntos": (0, 1, 2),
            "esperado": 1j
        },
        {
            "nombre": "Trascendente (Exponencial)",
            "func": lambda x: cmath.exp(-x) - x,
            "puntos": (0, 0.5, 1),
            "esperado": 0.5671
        },
        {
            "nombre": "Trigonométrica",
            "func": lambda x: cmath.sin(x) - x/2,
            "puntos": (1, 2, 3),
            "esperado": 1.8954
        },
        {
            "nombre": "Función Racional",
            "func": lambda x: (x**2 - 1) / (x + 2),
            "puntos": (0, 0.5, 0.8),
            "esperado": 1.0
        }
    ]

    for ej in ejemplos:
        print(f"\n--- Caso: {ej['nombre']} ---")
        try:
            raiz = muller(ej['func'], *ej['puntos'])
            error = abs(ej['func'](raiz))
            print(f"Puntos iniciales: {ej['puntos']}")
            print(f"Raíz encontrada:  {raiz.real:.6f} + {raiz.imag:.6f}j")
            print(f"Error |f(raiz)|:  {error:.2e}")
        except Exception as e:
            print(f"Error al ejecutar: {e}")

    print("\n" + "="*50)
    print("Fin de las pruebas.")
    print("="*50)

if __name__ == "__main__":
    ejecutar_ejemplos()
