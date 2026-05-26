import tkinter as tk
from tkinter import messagebox, ttk
import cmath
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from visualizacion_muller import muller_history

class MullerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Muller Method Studio")
        self.root.geometry("1100x700")
        
        # Variables de control
        self.ani = None
        self.history = []
        
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

        # Configuración de Matplotlib
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.setup_empty_plot()

    def create_input(self, parent, label, default):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.insert(0, default)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(10, 0))
        return entry

    def setup_empty_plot(self):
        self.ax.clear()
        self.ax.axhline(0, color='black', lw=1)
        self.ax.axvline(0, color='black', lw=1)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.set_title("Visualización del Método")
        self.canvas.draw()

    def start_visualization(self):
        try:
            # Limpiar animación anterior
            if self.ani:
                self.ani.event_source.stop()

            # Leer inputs
            func_str = self.f_entry.get()
            p0 = complex(self.p0_entry.get())
            p1 = complex(self.p1_entry.get())
            p2 = complex(self.p2_entry.get())
            x_min = float(self.min_entry.get())
            x_max = float(self.max_entry.get())
            iters = int(self.iter_entry.get())

            # Entorno seguro
            safe_dict = {'sin': cmath.sin, 'cos': cmath.cos, 'exp': cmath.exp, 
                         'log': cmath.log, 'sqrt': cmath.sqrt, 'pi': math.pi, 'e': math.e,
                         '__builtins__': None}
            f = lambda x: eval(func_str, safe_dict, {'x': x})

            # Generar historial
            self.history = muller_history(f, p0, p1, p2, max_iter=iters)
            if not self.history:
                raise ValueError("No se pudo generar el historial de iteraciones.")

            # Mostrar resultado final en label
            last_p3 = self.history[-1]['p3']
            self.res_label.config(text=f"Raíz: {last_p3.real:.6f} + {last_p3.imag:.6f}j")

            # Preparar Plot
            self.ax.clear()
            x_vals = np.linspace(x_min, x_max, 400)
            y_vals = [f(x).real for x in x_vals]
            self.ax.plot(x_vals, y_vals, 'k-', label='f(x)', alpha=0.7)
            self.ax.axhline(0, color='black', lw=1)
            self.ax.axvline(0, color='black', lw=1)
            self.ax.grid(True, linestyle=':', alpha=0.6)
            self.ax.set_title(f"Visualización: {func_str}")

            self.scatter = self.ax.scatter([], [], color='blue', label='Puntos (p0, p1, p2)')
            self.p3_point = self.ax.scatter([], [], color='red', marker='*', s=150, label='Siguiente (p3)')
            self.parabola_line, = self.ax.plot([], [], 'r--', label='Parábola', alpha=0.6)
            self.ax.legend()

            def update(frame):
                step = self.history[frame]
                pts, f_pts = step['points'], step['f_points']
                p3, (a, b, c) = step['p3'], step['coeffs']
                p2 = pts[2]

                self.scatter.set_offsets(np.array([[p.real, f_p.real] for p, f_p in zip(pts, f_pts)]))
                self.p3_point.set_offsets(np.array([[p3.real, f(p3).real]]))
                
                px = np.linspace(x_min, x_max, 200)
                py = [(a*(x - p2)**2 + b*(x - p2) + c).real for x in px]
                self.parabola_line.set_data(px, py)
                
                return self.scatter, self.p3_point, self.parabola_line

            self.ani = FuncAnimation(self.fig, update, frames=len(self.history), interval=1000, blit=True, repeat=False)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MullerApp(root)
    root.mainloop()
