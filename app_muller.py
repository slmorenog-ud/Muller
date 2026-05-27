import tkinter as tk
from tkinter import messagebox, ttk
import cmath
import math
import numpy as np
from matplotlib.figure import Figure
import io
from typing import Optional, List, Dict, Any, Callable
from visualizacion_muller import muller_history
from muller import ComplexNumber

# Paleta de colores "Flat UI" para un estilo profesional
COLORS = {
    "bg": "#f5f6fa",
    "sidebar": "#2f3640",
    "accent": "#3498db",
    "text_light": "#dcdde1",
    "text_dark": "#2f3640",
    "success": "#44bd32",
    "error": "#c23616",
    "white": "#ffffff"
}

class MullerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Muller Method Studio - Professional")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS["bg"])
        
        # Variables de estado
        self.history: List[Dict[str, Any]] = []
        self.current_frame: int = 0
        self.animation_running: bool = False
        self.photo_img: Optional[tk.PhotoImage] = None
        self.f: Optional[Callable[[ComplexNumber], ComplexNumber]] = None
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuración de frames y etiquetas
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Sidebar.TFrame", background=COLORS["sidebar"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text_dark"], font=("Segoe UI", 10))
        style.configure("Sidebar.TLabel", background=COLORS["sidebar"], foreground=COLORS["text_light"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        
        # Configuración de botones
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.map("Action.TButton",
                  foreground=[('pressed', COLORS['white']), ('active', COLORS['white'])],
                  background=[('pressed', '!disabled', COLORS['accent']), ('active', '#2980b9')])

    def setup_ui(self):
        # Layout Principal
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # --- PANEL IZQUIERDO (SIDEBAR) ---
        sidebar = ttk.Frame(self.main_container, style="Sidebar.TFrame", padding="20")
        self.main_container.add(sidebar, weight=0)

        ttk.Label(sidebar, text="MULLER STUDIO", style="Sidebar.TLabel", font=("Segoe UI", 18, "bold")).pack(pady=(0, 30))

        # Entradas con estilo
        self.entries = {}
        fields = [
            ("Función f(x):", "f_x", "x**3 - x - 1"),
            ("Punto p0:", "p0", "0.0"),
            ("Punto p1:", "p1", "0.5"),
            ("Punto p2:", "p2", "1.0"),
            ("Rango Min:", "x_min", "-2.0"),
            ("Rango Max:", "x_max", "3.0"),
            ("Iteraciones:", "iters", "20")
        ]

        for label_text, key, default in fields:
            lbl = ttk.Label(sidebar, text=label_text, style="Sidebar.TLabel")
            lbl.pack(fill=tk.X, pady=(10, 2))
            entry = ttk.Entry(sidebar, font=("Consolas", 11))
            entry.insert(0, default)
            entry.pack(fill=tk.X, pady=(0, 5))
            self.entries[key] = entry

        # Botones de Acción
        btn_container = ttk.Frame(sidebar, style="Sidebar.TFrame")
        btn_container.pack(pady=30, fill=tk.X)

        self.btn_run = ttk.Button(btn_container, text="INICIAR", style="Action.TButton", command=self.start_visualization)
        self.btn_run.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.btn_stop = ttk.Button(btn_container, text="DETENER", style="Action.TButton", command=self.stop_animation, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

        # Resultados en Sidebar
        self.res_label = ttk.Label(sidebar, text="Esperando ejecución...", style="Sidebar.TLabel", 
                                  font=("Segoe UI", 10, "italic"), wraplength=200)
        self.res_label.pack(pady=10, fill=tk.X)

        # --- PANEL DERECHO (VISUALIZACIÓN) ---
        viz_panel = ttk.Frame(self.main_container, padding="20")
        self.main_container.add(viz_panel, weight=1)

        ttk.Label(viz_panel, text="Visualización Iterativa", style="Header.TLabel").pack(pady=(0, 20))

        # Contenedor del Gráfico
        self.plot_container = tk.Frame(viz_panel, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        self.plot_container.pack(fill=tk.BOTH, expand=True)
        
        self.plot_label = tk.Label(self.plot_container, bg="white")
        self.plot_label.pack(fill=tk.BOTH, expand=True)

        # Preparar Figura
        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor=COLORS["white"])
        self.ax = self.fig.add_subplot(111)
        self.update_canvas()

    def update_canvas(self):
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        self.photo_img = tk.PhotoImage(data=buf.read())
        self.plot_label.config(image=self.photo_img)

    def start_visualization(self):
        try:
            self.stop_animation() # Asegurar que no haya nada corriendo
            
            # Obtener y validar datos de entrada
            if not hasattr(self, 'entries') or self.entries is None:
                raise ValueError("Error interno: Los campos de entrada no están inicializados.")
                
            f_str = self.entries.get("f_x").get() if self.entries.get("f_x") else ""
            p0_str = self.entries.get("p0").get() if self.entries.get("p0") else "0"
            p1_str = self.entries.get("p1").get() if self.entries.get("p1") else "0"
            p2_str = self.entries.get("p2").get() if self.entries.get("p2") else "0"
            
            p0 = complex(p0_str)
            p1 = complex(p1_str)
            p2 = complex(p2_str)
            self.x_min = float(self.entries["x_min"].get())
            self.x_max = float(self.entries["x_max"].get())
            iters = int(self.entries["iters"].get())

            # Entorno seguro para evaluación (sin bloquear builtins básicos)
            safe_dict = {
                'sin': cmath.sin, 'sen': cmath.sin, 'cos': cmath.cos, 'tan': cmath.tan,
                'exp': cmath.exp, 'log': cmath.log, 'ln': cmath.log,
                'sqrt': cmath.sqrt, 'pi': math.pi, 'e': math.e,
                'abs': abs, 'complex': complex
            }
            
            self.f = lambda x: eval(f_str, {"__builtins__": {}}, {**safe_dict, 'x': x})

            self.history = muller_history(self.f, p0, p1, p2, max_iter=iters)
            if not self.history:
                raise ValueError("El método no generó iteraciones válidas.")

            last_step = self.history[-1]
            last_p3 = last_step.get('p3', 0)
            self.res_label.config(text=f"CONVERGENCIA FINALIZADA\nRaíz: {last_p3.real:.6f} + {last_p3.imag:.6f}j", 
                                 foreground=COLORS["success"])

            # Cambiar estados de botones
            self.btn_run.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)

            self.current_frame = 0
            self.animation_running = True
            self.animate_loop()

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            messagebox.showerror("Error de Ejecución", f"Se produjo un error:\n{str(e)}")
            self.res_label.config(text="Error en la ejecución.", foreground=COLORS["error"])

    def stop_animation(self):
        """Detiene la animación en curso y restaura los botones."""
        self.animation_running = False
        self.btn_run.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def animate_loop(self):
        if not self.animation_running:
            return
            
        if self.current_frame >= len(self.history):
            self.stop_animation()
            return

        step = self.history[self.current_frame]
        self.draw_step(step)
        self.current_frame += 1
        self.root.after(1200, self.animate_loop)

    def draw_step(self, step: Dict[str, Any]):
        self.ax.clear()
        
        # Estilo de la gráfica coincidente con visualizacion_muller.py
        x_vals = np.linspace(self.x_min, self.x_max, 500)
        y_vals = [self.f(x).real for x in x_vals]
        
        self.ax.plot(x_vals, y_vals, color='#2c3e50', lw=2, alpha=0.8, label='f(x)')
        self.ax.axhline(0, color='#34495e', lw=1, alpha=0.3)
        self.ax.axvline(0, color='#34495e', lw=1, alpha=0.3)
        self.ax.grid(True, linestyle=':', alpha=0.4)
        
        pts, f_pts = step['points'], step['f_points']
        p3, (a, b, c) = step['p3'], step['coeffs']
        p2 = pts[2]

        self.ax.scatter([p.real for p in pts], [fp.real for fp in f_pts], color='#3498db', s=80, edgecolors='white', zorder=5)
        self.ax.scatter([p3.real], [self.f(p3).real], color='#e74c3c', marker='*', s=250, edgecolors='black', zorder=6)
        
        px = np.linspace(self.x_min, self.x_max, 250)
        py = [(a*(x - p2)**2 + b*(x - p2) + c).real for x in px]
        self.ax.plot(px, py, color='#e67e22', linestyle='--', lw=1.5, alpha=0.7, label='Parábola')
        
        self.ax.set_title(f"Iteración {step['iteration']} | p3 ≈ {p3.real:.4f}", fontsize=12, fontweight='bold')
        self.ax.legend(loc='upper right', frameon=True, facecolor='white')
        
        self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = MullerApp(root)
    root.mainloop()
