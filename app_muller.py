import tkinter as tk
from tkinter import messagebox, ttk
import cmath
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from visualizacion_muller import muller_history

class MullerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Muller Method Studio - Pro")
        self.root.geometry("1100x750")
        
        # Variables de control
        self.history = []
        self.current_frame = 0
        self.animation_running = False
        self.photo_img = None # Referencia para evitar que el GC la borre
        
        self.setup_ui()

    def setup_ui(self):
        # Frame Principal (Horizontal)
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo: Controles
        control_frame = ttk.Frame(main_pane, padding="20", width=300)
        main_pane.add(control_frame, weight=0)

        ttk.Label(control_frame, text="Configuración", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        # Entradas
        self.f_entry = self.create_input(control_frame, "Función f(x):", "x**3 - x - 1")
        self.p0_entry = self.create_input(control_frame, "Punto p0:", "0.0")
        self.p1_entry = self.create_input(control_frame, "Punto p1:", "0.5")
        self.p2_entry = self.create_input(control_frame, "Punto p2:", "1.0")
        self.min_entry = self.create_input(control_frame, "Rango Min (X):", "-2.0")
        self.max_entry = self.create_input(control_frame, "Rango Max (X):", "3.0")
        self.iter_entry = self.create_input(control_frame, "Máx. Iteraciones:", "20")

        # Botón
        self.btn_run = ttk.Button(control_frame, text="INICIAR VISUALIZACIÓN", command=self.start_visualization)
        self.btn_run.pack(pady=20, fill=tk.X)

        # Resultado
        self.res_label = ttk.Label(control_frame, text="Raíz: ---", font=("Arial", 10, "italic"), foreground="blue")
        self.res_label.pack(pady=10)

        # Panel Derecho: Gráfico
        self.graph_frame = ttk.Frame(main_pane, padding="10")
        main_pane.add(self.graph_frame, weight=1)

        # Label donde mostraremos el gráfico convertido a imagen
        self.plot_label = tk.Label(self.graph_frame, bg="white")
        self.plot_label.pack(fill=tk.BOTH, expand=True)

        # Preparar la figura de Matplotlib (backend AGG para ser independiente)
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.update_plot_canvas() # Mostrar ejes vacíos al inicio

    def create_input(self, parent, label, default):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.insert(0, default)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(10, 0))
        return entry

    def update_plot_canvas(self):
        """Convierte la figura de Matplotlib a un objeto PhotoImage de Tkinter de forma nativa."""
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        self.photo_img = tk.PhotoImage(data=buf.read())
        self.plot_label.config(image=self.photo_img)

    def start_visualization(self):
        try:
            self.animation_running = False # Detener animación previa si existe
            
            # Leer inputs
            func_str = self.f_entry.get()
            p0 = complex(self.p0_entry.get())
            p1 = complex(self.p1_entry.get())
            p2 = complex(self.p2_entry.get())
            self.x_min = float(self.min_entry.get())
            self.x_max = float(self.max_entry.get())
            iters = int(self.iter_entry.get())

            # Entorno seguro para evaluar
            safe_dict = {
                'sin': cmath.sin,
                'cos': cmath.cos,
                'exp': cmath.exp,
                'log': cmath.log,
                'ln': cmath.log, # Alias para logaritmo natural
                'sqrt': cmath.sqrt,
                'pi': math.pi,
                'e': math.e,
                '__builtins__': None
            }

            self.f = lambda x: eval(func_str, safe_dict, {'x': x})

            # Generar historial
            self.history = muller_history(self.f, p0, p1, p2, max_iter=iters)
            if not self.history:
                raise ValueError("No se pudo converger o generar el historial.")

            # Mostrar resultado final
            last_p3 = self.history[-1]['p3']
            self.res_label.config(text=f"Raíz: {last_p3.real:.6f} + {last_p3.imag:.6f}j")

            # Iniciar ciclo de animación manual
            self.current_frame = 0
            self.animation_running = True
            self.animate_loop()

        except Exception as e:
            messagebox.showerror("Error", f"Verifica los datos:\n{str(e)}")

    def animate_loop(self):
        if not self.animation_running or self.current_frame >= len(self.history):
            return

        step = self.history[self.current_frame]
        self.draw_step(step)
        self.current_frame += 1
        
        # Siguiente frame en 1 segundo
        self.root.after(1000, self.animate_loop)

    def draw_step(self, step):
        self.ax.clear()
        
        # Dibujar función base
        x_vals = np.linspace(self.x_min, self.x_max, 400)
        y_vals = [self.f(x).real for x in x_vals]
        self.ax.plot(x_vals, y_vals, 'k-', label='f(x)', alpha=0.7)
        self.ax.axhline(0, color='black', lw=1)
        self.ax.axvline(0, color='black', lw=1)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        
        # Datos del paso
        pts, f_pts = step['points'], step['f_points']
        p3, (a, b, c) = step['p3'], step['coeffs']
        p2 = pts[2]

        # Puntos y Parábola
        self.ax.scatter([p.real for p in pts], [fp.real for fp in f_pts], color='blue', label='Puntos (p0, p1, p2)')
        self.ax.scatter([p3.real], [self.f(p3).real], color='red', marker='*', s=150, label='Siguiente (p3)')
        
        px = np.linspace(self.x_min, self.x_max, 200)
        py = [(a*(x - p2)**2 + b*(x - p2) + c).real for x in px]
        self.ax.plot(px, py, 'r--', label='Parábola', alpha=0.6)
        
        self.ax.set_title(f"Iteración {step['iteration']} | p3 ≈ {p3.real:.4f}")
        self.ax.legend(loc='upper right')
        
        self.update_plot_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = MullerApp(root)
    root.mainloop()
