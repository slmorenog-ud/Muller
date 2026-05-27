import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cmath
from typing import Callable, List, Dict, Any, Tuple
from muller import muller, ComplexNumber

# Configuración de estilo global para un look más moderno
plt.style.use('seaborn-v0_8-muted')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def muller_history(
    f: Callable[[ComplexNumber], ComplexNumber], 
    p0: ComplexNumber, 
    p1: ComplexNumber, 
    p2: ComplexNumber, 
    tol: float = 1e-10, 
    max_iter: int = 20
) -> List[Dict[str, Any]]:
    """
    Versión del método de Muller que devuelve el historial de cada paso para graficar.
    """
    history: List[Dict[str, Any]] = []
    iteration: int = 0
    
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

def animar_muller(
    f: Callable[[ComplexNumber], ComplexNumber], 
    p0: ComplexNumber, 
    p1: ComplexNumber, 
    p2: ComplexNumber, 
    x_range: Tuple[float, float] = (-2, 3), 
    max_iter: int = 20, 
    nombre: str = "Método de Muller"
) -> None:
    history = muller_history(f, p0, p1, p2, max_iter=max_iter)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    
    # Eje X para graficar la función
    x_vals = np.linspace(x_range[0], x_range[1], 500)
    # Solo graficamos la parte real para visualización 2D
    y_vals = [f(x).real for x in x_vals]
    
    ax.plot(x_vals, y_vals, color='#2c3e50', label='f(x)', linewidth=2, alpha=0.8)
    ax.axhline(0, color='#34495e', lw=1, alpha=0.5)
    ax.axvline(0, color='#34495e', lw=1, alpha=0.5)
    
    scatter = ax.scatter([], [], color='#3498db', s=80, edgecolors='white', zorder=5, label='Puntos (p0, p1, p2)')
    p3_point = ax.scatter([], [], color='#e74c3c', marker='*', s=250, edgecolors='black', zorder=6, label='Siguiente (p3)')
    parabola_line, = ax.plot([], [], color='#e67e22', linestyle='--', linewidth=1.5, label='Parábola aproximada', alpha=0.7)
    
    # Fondo para el texto informativo
    text_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top', 
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='#bdc3c7'))

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
        px = np.linspace(x_range[0], x_range[1], 250)
        py = [ (a*(x - p2)**2 + b*(x - p2) + c).real for x in px ]
        parabola_line.set_data(px, py)
        
        text_info.set_text(f"Iteración: {step['iteration']}\n"
                          f"p3: {p3.real:.6f} + {p3.imag:.6f}j\n"
                          f"|f(p3)|: {abs(f(p3)):.2e}")
        
        return scatter, p3_point, parabola_line, text_info

    ani = FuncAnimation(fig, update, frames=len(history), init_func=init, blit=True, repeat=True, interval=1200)
    
    ax.set_title(f"Visualización: {nombre}", fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("x (Real)", fontsize=11)
    ax.set_ylabel("f(x) (Real)", fontsize=11)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    
    plt.tight_layout()
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
            f_custom = lambda x: eval(args.func, {"__builtins__": {}}, {**safe_dict, 'x': x})
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
