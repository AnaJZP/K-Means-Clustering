# -*- coding: utf-8 -*-
"""K-means.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mhxjx17DXfzVqv07QD7FmNjc5m135VA_

# **Ana Lorena Jiménez Preciado**
# **Econometría Financiera - EARF**

# **K-means**
"""

## Librerias

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

"""# <span style="color:white"> K-Means Clustering </span>

## <span style="color:lightblue"> Introducción </span>
K-Means es un algoritmo de **clustering no supervisado** que agrupa datos en **K clusters** basándose en su proximidad. El objetivo es minimizar la **suma de distancias al cuadrado** entre puntos de datos y el centroide de su grupo.

## <span style="color:lightblue"> Pasos del Algoritmo </span>
1. **Inicialización**: Se eligen **K centroides** aleatorios, uno para cada cluster.
2. **Asignación de Clusters**: Cada punto se asigna al cluster cuyo centroide esté más cerca.
3. **Actualización de Centroides**: Se recalculan los centroides promediando los puntos en cada cluster.
4. **Iteración**: Los pasos 2 y 3 se repiten hasta que los centroides no cambien significativamente.

## <span style="color:lightblue"> Fórmulas Clave </span>

1. **Distancia Euclidiana**: Para asignar cada punto $x_i$ al centroide más cercano $\mu_j$, usamos la **distancia euclidiana**:
   $$
   d(x_i, \mu_j) = \sqrt{\sum_{k=1}^{n} (x_{ik} - \mu_{jk})^2}
   $$
   donde $x_{ik}$ y $ \mu_{jk}$ son las coordenadas del punto $i$ y del centroide $j$ en la dimensión $k$.

2. **Función Objetivo (Inercia)**: La función objetivo del K-Means busca minimizar la suma de las distancias al cuadrado entre los puntos y su centroide:
   $$
   J = \sum_{j=1}^{K} \sum_{x_i \in C_j} \|x_i - \mu_j\|^2
   $$
   donde $C_j$ es el conjunto de puntos asignados al cluster $j$.

La doble sumatoria en la función objetivo representa:

- a. **Sumatoria Externa**: La suma de las distancias al cuadrado dentro de cada cluster $ j $ .
- b. **Sumatoria Interna**: La suma de las distancias de cada punto $  x_i$  en el cluster $ j $  a su respectivo centroide $  \mu_j $ .


3. **Recalculación de Centroides**: Después de asignar los puntos a los clusters, el nuevo centroide de cada cluster $j$ es el promedio de todos los puntos en ese cluster:
   $$
   \mu_j = \frac{1}{|C_j|} \sum_{x_i \in C_j} x_i
   $$


El **centroide** de un cluster es el **punto promedio** de todos los puntos en ese cluster. Es el punto que minimiza la distancia total de todos los puntos en el cluster hacia él. Matemáticamente, el centroide del cluster $ j $ se calcula como:

$$
\mu_j = \frac{1}{|C_j|} \sum_{x_i \in C_j} x_i
$$

Donde:
- $ \mu_j $ es el centroide del cluster $ j $.
- $ |C_j|$ es el número de puntos en el cluster $ j $.
- $x_i$ representa cada punto en el cluster $ j $.

# <span style="color:white">Ejemplo de K-Means con precios de activos Financieros</span>

Supongamos que tenemos cinco días de precios para tres activos financieros. La idea es agrupar estos activos en dos clusters según la similitud en sus precios.

## <span style="color:lightblue">Datos de Precios de Activos</span>

Los precios para cada activo durante cinco días se ven así:

| Activo | Día 1 | Día 2 | Día 3 | Día 4 | Día 5 |
|--------|-------|-------|-------|-------|-------|
| Activo 1 | 100 | 102 | 101 | 105 | 107 |
| Activo 2 | 200 | 202 | 198 | 201 | 199 |
| Activo 3 | 105 | 106 | 104 | 108 | 110 |

**Matriz de características** (cada fila es un activo):

# <span style="color:white">Paso 1: Inicialización</span>

Elegimos dos centroides iniciales aleatorios de entre los puntos (o generamos centroides aleatorios). Supongamos que los inicializamos con:

- $ \mu_1 = [100, 102, 101, 105, 107] $ (similar al Activo 1)
- $ \mu_2 = [200, 202, 198, 201, 199] $ (similar al Activo 2)

# <span style="color:white">Paso 2: Asignación de Clusters</span>

Para cada activo, calculamos la **distancia euclidiana** entre el activo y cada centroide, y asignamos el activo al cluster con el centroide más cercano. Usamos la fórmula:

$$
d(x, \mu) = \sqrt{\sum_{i=1}^{n} (x_i - \mu_i)^2}
$$

Realizamos las operaciones paso a paso para cada activo:

1. **Para Activo 1** $(100, 102, 101, 105, 107)$:
   - Distancia a $\mu_1 = (100, 102, 101, 105, 107)$:
   $$d(x_1, \mu_1) = \sqrt{(100 - 100)^2 + (102 - 102)^2 + (101 - 101)^2 + (105 - 105)^2 + (107 - 107)^2} = 0$$

   - Distancia a $ \mu_2 = (200, 202, 198, 201, 199) $:
   $$d(x_1, \mu_2) = \sqrt{(100 - 200)^2 + (102 - 202)^2 + (101 - 198)^2 + (105 - 201)^2 + (107 - 199)^2}$$
     Calculamos cada término:
     - $(100 - 200)^2 = 10000$
     - $(102 - 202)^2 = 10000$
     - $(101 - 198)^2 = 9409$
     - $(105 - 201)^2 = 9216$
     - $(107 - 199)^2 = 8464$
     
     Entonces,
     $$
     d(x_1, \mu_2) = \sqrt{10000 + 10000 + 9409 + 9216 + 8464} = \sqrt{47089} \approx 217.04
     $$

   - **Resultado**: Activo 1 se asigna al Cluster 1, ya que $ d(x_1, \mu_1) < d(x_1, \mu_2) $.

2. **Para Activo 2** $(200, 202, 198, 201, 199)$:
   - Distancia a $ \mu_1 = (100, 102, 101, 105, 107) $:
   $$d(x_2, \mu_1) = \sqrt{(200 - 100)^2 + (202 - 102)^2 + (198 - 101)^2 + (201 - 105)^2 + (199 - 107)^2}$$
     Calculamos cada término:
     - $(200 - 100)^2 = 10000$
     - $(202 - 102)^2 = 10000$
     - $(198 - 101)^2 = 9409$
     - $(201 - 105)^2 = 9216$
     - $(199 - 107)^2 = 8464$
     
     Entonces,
     $$d(x_2, \mu_1) = \sqrt{10000 + 10000 + 9409 + 9216 + 8464} = \sqrt{47089} \approx 217.04$$
    

   - Distancia a $ \mu_2 = (200, 202, 198, 201, 199) $:
   $$d(x_2, \mu_2) = \sqrt{(200 - 200)^2 + (202 - 202)^2 + (198 - 198)^2 + (201 - 201)^2 + (199 - 199)^2} = 0
   $$

   - **Resultado**: Activo 2 se asigna al Cluster 2, ya que $ d(x_2, \mu_2) < d(x_2, \mu_1) $.

3. **Para Activo 3** $(105, 106, 104, 108, 110)$:
   - Distancia a $ \mu_1 = (100, 102, 101, 105, 107) $:
   $$d(x_3, \mu_1) = \sqrt{(105 - 100)^2 + (106 - 102)^2 + (104 - 101)^2 + (108 - 105)^2 + (110 - 107)^2}$$

     Calculamos cada término:
     - $(105 - 100)^2 = 25$
     - $(106 - 102)^2 = 16$
     - $(104 - 101)^2 = 9$
     - $(108 - 105)^2 = 9$
     - $(110 - 107)^2 = 9$
     
     Entonces,
     $$
     d(x_3, \mu_1) = \sqrt{25 + 16 + 9 + 9 + 9} = \sqrt{68} \approx 8.25
     $$

   - Distancia a $ \mu_2 = (200, 202, 198, 201, 199) $:
   $$d(x_3, \mu_2) = \sqrt{(105 - 200)^2 + (106 - 202)^2 + (104 - 198)^2 + (108 - 201)^2 + (110 - 199)^2}$$
   
     Calculamos cada término:
     - $(105 - 200)^2 = 9025$
     - $(106 - 202)^2 = 9216$
     - $(104 - 198)^2 = 8836$
     - $(108 - 201)^2 = 8649$
     - $(110 - 199)^2 = 7921$
     
     Entonces,
     $$
     d(x_3, \mu_2) = \sqrt{9025 + 9216 + 8836 + 8649 + 7921} = \sqrt{43647} \approx 208.88
     $$

   - **Resultado**: Activo 3 se asigna al Cluster 1, ya que $ d(x_3, \mu_1) < d(x_3, \mu_2) $.

# <span style="color:white">Resultados de Asignación Inicial</span>

- **Cluster 1**: Activo 1, Activo 3
- **Cluster 2**: Activo 2

Este es el paso inicial de asignación de clusters. Después de esto, se recalcularían los centroides y repetirían los pasos hasta que los centroides no cambien significativamente (criterio de convergencia).

## **Prueba del codo**

# <span style="color:white">Prueba del Codo</span>

La **prueba del codo** busca el número óptimo de clusters ($ K $) al observar cómo varía la **inercia** (o suma de las distancias al cuadrado) a medida que incrementamos $ K $. El objetivo es encontrar el punto en el que añadir más clusters no reduce significativamente la inercia, formando un "codo" en la gráfica.

## <span style="color:lightblue">Fórmula de Inercia (Función Objetivo)</span>

La inercia se calcula como:

$$
J = \sum_{j=1}^{K} \sum_{x_i \in C_j} \| x_i - \mu_j \|^2
$$

Donde:
- $ J $ es la inercia total para $ K $ clusters.
- $ K $ es el número de clusters.
- $ C_j $ es el conjunto de puntos en el cluster $ j $.
- $ x_i $ es cada punto en el cluster $ j $.
- $ \mu_j $ es el centroide del cluster $ j $.

---

## <span style="color:lightblue">Ejercicio Numérico para la Prueba del Codo</span>

Vamos a calcular la inercia para nuestro conjunto de datos de precios de activos con diferentes valores de $ K $. Usaremos los mismos datos de ejemplo:

| Activo | Día 1 | Día 2 | Día 3 | Día 4 | Día 5 |
|--------|-------|-------|-------|-------|-------|
| Activo 1 | 100 | 102 | 101 | 105 | 107 |
| Activo 2 | 200 | 202 | 198 | 201 | 199 |
| Activo 3 | 105 | 106 | 104 | 108 | 110 |

---

### Cálculo Paso a Paso de la Inercia

#### 1. Para $ K = 1 $
- Con $ K = 1 $, todos los puntos pertenecen al mismo cluster, por lo que el centroide es el promedio de todos los puntos:

  $$
  \mu = \left( \frac{100 + 200 + 105}{3}, \frac{102 + 202 + 106}{3}, \frac{101 + 198 + 104}{3}, \frac{105 + 201 + 108}{3}, \frac{107 + 199 + 110}{3} \right)
  $$
  - Calculamos cada componente del centroide:
    - Primer valor: $ \frac{100 + 200 + 105}{3} = 135 $
    - Segundo valor: $ \frac{102 + 202 + 106}{3} = 136.67 $
    - Tercer valor: $ \frac{101 + 198 + 104}{3} = 134.33 $
    - Cuarto valor: $ \frac{105 + 201 + 108}{3} = 138 $
    - Quinto valor: $ \frac{107 + 199 + 110}{3} = 138.67 $

  El centroide es $ \mu = (135, 136.67, 134.33, 138, 138.67) $.

- **Inercia para $ K = 1 $**:
  Sumamos las distancias al cuadrado de cada punto al centroide:

  - Para $ x_1 = (100, 102, 101, 105, 107) $:

  $$\| x_1 - \mu \|^2 = (100 - 135)^2 + (102 - 136.67)^2 + (101 - 134.33)^2 + (105 - 138)^2 + (107 - 138.67)^2 = 1220.89 + 1188.14 + 1098.78 + 1089 + 993.41 = 5590.22$$

  - Realizamos cálculos similares para $ x_2 $ y $ x_3 $, y sumamos para obtener la inercia total.

---

#### 2. Para $ K = 2 $
- Con $ K = 2 $, dividimos los puntos en dos clusters. Calculamos los centroides de cada cluster y sumamos las distancias al cuadrado.

- **Inercia para $ K = 2 $**:
  Calculamos las distancias al cuadrado y sumamos para cada punto en su respectivo cluster. Este proceso se repite hasta que obtenemos la inercia total.

---
"""

