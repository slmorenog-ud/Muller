# Método de Muller - Proyecto de Métodos Numéricos

Este repositorio contiene la implementación y documentación del **Método de Muller**, un algoritmo iterativo para la búsqueda de raíces de ecuaciones no lineales (tanto reales como complejas).

## Contenido del Proyecto

- `muller.py`: Implementación principal del algoritmo en Python.
- `ejemplos_muller.py`: Suite de pruebas con ejemplos detallados (funciones racionales, logarítmicas, radicales, etc.).
- `PROYECTO.tex`: Reporte final en formato LaTeX siguiendo la estructura de un artículo científico.
- `REPORTE.md`: Versión simplificada del reporte en Markdown.

## Requisitos

Para ejecutar el código, solo necesitas **Python 3.x**. No se requieren librerías externas, ya que se utilizan los módulos nativos `math` y `cmath`.

## Cómo Ejecutar

Para ver el método en acción con diversos ejemplos y su convergencia paso a paso:

```bash
python3 ejemplos_muller.py
```

Para usar el método en tu propio script:

```python
from muller import muller

f = lambda x: x**3 - x - 1
raiz = muller(f, 0, 1, 2)
print(f"La raíz es: {raiz}")
```

## Características Principales

- **Soporte Complejo:** Encuentra raíces imaginarias de forma nativa.
- **Estabilidad Numérica:** Implementa la fórmula cuadrática alternativa para evitar errores de redondeo.
- **Versatilidad:** Probado con funciones polinomiales, trascendentes y racionales.
- **Manejo de Clusters:** Lógica de actualización de puntos optimizada para raíces cercanas.

## Referencias

- Mathews, J. H., & Fink, K. D. (2000). *Métodos Numéricos con MATLAB*. Prentice Hall.
