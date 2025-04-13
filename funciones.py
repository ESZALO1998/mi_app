import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Función para escribir la introducción
def escribir_introduccion(nombre_madre, municipio_madre, cedula_madre, nombre_padre, municipio_padre, cedula_padre, ciudad_menor, niños):
    frases_concatenadas = ""
    nombres = []
    for clave, datos in niños.items():
        nombre = datos["nombre"]
        identificacion = datos["identificacion"]
        nombres.append(nombre)
        
        frase = f"{nombre} quien se identifica con NUIP No. {identificacion}"
        if frases_concatenadas:
            frases_concatenadas += "; " + frase
        else:
            frases_concatenadas += frase
    
    parrafo = f'''PEPITO PÉREZ, mayor de edad, domiciliado en la ciudad de Manizales - Caldas, e identificado 
    cédula de ciudadanía N° 1.111.111.111, abogado en ejercicio portador de la T.P N° 111.111 del C.S de la J, 
    obrando como apoderado especial de la señora {nombre_madre}, mayor de edad, vecina del municipio de {municipio_madre}, e identificada con la cédula de ciudadanía número {cedula_madre} y quien actúa como madre y representante legal de {frases_concatenadas}, con domicilio en {ciudad_menor}. Mediante el presente escrito, de manera respetuosa, presento DEMANDA EJECUTIVA DE ALIMENTOS EN FAVOR DE MENOR DE EDAD, en contra del señor {nombre_padre} mayor de edad, identificado con la cédula de ciudadanía número {cedula_padre} y vecino del municipio de {municipio_padre}, la cual fundamento en los siguientes:'''
    
    return parrafo, nombres

# Función para escribir el primer hecho
def escribir_hecho_1(nombre_madre, nombre_padre, nombres, ciudad_menor):
    hecho1 = f"""PRIMERO. La señora {nombre_madre} y el señor {nombre_padre}, son los padres de {', '.join(nombres)}, actualmente menores de edad, con domicilio en {ciudad_menor}."""
    
    return hecho1

# Función para escribir el segundo hecho
def escribir_hecho_2(dia_audiencia, acuerdo):
    
    hecho2 = f"""SEGUNDO. En audiencia de conciliación para fijación de cuota alimentaria, celebrada el {dia_audiencia}, realizaron acuerdo conciliatorio para la fijación de cuota alimentaria a cargo del demandado y en favor de sus hijos, en los siguientes términos:\n\n{acuerdo}"""
    
    return f"{hecho2}"

# Función para calcular meses entre fechas
def calcular_meses_entre_fechas(fecha_inicio, fecha_fin):
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    if isinstance(fecha_fin, str):
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    
    meses = (fecha_fin.year - fecha_inicio.year) * 12 + fecha_fin.month - fecha_inicio.month
    # if fecha_fin.day < fecha_inicio.day:
    #     meses -= 1
        
    return meses

# Función para escribir el tercer hecho
def escribir_hecho_3(fecha_inicio, fecha_fin):
    cantidad_meses = calcular_meses_entre_fechas(fecha_inicio, fecha_fin)
    hecho3 = f"""TERCERO. El demandado cesó pagos desde el {fecha_inicio} y hasta el {fecha_fin}, adeudando un total de {cantidad_meses} cuotas"""
    
    return hecho3

# Función para crear el dataframe de cuotas variables
def crear_dataframe_cuotas_variables(fecha_inicio, meses, cuota_inicial):
    incrementos_anuales = {
        2023: 0,
        2024: 0.02,
        2025: 0.05
    }
    
    fechas = []
    cuotas = []
    fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    cuota_base = cuota_inicial
    
    for i in range(meses + 1):
        fechas.append(fecha_actual.strftime('%Y-%m-%d'))
        año_actual = fecha_actual.year
        
        if i == 0:
            cuota_mes = cuota_base
        else:
            if fecha_actual.year > datetime.strptime(fechas[i-1], '%Y-%m-%d').year:
                incremento = incrementos_anuales.get(año_actual, 0)
                cuota_base = cuota_base * (1 + incremento)
            cuota_mes = cuota_base
        
        cuotas.append(cuota_mes)
        fecha_actual += relativedelta(months=1)
    
    df = pd.DataFrame()
    df['Fecha'] = fechas
    df['Año'] = [datetime.strptime(fecha, '%Y-%m-%d').year for fecha in fechas]
    df['Mes Adeudado'] = range(meses, -1, -1)
    df['Cuota'] = cuotas
    df['Interes 0.5%'] = df['Cuota'] * df['Mes Adeudado'] * 0.005
    df['Total'] = df['Cuota'] + df['Interes 0.5%']
    
    return df

# Función para escribir el cuarto hecho
def escribir_hecho_4(nombre_padre, df_cuotas_variables):
    suma_cuotas = df_cuotas_variables['Cuota'].sum()
    suma_intereses = df_cuotas_variables['Interes 0.5%'].sum()
    tabla_html = df_cuotas_variables.to_html(index=False, classes='table table-striped')
    
    hecho4 = f"""CUARTO. Actualmente {nombre_padre} adeuda las siguientes sumas de dinero. 
    \nPor concepto de cuotas adeudadas $ {suma_cuotas:,.0f}. 
    \nPor concepto de intereses $ {suma_intereses:,.0f}."""
    
    return hecho4, tabla_html