# Datos de ejemplo (precios de activos en días anteriores)
X = np.array([
    [100, 102, 101, 105, 107],
    [200, 202, 198, 201, 199],
    [105, 106, 104, 108, 110]
])

# Calculamos la inercia para distintos valores de K
inertias = []
K_values = range(1, 4)  # Evaluamos K desde 1 hasta el número de muestras
for k in K_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
    print(f"Número de Clusters (K): {k}, Inercia: {kmeans.inertia_:.2f}")

# Graficamos la inercia vs el número de clusters
plt.figure(figsize=(8, 6))
plt.plot(K_values, inertias, 'bo-', markersize=8)
plt.xticks(K_values)  # Aseguramos que solo se muestren números enteros en el eje X
plt.xlabel("Número de Clusters (K)")
plt.ylabel("Inercia")
plt.title("Prueba del Codo para Evaluar el Número de Clusters")
plt.show()

"""## **Prueba de la silueta**

# <span style="color:white">Prueba de Silueta</span>

La **prueba de silueta** mide qué tan bien se separan los clusters entre sí y qué tan cohesionados están los puntos dentro de cada cluster. La **silueta** de cada punto varía entre -1 y 1:
- Valores cercanos a 1 indican que el punto está bien agrupado dentro de su cluster.
- Valores cercanos a 0 indican que el punto está en el límite entre clusters.
- Valores negativos indican que el punto puede estar en el cluster incorrecto.

## <span style="color:lightblue">Fórmula del Coeficiente de Silueta</span>

Para cada punto $ x_i $, el coeficiente de silueta $ s(i) $ se define como:

$$
s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}
$$

Donde:
- $ a(i) $ es la distancia promedio entre $ x_i $ y todos los otros puntos en el mismo cluster (cohesión).
- $ b(i) $ es la distancia promedio entre $ x_i $ y todos los puntos en el cluster más cercano (separación).

El **coeficiente de silueta promedio** de todos los puntos es el valor que utilizamos para evaluar el rendimiento del clustering.

---

## <span style="color:lightblue">Ejercicio Numérico para la Prueba de Silueta</span>

Imaginemos que tenemos tres puntos en el **Cluster A** y dos puntos en el **Cluster B** con las siguientes distancias entre ellos:

### Distancias entre Puntos en el Mismo Cluster

- **Cluster A**:
  - Distancia entre $ x_1 $ y $ x_2 $: 2
  - Distancia entre $ x_1 $ y $ x_3 $: 4
  - Distancia entre $ x_2 $ y $ x_3 $: 3

- **Cluster B**:
  - Distancia entre $ y_1 $ y $ y_2 $: 5

### Distancias entre Puntos de Clusters Diferentes

- Distancia entre $ x_1 $ (en Cluster A) y $ y_1 $ (en Cluster B): 7
- Distancia entre $ x_1 $ y $ y_2 $: 8
- Distancia entre $ x_2 $ y $ y_1 $: 6
- Distancia entre $ x_2 $ y $ y_2 $: 9
- Distancia entre $ x_3 $ y $ y_1 $: 5
- Distancia entre $ x_3 $ y $ y_2 $: 4

### Cálculo de Silueta para el Punto $ x_1 $

1. **Cálculo de $ a(i) $** (cohesión):
   - $ x_1 $ está en el **Cluster A**.
   - Calculamos la distancia promedio de $ x_1 $ a los otros puntos en el mismo cluster:
   $$a(x_1) = \frac{\text{Distancia}(x_1, x_2) + \text{Distancia}(x_1, x_3)}{2} = \frac{2 + 4}{2} = 3$$

2. **Cálculo de $ b(i) $** (separación):
   - La distancia promedio de $ x_1 $ al **Cluster B** (puntos $ y_1 $ y $ y_2 $):
   $$b(x_1) = \frac{\text{Distancia}(x_1, y_1) + \text{Distancia}(x_1, y_2)}{2} = \frac{7 + 8}{2} = 7.5
   $$

3. **Coeficiente de Silueta para $ x_1 $**:
   - Sustituimos en la fórmula de silueta:
     $$
     s(x_1) = \frac{b(x_1) - a(x_1)}{\max(a(x_1), b(x_1))} = \frac{7.5 - 3}{\max(3, 7.5)} = \frac{4.5}{7.5} = 0.6
     $$

### Interpretación del Resultado para $ x_1 $
- El coeficiente de silueta de $ x_1 $ es 0.6, lo cual indica que está **bien agrupado** dentro de su cluster, pero relativamente cerca de los puntos en el otro cluster.

---

# <span style="color:white">Análisis de Silueta para los Activos Financieros</span>

Vamos a realizar el cálculo del **coeficiente de silueta** para cada punto en el conjunto de datos de los activos financieros, con el objetivo de evaluar la cohesión y separación de los clusters cuando $ K = 2 $.

## <span style="color:lightblue">Datos de Ejemplo</span>

Tenemos tres puntos que representan precios de activos en cinco días:

| Activo | Día 1 | Día 2 | Día 3 | Día 4 | Día 5 |
|--------|-------|-------|-------|-------|-------|
| Activo 1 | 100 | 102 | 101 | 105 | 107 |
| Activo 2 | 200 | 202 | 198 | 201 | 199 |
| Activo 3 | 105 | 106 | 104 | 108 | 110 |

Para el análisis, agruparemos estos puntos en dos clusters:
- **Cluster A**: Activo 1 y Activo 3
- **Cluster B**: Activo 2

## <span style="color:lightblue">Fórmula del Coeficiente de Silueta</span>

El coeficiente de silueta $ s(i) $ para cada punto $ x_i $ se define como:

$$
s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}
$$

Donde:
- $ a(i) $ es la distancia promedio entre $ x_i $ y todos los otros puntos en el mismo cluster (medida de cohesión).
- $ b(i) $ es la distancia promedio entre $ x_i $ y todos los puntos en el cluster más cercano (medida de separación).

---

## <span style="color:lightblue">Cálculo del Coeficiente de Silueta para Cada Activo</span>

### 1. Cálculo para el Activo 1

1. **Cálculo de $ a(i) $** (cohesión):
   - El Activo 1 está en el **Cluster A** con el Activo 3.
   - Calculamos la distancia euclidiana entre el Activo 1 y el Activo 3:
     $$
     d(x_1, x_3) = \sqrt{(100 - 105)^2 + (102 - 106)^2 + (101 - 104)^2 + (105 - 108)^2 + (107 - 110)^2}
     $$
     - Primer término: $ (100 - 105)^2 = 25 $
     - Segundo término: $ (102 - 106)^2 = 16 $
     - Tercer término: $ (101 - 104)^2 = 9 $
     - Cuarto término: $ (105 - 108)^2 = 9 $
     - Quinto término: $ (107 - 110)^2 = 9 $

     Entonces,
     $$
     d(x_1, x_3) = \sqrt{25 + 16 + 9 + 9 + 9} = \sqrt{68} \approx 8.25
     $$

   - Como solo hay un otro punto en el mismo cluster, $ a(x_1) = d(x_1, x_3) = 8.25 $.

2. **Cálculo de $ b(i) $** (separación):
   - La distancia promedio entre el Activo 1 (en Cluster A) y el Activo 2 (en Cluster B) es:
     $$
     b(x_1) = d(x_1, x_2) = \sqrt{(100 - 200)^2 + (102 - 202)^2 + (101 - 198)^2 + (105 - 201)^2 + (107 - 199)^2}
     $$
     - Primer término: $ (100 - 200)^2 = 10000 $
     - Segundo término: $ (102 - 202)^2 = 10000 $
     - Tercer término: $ (101 - 198)^2 = 9409 $
     - Cuarto término: $ (105 - 201)^2 = 9216 $
     - Quinto término: $ (107 - 199)^2 = 8464 $

     Entonces,
     $$
     b(x_1) = \sqrt{10000 + 10000 + 9409 + 9216 + 8464} = \sqrt{47089} \approx 217.04
     $$

3. **Coeficiente de Silueta para el Activo 1**:
   $$
   s(x_1) = \frac{b(x_1) - a(x_1)}{\max(a(x_1), b(x_1))} = \frac{217.04 - 8.25}{\max(8.25, 217.04)} = \frac{208.79}{217.04} \approx 0.96
   $$

### 2. Cálculo para el Activo 2

1. **Cálculo de $ a(i) $** (cohesión):
   - El Activo 2 está en el **Cluster B** y es el único punto en ese cluster, por lo que la cohesión es 0:
     $$
     a(x_2) = 0
     $$

2. **Cálculo de $ b(i) $** (separación):
   - La distancia promedio entre el Activo 2 y los puntos en el Cluster A (Activo 1 y Activo 3):
     $$
     b(x_2) = \frac{d(x_2, x_1) + d(x_2, x_3)}{2}
     $$
     Ya conocemos $ d(x_2, x_1) \approx 217.04 $ y ahora calculamos $ d(x_2, x_3) $:
     $$
     d(x_2, x_3) = \sqrt{(200 - 105)^2 + (202 - 106)^2 + (198 - 104)^2 + (201 - 108)^2 + (199 - 110)^2}
     $$
     - Primer término: $ (200 - 105)^2 = 9025 $
     - Segundo término: $ (202 - 106)^2 = 9216 $
     - Tercer término: $ (198 - 104)^2 = 8836 $
     - Cuarto término: $ (201 - 108)^2 = 8649 $
     - Quinto término: $ (199 - 110)^2 = 7921 $

     Entonces,
     $$
     d(x_2, x_3) = \sqrt{9025 + 9216 + 8836 + 8649 + 7921} = \sqrt{43647} \approx 208.88
     $$
     
     Ahora calculamos $ b(x_2) $:
     $$
     b(x_2) = \frac{217.04 + 208.88}{2} = 212.96
     $$

3. **Coeficiente de Silueta para el Activo 2**:
   $$
   s(x_2) = \frac{b(x_2) - a(x_2)}{\max(a(x_2), b(x_2))} = \frac{212.96 - 0}{\max(0, 212.96)} = 1.0
   $$

### 3. Cálculo para el Activo 3

1. **Cálculo de $ a(i) $** (cohesión):
   - El Activo 3 está en el **Cluster A** con el Activo 1.
   - $ a(x_3) = d(x_3, x_1) \approx 8.25 $.

2. **Cálculo de $ b(i) $** (separación):
   - La distancia promedio de $ x_3 $ al Cluster B (Activo 2):
   $$b(x_3) = d(x_3, x_2) \approx 208.88$$

3. **Coeficiente de Silueta para el Activo 3**:
$$s(x_3) = \frac{b(x_3) - a(x_3)}{\max(a(x_3), b(x_3))} = \frac{208.88 - 8.25}{\max(8.25, 208.88)} = \frac{200.63}{208.88} \approx 0.96$$

---

## <span style="color:lightblue">Interpretación de los Resultados</span>

- **Activo 1**: $ s(x_1) \approx 0.96 $
- **Activo 2**: $ s(x_2) = 1.0 $
- **Activo 3**: $ s(x_3) \approx 0.96 $

El coeficiente de silueta promedio es alto (cercano a 1), lo cual indica que los puntos están bien agrupados dentro de sus clusters y están bien separados de los otros clusters. Esto sugiere que $ K = 2 $ es un buen número de clusters para este conjunto de datos.

---
"""

