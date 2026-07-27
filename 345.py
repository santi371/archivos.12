import pandas as pd 
import glob 

#1. buscar datos y leer archivos 

df_medellin = pd.read_csv('sucursal_medellin.csv')
print(df_medellin)

df_bogota = pd.read_excel('sucursal_bogota.xlsx')
print(df_bogota.head(3))

print(df_medellin.columns)
print(df_bogota.columns)


archivos_cvs = glob.glob('*.csv')
print(f'Archivos CSV encontrados: {archivos_cvs}')


archivos_xlsx = glob.glob('*.xlsx')
print(f'Archivos XLSX encontrados: {archivos_xlsx}')


#2. guardar en la lista

lista_dataframes = []

for archivo in archivos_cvs:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"leido archivo: {archivo} - {len(df)}filas")

for archivo in archivos_xlsx:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"leido archivo: {archivo} - {len(df)}filas")
