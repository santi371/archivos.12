import pandas as pd
import glob
import os

carpeta = os.path.dirname(__file__)

# Leer solo archivos de sucursales
archivos_csv = glob.glob(os.path.join(carpeta, 'sucursal_*.csv'))
archivos_xlsx = glob.glob(os.path.join(carpeta, 'sucursal_*.xlsx'))

lista_dataframes = []

# CSV
for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f'Leído: {os.path.basename(archivo)} - {len(df)} filas')

# Excel
for archivo in archivos_xlsx:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f'Leído: {os.path.basename(archivo)} - {len(df)} filas')

# Renombrar Bogotá
for i, df in enumerate(lista_dataframes):
    if 'Fecha_Venta' in df.columns:
        lista_dataframes[i] = df.rename(columns={
            'Fecha_Venta': 'fecha',
            'Producto': 'producto',
            'Categoria': 'categoria',
            'Cant': 'cantidad',
            'Valor_Unitario': 'precio_unitario',
            'Vendedor': 'vendedor',
            'Pago': 'metodo_pago'
        })

# Verificar que no haya columnas duplicadas
for i, df in enumerate(lista_dataframes):
    df = df.loc[:, ~df.columns.duplicated()]
    lista_dataframes[i] = df

# Consolidar
df_consolidado = pd.concat(lista_dataframes, ignore_index=True)

# Limpiar datos
df_consolidado.columns = df_consolidado.columns.str.strip()

for col in df_consolidado.columns:
    if df_consolidado[col].dtype == object:
        df_consolidado[col] = df_consolidado[col].astype(str).str.strip()

df_consolidado = df_consolidado.drop_duplicates()

# Guardar
salida = os.path.join(carpeta, 'consolidado_limpio.xlsx')
df_consolidado.to_excel(salida, index=False)

print('Consolidación completada')
print(df_consolidado.shape)