# Datos de ejemplo (precios de activos en días anteriores)
X = np.array([
    [100, 102, 101, 105, 107],
    [200, 202, 198, 201, 199],
    [105, 106, 104, 108, 110]
])

# Calculamos el coeficiente de silueta para distintos valores de K
silhouette_scores = []
K_values = range(2, 3)  # Cambiamos el rango a 2 para que no exceda el número de muestras
for k in K_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)
    print(f"Número de Clusters (K): {k}, Coeficiente de Silueta: {score:.4f}")

# Graficamos los resultados de la prueba de silueta
plt.figure(figsize=(8, 6))
plt.plot(K_values, silhouette_scores, 'bo-', markersize=8)
plt.xticks(K_values)  # Aseguramos que solo se muestren números enteros en el eje X
plt.xlabel("Número de Clusters (K)")
plt.ylabel("Coeficiente de Silueta")
plt.title("Prueba de Silueta para Evaluar el Número de Clusters")
plt.show()

"""**# 1. Descripción del análisis**

# Análisis de Clusters para Países Latinoamericanos: Un Enfoque Multidimensional

Este notebook presenta un análisis de clustering para países latinoamericanos utilizando indicadores
socioeconómicos y ambientales clave. El objetivo es identificar grupos de países con características
similares considerando múltiples dimensiones del desarrollo.

## Variables utilizadas:
- GDPPC: PIB per cápita
- CO2GDP: Emisiones de CO2 por PIB
- EIL: Nivel de intensidad energética
- PRE: Porcentaje de energía renovable
- Trade: Apertura comercial
- FG: Globalización financiera
- Gini: Coeficiente de Gini
- School: Años promedio de escolaridad
- Net: Ahorro neto ajustado

## Metodología:
1. Preparación de datos y estandarización
2. Determinación del número óptimo de clusters usando método del codo y silueta
3. Aplicación de K-means
4. Visualización y análisis de resultados

"""

