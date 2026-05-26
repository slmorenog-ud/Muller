import tkinter as tk
from tkinter import messagebox, ttk
import cmath
import math
from visualizacion_muller import animar_muller

class MullerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Muller - Visualizador")
        self.root.geometry("450x450")
        self.root.resizable(False, False)
        
        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Configuración del Método", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos de entrada
        self.create_entry(main_frame, "Función f(x):", "f_entry", "x**3 - x - 1", 1)
        self.create_entry(main_frame, "Punto p0:", "p0_entry", "0.0", 2)
        self.create_entry(main_frame, "Punto p1:", "p1_entry", "0.5", 3)
        self.create_entry(main_frame, "Punto p2:", "p2_entry", "1.0", 4)
        self.create_entry(main_frame, "Rango Min (Eje X):", "min_entry", "-2.0", 5)
        self.create_entry(main_frame, "Rango Max (Eje X):", "max_entry", "3.0", 6)
        self.create_entry(main_frame, "Máx. Iteraciones:", "iter_entry", "20", 7)

        # Botón de Visualización
        self.btn_visualizar = ttk.Button(main_frame, text="¡INICIAR VISUALIZACIÓN!", command=self.ejecutar_visualizacion)
        self.btn_visualizar.grid(row=8, column=0, columnspan=2, pady=(30, 0), sticky="ew")

        # Ayuda rápida
        help_text = "Usa: sin(x), cos(x), exp(x), log(x), sqrt(x), x**2"
        help_label = ttk.Label(main_frame, text=help_text, font=("Arial", 8, "italic"), foreground="gray")
        help_label.grid(row=9, column=0, columnspan=2, pady=(10, 0))

    def create_entry(self, parent, label_text, attr_name, default_val, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=5)
        entry = ttk.Entry(parent, width=30)
        entry.insert(0, default_val)
        entry.grid(row=row, column=1, sticky="e", pady=5)
        setattr(self, attr_name, entry)

    def ejecutar_visualizacion(self):
        try:
            func_str = self.f_entry.get()
            p0 = float(self.p0_entry.get())
            p1 = float(self.p1_entry.get())
            p2 = float(self.p2_entry.get())
            x_min = float(self.min_entry.get())
            x_max = float(self.max_entry.get())
            iters = int(self.iter_entry.get())

            if x_min >= x_max:
                raise ValueError("El rango mínimo debe ser menor al máximo.")

            # Entorno seguro para evaluar la función
            safe_dict = {
                'sin': cmath.sin,
                'cos': cmath.cos,
                'exp': cmath.exp,
                'log': cmath.log,
                'sqrt': cmath.sqrt,
                'pi': math.pi,
                'e': math.e,
                '__builtins__': None
            }
            
            # Crear la función lambda a partir del string
            f = lambda x: eval(func_str, safe_dict, {'x': x})
            
            # Prueba rápida
            f(p0)
            
            # Cerrar ventanas previas de matplotlib si existen para no saturar
            import matplotlib.pyplot as plt
            plt.close('all')
            
            # Ejecutar animación
            animar_muller(f, p0, p1, p2, x_range=(x_min, x_max), max_iter=iters, nombre=func_str)

        except Exception as e:
            messagebox.showerror("Error de Entrada", f"Hubo un problema con los datos:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MullerGUI(root)
    root.mainloop()
