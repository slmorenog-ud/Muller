# El Método de Muller: Una Aproximación Geométrica y Numérica

**Autores:** [Tus Datos Aquí]  
**Institución:** [Nombre de la Institución]  
**Asignatura:** Métodos Numéricos  
**Fecha:** 26 de mayo de 2026

## 1. Introducción
La búsqueda de raíces de ecuaciones no lineales es un pilar fundamental en el análisis numérico. Mientras que el método de la secante utiliza una interpolación lineal entre dos puntos, el método de Muller extiende esta idea utilizando una interpolación cuadrática a través de tres puntos. Esta característica no solo permite una convergencia más rápida (casi cuadrática), sino que también faculta al método para encontrar raíces complejas, una limitación común en métodos basados exclusivamente en aritmética real.

## 2. Desarrollo Teórico y Motivación Geométrica

### 2.1 Intuición Geométrica
A diferencia de la secante que traza una línea, Muller propone ajustar una parábola $y = ax^2 + bx + c$ que pase por tres puntos iniciales: $(p_0, f(p_0))$, $(p_1, f(p_1))$ y $(p_2, f(p_2))$. La raíz de esta parábola que se encuentra más cerca del último punto ($p_2$) se toma como la siguiente aproximación $p_3$.

La motivación detrás de usar una parábola es capturar la curvatura local de la función, lo cual explica por qué el método es tan eficiente incluso cerca de puntos de inflexión o mínimos locales donde otros métodos podrían fallar o ralentizarse.

### 2.2 Origen de las Fórmulas
Para facilitar los cálculos, se realiza un cambio de variable $t = x - p_2$. El polinomio cuadrático resultante es:
$$P(t) = a t^2 + b t + c$$
Donde al evaluar en $t=0$ (que corresponde a $x=p_2$), obtenemos inmediatamente que $c = f(p_2)$. Los coeficientes $a$ y $b$ se derivan resolviendo el sistema lineal formado por las evaluaciones en $h_0 = p_0 - p_2$ y $h_1 = p_1 - p_2$.

### 2.3 La Fórmula Cuadrática Alternativa
Un aspecto crítico del método es el uso de la fórmula cuadrática en su forma:
$$z = \frac{-2c}{b \pm \sqrt{b^2 - 4ac}}$$
Esta forma es matemáticamente equivalente a la tradicional, pero numéricamente superior en este contexto. Al elegir el signo que maximiza la magnitud del denominador, evitamos la pérdida de significancia por cancelación sustractiva y garantizamos que estamos seleccionando la raíz de la parábola más cercana a $p_2$.

## 3. Desafíos Prácticos

### 3.1 Selección de Aproximaciones Iniciales
La elección de $p_0, p_1, p_2$ es vital. Si los puntos están demasiado alejados de la raíz, la parábola interpolante puede no representar bien a la función original, llevando a la divergencia o a converger a una raíz no deseada. Se recomienda realizar un estudio previo (gráfico o por bisección) para acotar la región de interés.

### 3.2 El Problema de Raíces Cercanas (Clusters)
Cuando existen raíces muy cercanas entre sí, el método puede saltar de una a otra. Para garantizar la convergencia a una raíz específica, es fundamental:
1.  **Cercanía:** Los puntos iniciales deben estar más cerca de la raíz objetivo que de cualquier otra.
2.  **Deflación:** Si ya se encontró una raíz $r_1$, se puede trabajar con la función $g(x) = \frac{f(x)}{x - r_1}$ para buscar las siguientes, eliminando la influencia de la raíz ya hallada.

## 4. Algoritmo e Implementación
La implementación en Python utiliza el módulo `cmath` para manejar de forma nativa la aritmética compleja, permitiendo encontrar raíces reales e imaginarias sin cambios en el código base.

```python
# Ver muller.py para la implementación completa
```

## 5. Ejemplos y Resultados
Se probaron diversas naturalezas de funciones:
1.  **Polinomial:** $x^3 - x - 1 = 0$ $\rightarrow$ Raíz: $1.3247$
2.  **Trascendente:** $e^{-x} - x = 0$ $\rightarrow$ Raíz: $0.5671$
3.  **Trigonométrica:** $\sin(x) - x/2 = 0$ $\rightarrow$ Raíz: $1.8954$
4.  **Compleja:** $x^2 + 1 = 0$ $\rightarrow$ Raíz: $0 + 1j$

## 6. Conclusión
El método de Muller es una herramienta poderosa y versátil. Su capacidad para manejar funciones no polinomiales y encontrar raíces complejas lo sitúa por encima de métodos más simples como la secante. Sin embargo, su éxito depende de una implementación cuidadosa de la estabilidad numérica y una elección informada de los valores iniciales.

## Bibliografía
- Mathews, J. H., & Fink, K. D. (2000). *Métodos Numéricos con MATLAB*. Prentice Hall.