# 2. Cargamos y preparamos los datos
# Leemos los datos
df = pd.read_csv('green.csv')
df

# 2. Exploramos la estructura básica
print("Dimensiones del dataset:")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

print("\nInformación general del dataset:")
print(df.info())

print("\nEstadísticas descriptivas:")
print(df.describe())

# 3. Verificamos valores faltantes
print("\nValores faltantes por columna:")
print(df.isnull().sum())

# 4. Análisis temporal
years_by_country = df.groupby('Country')['Year'].agg(['min', 'max', 'count'])
print("\nCobertura temporal por país:")
print(years_by_country)

# 5. Matriz de correlación
variables_cluster = ['GDPPC', 'CO2GDP', 'EIL', 'PRE', 'Trade', 'FG', 'Gini', 'School', 'Net']
correlation_matrix = df[variables_cluster].corr()

# Visualización de la matriz de correlación
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis', center=0)
plt.title('Matriz de Correlación de Variables')
plt.show()

"""## 2. Preparación de Datos para Clustering

Analizaremos dos enfoques:

- A. Usando el último año disponible (2020)
- B. Usando promedios por país
"""

# A. Preparación con último año
df_recent = df[df['Year'] == 2020].copy()
X_recent = df_recent[variables_cluster]

# B. Preparación con promedios
df_means = df.groupby('Country')[variables_cluster].mean().reset_index()
X_means = df_means[variables_cluster]

