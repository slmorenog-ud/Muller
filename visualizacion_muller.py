import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cmath
from muller import muller

def muller_history(f, p0, p1, p2, tol=1e-10, max_iter=20):
    """
    Versión del método de Muller que devuelve el historial de cada paso para graficar.
    """
    history = []
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
        
        history.append({
            'iteration': iteration,
            'points': (p0, p1, p2),
            'f_points': (f0, f1, f2),
            'p3': p3,
            'coeffs': (a, b, c) # Para la parábola: a(x-p2)^2 + b(x-p2) + c
        })
        
        if abs(z) < tol:
            break
            
        points = sorted([p0, p1, p2], key=lambda p: abs(p - p3))
        p0, p1 = points[0], points[1]
        p2 = p3
        iteration += 1
        
    return history

def animar_muller(f, p0, p1, p2, x_range=(-2, 3), max_iter=20, nombre="Método de Muller"):
    history = muller_history(f, p0, p1, p2, max_iter=max_iter)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Eje X para graficar la función
    x_vals = np.linspace(x_range[0], x_range[1], 400)
    # Solo graficamos la parte real para visualización 2D
    y_vals = [f(x).real for x in x_vals]
    
    ax.plot(x_vals, y_vals, 'k-', label='f(x)', linewidth=1.5, alpha=0.7)
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    
    scatter = ax.scatter([], [], color='blue', label='Puntos (p0, p1, p2)')
    p3_point = ax.scatter([], [], color='red', marker='*', s=150, label='Siguiente (p3)')
    parabola_line, = ax.plot([], [], 'r--', label='Parábola aproximada', alpha=0.6)
    
    text_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top')

    def init():
        scatter.set_offsets(np.empty((0, 2)))
        p3_point.set_offsets(np.empty((0, 2)))
        parabola_line.set_data([], [])
        text_info.set_text('')
        return scatter, p3_point, parabola_line, text_info

    def update(frame):
        step = history[frame]
        pts = step['points']
        f_pts = step['f_points']
        p3 = step['p3']
        a, b, c = step['coeffs']
        p2 = pts[2]
        
        # Actualizar puntos actuales
        scatter.set_offsets(np.array([[p.real, f_p.real] for p, f_p in zip(pts, f_pts)]))
        
        # Actualizar p3
        p3_point.set_offsets(np.array([[p3.real, f(p3).real]]))
        
        # Dibujar parábola: y = a(x-p2)^2 + b(x-p2) + c
        px = np.linspace(x_range[0], x_range[1], 200)
        py = [ (a*(x - p2)**2 + b*(x - p2) + c).real for x in px ]
        parabola_line.set_data(px, py)
        
        text_info.set_text(f"Iteración: {step['iteration']}\np3: {p3.real:.6f} + {p3.imag:.6f}j")
        
        return scatter, p3_point, parabola_line, text_info

    ani = FuncAnimation(fig, update, frames=len(history), init_func=init, blit=True, repeat=True, interval=1500)
    
    plt.title(f"Visualización: {nombre}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Visualización interactiva del Método de Muller")
    parser.add_argument("--func", type=str, help="Función en términos de x (ej: 'x**3 - x - 1')")
    parser.add_argument("--p0", type=float, default=0.0, help="Punto inicial p0")
    parser.add_argument("--p1", type=float, default=0.5, help="Punto inicial p1")
    parser.add_argument("--p2", type=float, default=1.0, help="Punto inicial p2")
    parser.add_argument("--range", type=float, nargs=2, default=[-2.0, 3.0], metavar=('MIN', 'MAX'), help="Rango del eje X para mostrar")
    parser.add_argument("--iters", type=int, default=20, help="Máximo de iteraciones")
    parser.add_argument("--nombre", type=str, default="Personalizada", help="Nombre de la función")

    args = parser.parse_args()

    if args.func:
        # Crear entorno seguro para eval con funciones de cmath y math
        safe_dict = {
            'x': 0,
            'sin': cmath.sin,
            'cos': cmath.cos,
            'exp': cmath.exp,
            'log': cmath.log,
            'ln': cmath.log, # Alias para logaritmo natural
            'sqrt': cmath.sqrt,
            'pi': math.pi,
            'e': math.e
        }
        try:
            f_custom = lambda x: eval(args.func, {"__builtins__": None}, {**safe_dict, 'x': x})
            # Prueba rápida para verificar la función
            f_custom(0)
            print(f"Iniciando visualización personalizada para: {args.func}")
            animar_muller(f_custom, args.p0, args.p1, args.p2, x_range=tuple(args.range), max_iter=args.iters, nombre=args.func)
        except Exception as e:
            print(f"Error al procesar la función: {e}")
            sys.exit(1)
    else:
        # Ejecución por defecto si no hay argumentos
        f1 = lambda x: x**3 - x - 1
        print("Iniciando visualización por defecto para x^3 - x - 1...")
        animar_muller(f1, 0, 1, 2, x_range=(-1, 2.5), nombre="x^3 - x - 1")
