# inspeccion.py — Tipos, columna derivada e indicadores (Python)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   python scripts/inspeccion.py

# TODO 1: carga data/ventas.csv
# TODO 2: imprime los tipos (dtypes) de cada columna
# TODO 3: crea la columna derivada "ticket" = ventas / clientes
# TODO 4: calcula e imprime:
#         - venta promedio por sucursal
#         - ticket promedio (ventas totales / clientes totales)
#         - sucursal con mayor y menor venta
#         - región con mayor venta total


import pandas as pd

ventas = pd.read_csv("data/ventas.csv")
ventas["ticket"] = ventas["ventas"] / ventas["clientes"]
print(ventas.head())

print(ventas["ventas"].max())

print(ventas.loc[ventas["ventas"].idxmax(),"sucursal" ]) #sucursal con mayor venta

print(ventas.loc[ventas["ventas"].idxmin(),"sucursal" ]) # sucursal con menor venta

ventas_per_region = ventas.groupby("region")["ventas"].sum()
print(ventas_per_region)

print(ventas_per_region.idxmax()) # Region con mayor venta total