# Estandarización para ambos casos
scaler = StandardScaler()
X_recent_scaled = scaler.fit_transform(X_recent)
X_means_scaled = scaler.fit_transform(X_means)

# 3. Determinamos el k óptimo
def evaluate_clusters(X_scaled, title_prefix):
    k_range = range(2, 11)
    inertias = []
    silhouette_scores = []

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

    # Visualización
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=(f'{title_prefix} - Método del Codo',
                                      f'{title_prefix} - Coeficiente de Silueta'))

    fig.add_trace(
        go.Scatter(x=list(k_range), y=inertias, mode='lines+markers',
                   line=dict(color='#440154')),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=list(k_range), y=silhouette_scores, mode='lines+markers',
                   line=dict(color='#440154')),
        row=1, col=2
    )

    fig.update_layout(height=400, width=800, showlegend=False,
                     title=f'Determinación del número óptimo de clusters - {title_prefix}')
    fig.show()

    return inertias, silhouette_scores

# Evaluamos clusters para ambos enfoques
inertias_recent, sil_recent = evaluate_clusters(X_recent_scaled, "Último Año (2020)")
inertias_means, sil_means = evaluate_clusters(X_means_scaled, "Promedios Históricos")

# 4. Imprimimos los scores
print("Scores para el último año (2020):")
print("K\tInercia\t\tSilueta")
print("-" * 40)
for k, (inertia, silhouette) in enumerate(zip(inertias_recent, sil_recent), 2):
    print(f"{k}\t{inertia:.4f}\t{silhouette:.4f}")

