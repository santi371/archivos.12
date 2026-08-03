# Reto: uno de los 4 archivos tiene columnas con nombres distintos 
# a los demás. Deben:
# 1. Identificar cual archivo es (revisen las columnas de cada uno)
# 2. Identificar cual columna unica sirve para reconocerlo
# 3. Crear el diccionario de renombrado completo

lista_informes = []

for i, df in enumerate(lista_informes):
    if 'NOMBRE_COLUMNA_UNICA' in df.columns:
        lista_informes[i] = df.rename(columns={
            # completen aqui su propio diccionario,
            # basandose en como se llaman las columnas 
            # en los otros 3 archivos que si coinciden
        })
