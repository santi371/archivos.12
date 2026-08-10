import pandas as pd
import glob
import matplotlib.pyplot as plt

# ============================================
# BOT DE VENTAS - Guía de referencia completada
# ============================================

# --------------------------------------------
# PARTE 1: Buscar y leer los archivos
# --------------------------------------------
archivos_csv = glob.glob("datos/sucursal_*.csv")
archivos_xlsx = glob.glob("datos/sucursal_*.xlsx")
lista_informes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_informes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo, engine='openpyxl')
    lista_informes.append(df)
    print(f"Leído: {archivo} - {len(df)} filas")

# --------------------------------------------
# PARTE 2: Consolidar (primer intento)
# --------------------------------------------
df_consolidado = pd.concat(lista_informes, ignore_index=True)
print("\nColumnas antes de renombrar:")
print(df_consolidado.columns)

# --------------------------------------------
# PARTE 3: Renombrar columnas
# --------------------------------------------
for i, df in enumerate(lista_informes):
    if 'Fecha_Venta' in df.columns:  # Columna única de la sucursal de Bogotá
        lista_informes[i] = df.rename(columns={
            'Fecha_Venta': 'fecha',
            'Producto': 'producto',
            'Categoria': 'categoria',
            'Cant': 'cantidad',
            'Valor_Unitario': 'precio_unitario',
            'Vendedor': 'vendedor',
            'Pago': 'metodo_pago'
        })

df_consolidado = pd.concat(lista_informes, ignore_index=True)
print("\nColumnas después de renombrar (deben ser 7):")
print(df_consolidado.columns) 

# --------------------------------------------
# PARTE 4: Limpieza de datos
# --------------------------------------------
# Limpiamos espacios extra en las columnas de texto primero para evitar falsos duplicados
for col in df_consolidado.columns:
    if df_consolidado[col].dtype == object:
        df_consolidado[col] = df_consolidado[col].astype(str).str.strip()

filas_antes = len(df_consolidado)
df_consolidado = df_consolidado.drop_duplicates()
print(f"\nFilas antes: {filas_antes} - después de eliminar duplicados: {len(df_consolidado)}")

print("\nValores nulos por columna:")
print(df_consolidado.isnull().sum())
# Rellenar nulos si hay (ejemplo: cantidades o precios vacíos con 0, o textos con 'Sin especificar')
df_consolidado['precio_unitario'] = pd.to_numeric(df_consolidado['precio_unitario'], errors='coerce').fillna(0)
df_consolidado['cantidad'] = pd.to_numeric(df_consolidado['cantidad'], errors='coerce').fillna(0)
df_consolidado['vendedor'] = df_consolidado['vendedor'].fillna('Sin especificar')
df_consolidado['categoria'] = df_consolidado['categoria'].fillna('Sin especificar')

# --------------------------------------------
# PARTE 5: Guardar el resultado
# --------------------------------------------
df_consolidado.to_excel("resultados/consolidado_limpio.xlsx", index=False)
print("\nArchivo guardado en resultados/consolidado_limpio.xlsx")

# --------------------------------------------
# PARTE 6: Análisis y visualización
# --------------------------------------------

# 6a. EJEMPLO RESUELTO: ventas por categoría (gráfico de barras)
ventas_por_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
ventas_por_categoria.plot(kind='bar', title='Ventas por Categoria', color='skyblue')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel('Ventas totales ($)')
plt.xlabel('Categoría')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("resultados/grafico_ventas_categoria.png")
plt.close() # Cerramos el gráfico para no superponerlos

# 6b. EJEMPLO RESUELTO: participación por vendedor (gráfico de torta)
ventas_por_vendedor = df_consolidado.groupby('vendedor')['precio_unitario'].sum()
ventas_por_vendedor.plot(kind='pie', autopct='%1.1f%%', title='Participacion de Ventas por Vendedor')
plt.ylabel('')
plt.tight_layout()
plt.savefig("resultados/grafico_ventas_vendedor.png")
plt.close()

# 6c. AHORA USTEDES: ¿cuál es el producto que aparece más veces?
productos_mas_frecuentes = df_consolidado['producto'].value_counts()
print("\nTop 5 productos que más veces aparecen en ventas:")
print(productos_mas_frecuentes.head(5))

# Graficamos el top 10 de productos
productos_mas_frecuentes.head(10).plot(kind='bar', title='Top 10 Productos Más Vendidos (Frecuencia)', color='coral')
plt.ylabel('Número de veces vendido')
plt.xlabel('Producto')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("resultados/grafico_productos_mas_vendidos.png")
plt.close()

print("\n¡Análisis completo! Gráficos guardados en la carpeta resultados/")