print("\nScores para promedios históricos:")
print("K\tInercia\t\tSilueta")
print("-" * 40)
for k, (inertia, silhouette) in enumerate(zip(inertias_means, sil_means), 2):
    print(f"{k}\t{inertia:.4f}\t{silhouette:.4f}")

# 5. Aplicamos k-means con k óptimo
k_optimo = 4
kmeans_recent = KMeans(n_clusters=k_optimo, random_state=42)
kmeans_means = KMeans(n_clusters=k_optimo, random_state=42)

clusters_recent = kmeans_recent.fit_predict(X_recent_scaled)
clusters_means = kmeans_means.fit_predict(X_means_scaled)

# 6. Añadimos los clusters a los dataframes
df_recent['Cluster'] = clusters_recent
df_means['Cluster'] = clusters_means

# 7. Visualización 3D
fig_3d_recent = px.scatter_3d(df_recent,
                             x='GDPPC',
                             y='School',
                             z='Gini',
                             color='Cluster',
                             hover_data=['Country'],
                             color_continuous_scale='viridis',
                             title='Clusters de países - Último Año (2020)')
fig_3d_recent.show()

fig_3d_means = px.scatter_3d(df_means,
                            x='GDPPC',
                            y='School',
                            z='Gini',
                            color='Cluster',
                            hover_data=['Country'],
                            color_continuous_scale='viridis',
                            title='Clusters de países - Promedios Históricos')
