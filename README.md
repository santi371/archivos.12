# Bot de Ventas - Proyecto Final

Este proyecto consiste en un script automatizado (`bot.py`) diseñado para consolidar, limpiar y analizar datos de ventas provenientes de distintas sucursales. Los datos originales se encuentran en múltiples formatos (CSV y Excel) y el script se encarga de unificarlos para generar información valiosa y gráficos listos para la toma de decisiones.

## Estructura del proyecto

- `datos/`: Contiene los archivos originales de las ventas de diferentes sucursales en formatos `.csv` y `.xlsx`.
- `resultados/`: Carpeta donde el bot guarda el archivo de Excel consolidado y limpio, junto con todos los gráficos generados.
- `bot.py`: Script principal en Python que ejecuta todo el flujo de trabajo (lectura, limpieza y análisis).
- `README.md`: Este archivo explicativo.

---

## Requisitos y Ejecución

Para ejecutar este proyecto, necesitas tener instalado Python y las siguientes librerías:

```bash
pip install pandas matplotlib openpyxl
```

Una vez instaladas las dependencias, simplemente ejecuta el bot:

```bash
python bot.py
```

---

## Explicación del Código (`bot.py`)

El código está estructurado en 6 partes principales para procesar la información paso a paso de manera ordenada:

### Parte 1: Buscar y leer los archivos
Se utiliza la librería `glob` para buscar automáticamente todos los archivos `.csv` y `.xlsx` dentro de la carpeta `datos/`. Luego, un bucle `for` lee el contenido de cada archivo usando la librería `pandas` (`pd.read_csv` y `pd.read_excel`) y los va guardando en una lista temporal llamada `lista_informes`.

### Parte 2 y 3: Consolidar y Renombrar columnas
Las distintas sucursales pueden manejar nombres de columnas diferentes en sus archivos (por ejemplo, la sucursal de Bogotá usa `Fecha_Venta` en lugar de `fecha`). El código identifica estas diferencias y renombra las columnas afectadas para que todas las tablas tengan exactamente la misma estructura base (7 columnas: `fecha`, `producto`, `categoria`, `cantidad`, `precio_unitario`, `vendedor`, `metodo_pago`). Una vez estandarizadas, se unen todas las tablas en un único y gran conjunto de datos (DataFrame) usando la función `pd.concat()`.

### Parte 4: Limpieza de datos
Para garantizar que la información analizada sea de calidad, el programa aplica varias reglas de limpieza:
1. **Elimina espacios en blanco sobrantes** al principio y al final de los textos utilizando `.str.strip()`. Esto evita errores de clasificación (por ejemplo, evita que "Jean" y "Jean " sean contados como dos productos distintos).
2. **Elimina registros duplicados** empleando la función `.drop_duplicates()`.
3. **Maneja valores nulos (vacíos)**: Rellena las celdas de precios o cantidades que vengan vacías con `0` (`fillna(0)`), y rellena los campos de texto sin información (como el nombre del vendedor o la categoría) con la frase `'Sin especificar'`.

### Parte 5: Guardar el resultado
El gran conjunto de datos, ahora limpio, consolidado y sin errores, se exporta a un nuevo archivo de Excel ubicado en la ruta `resultados/consolidado_limpio.xlsx` mediante la función `to_excel()`. 

### Parte 6: Análisis y visualización
El bot realiza agrupaciones estadísticas sobre los datos (`groupby` y `value_counts`) y usa `matplotlib` para generar gráficos que responden a preguntas clave del negocio:
- **Ventas por categoría:** Agrupa por categoría y suma la columna `precio_unitario`, generando un **gráfico de barras**.
- **Participación por vendedor:** Agrupa por vendedor y suma sus ventas totales para ver la cuota de cada uno, generando un **gráfico de torta** (pie chart).
- **Productos más frecuentes:** Usa `value_counts()` sobre la columna `producto` para determinar cuáles son los artículos que se venden con más frecuencia (los que aparecen más veces en las transacciones). Se extrae el *Top 10* y se grafica en un diagrama de barras. 

Todos los gráficos se guardan automáticamente como imágenes `.png` dentro de la carpeta `resultados/`.

---

## Mini-Informe de Resultados

**¿Qué categoría vende más? ¿Por cuánto?**
La categoría que más vende es **Electrónica** con un total de **$3,265,600**.

**¿Qué vendedor tiene más ventas totales?**
El vendedor con más ventas es **Camila Ruiz**.

**¿Cuál es el producto más vendido?**
El producto más vendido (el que más veces aparece en las transacciones) es el **Jean clásico**, seguido muy de cerca por el **Cargador USB-C**.

**¿Qué decisión tomaría el dueño del negocio con esta información?**
Con esta información, el dueño del negocio podría tomar las siguientes decisiones:
1. **Invertir más en Electrónica**: Dado que es la categoría con mayores ingresos, se podría ampliar el catálogo de estos productos o negociar mejores precios con proveedores.
2. **Premiar a Camila Ruiz**: Implementar un sistema de bonos para motivar al mejor vendedor e incentivar a los demás.
3. **Estrategia de inventario**: Asegurar que nunca haya desabastecimiento de *Jeans clásicos* ni *Cargadores USB-C*, ya que son productos de alta rotación (los más frecuentes).
4. **Armar promociones cruzadas**: Ofrecer descuentos al comprar un Jean y un artículo menos popular, aprovechando la alta frecuencia del primero.