fig_3d_means.show()

# 8. Visualización 2D con centroides
fig = make_subplots(rows=1, cols=2, subplot_titles=('K-means 2020 con centroides',
                                                   'K-means Promedios Históricos con centroides'))

# 9. Análisis estadístico de los clusters
print("\nResumen de características principales por cluster (2020):")
cluster_summary_recent = df_recent.groupby('Cluster')[variables_cluster].agg([
    ('media', 'mean')
]).round(4)
print(cluster_summary_recent)

print("\nResumen de características principales por cluster (Promedios Históricos):")
cluster_summary_means = df_means.groupby('Cluster')[variables_cluster].agg([
    ('media', 'mean')
]).round(4)
print(cluster_summary_means)

#  des-estandarizar los valores
def destandardize(standardized_value, original_mean, original_std):
    return (standardized_value * original_std) + original_mean

# Calculamos medias y desviaciones estándar originales
original_stats = df[variables_cluster].agg(['mean', 'std'])

print("Valores originales de los centroides (2020):")
print("-" * 50)
for var in variables_cluster:
    print(f"\n{var}:")
    print(f"Media original: {original_stats.loc['mean', var]:.4f}")
    print(f"Desviación estándar original: {original_stats.loc['std', var]:.4f}")

"""Interpretación de los Clusters:

Para el año 2020:

Cluster 0 - Países de Desarrollo Medio-Alto:
- PIB per cápita medio (6160 USD)
- Emisiones CO2/PIB moderadas (0.38)
- Educación relativamente alta (9.56 años)
- Baja proporción de energía renovable (19.31%)
- Desigualdad moderada (Gini 43.02)
- Apertura comercial moderada (Trade 49.54)

Cluster 1 - Países de Menor Desarrollo con Alta Renovabilidad:
- PIB per cápita bajo (2047 USD)
- Altas emisiones por PIB (0.38)
- Mayor uso de energía renovable (51.11%)
- Alta desigualdad (Gini 49.02)
- Alta apertura comercial (87.27)
- Educación más baja (7.12 años)

Cluster 2 - Países de Alto Desarrollo:
- PIB per cápita más alto (11878 USD)
- Bajas emisiones por PIB (0.20)
- Educación más alta (9.63 años)
- Energía renovable moderada (36.80%)
- Desigualdad alta (Gini 48.98)
- Alta globalización financiera (72.47)

Cluster 3 - Países en Transición:
- PIB per cápita medio-bajo (4949 USD)
- Bajas emisiones por PIB (0.22)
- Alta proporción de renovables (63.32%)
- Mayor desigualdad (Gini 51.74)
- Menor apertura comercial (42.67)
- Educación relativamente baja (7.06 años)

Evolución Histórica vs 2020:

1. Estabilidad:
   - Los clusters mantienen patrones similares
   - Las diferencias principales están en energía renovable y comercio

2. Cambios Notables:
   - Aumento general en años de escolaridad
   - Tendencia a menor desigualdad en algunos grupos
   - Mayor divergencia en PIB per cápita

3. Resiliencia:
   - Algunos países mantienen su posición en los clusters
   - Otros muestran movilidad entre grupos cercanos

Conclusiones:

1. Heterogeneidad Regional:
   - Clara diferenciación entre niveles de desarrollo
   - Patrones distintos de sostenibilidad ambiental
   - Diferencias persistentes en desigualdad

2. Desafíos:
   - Brecha educativa entre clusters
   - Desigualdad persistente
   - Balance entre desarrollo y sostenibilidad

3. Oportunidades:
   - Potencial de energía renovable
   - Mejoras en educación
   - Integración comercial y financiera
"""

# Función para asignar nombres descriptivos a los clusters
def assign_cluster_names(cluster):
    names = {
        0: "Desarrollo Medio-Alto",
        1: "Menor Desarrollo con Alta Renovabilidad",
        2: "Alto Desarrollo",
        3: "Países en Transición"
    }
    return names[cluster]

# Agregamos nombres descriptivos
df_recent['Cluster_Descripcion'] = df_recent['Cluster'].map(assign_cluster_names)

# Mostramos la clasificación final de países
print("\nClasificación final de países (2020):")
print(df_recent[['Country', 'Cluster_Descripcion']].sort_values('Cluster_Descripcion'))