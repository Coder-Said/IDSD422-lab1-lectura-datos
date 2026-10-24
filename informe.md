# Informe técnico — Consolidación de reportes de ventas

**Para:** Gerencia de RetailAndina S.A. · **De:** Equipo de Business Intelligence
**Fecha:** 16/10/2026 · **Asunto:** Primer análisis de los reportes de ventas (semana 39)

---

## Resumen ejecutivo

Se recibieron los reportes semanales de ventas en tres formatos: CSV (ERP de sucursales), JSON (API de fidelización) y Excel (consolidado de Finanzas). Se confirmó que los tres contienen la misma información: 5 filas y 4 columnas, con tipos numéricos correctos en `ventas` y `clientes`. La sucursal con mayor venta es Guayaquil Centro (15.200) y la región con mayor venta total es la Sierra (30.860). El equipo recomienda usar cualquiera de los tres formatos como fuente, validando siempre estructura y tipos al momento de la carga.

## 1. ¿Los tres formatos contienen la misma información?

| Formato | Origen | Filas | Columnas | Lectura en código |
|---|---|---|---|---|
| CSV | ERP de sucursales | 5 | 4 | Python: `pd.read_csv()` · R: `read_csv()` (readr) |
| JSON | API de fidelización | 5 | 4 | Python: `json.load()` + `pd.json_normalize()` · R: `fromJSON()` (jsonlite) |
| Excel | Consolidado de finanzas | 5 | 4 | Python: `pd.read_excel(sheet_name="ventas")` · R: `read_excel(sheet="ventas")` (readxl) |

No, la estructura interna del archivo (texto plano, anidada o binaria) no cambia el contenido: en los tres formatos se obtuvo la misma tabla de 5 filas y 4 columnas, porque se trata del mismo dataset presentado de formas distintas.

## 2. Tipos de datos y calidad

| Variable | Tipo inferido (Python) | Tipo inferido (R) | Interpretación |
|---|---|---|---|
| `ventas` | int64 | dbl (CSV y Excel) / int (JSON) | Numérico, tipo esperado; permite cálculos directos. |
| `clientes` | int64 | dbl (CSV y Excel) / int (JSON) | Numérico, tipo esperado; permite calcular el ticket promedio. |
| `sucursal` | object | chr | Texto, tipo esperado para un nombre. |
| `region` | object | chr | Texto, tipo esperado para una categoría. |

Si `ventas` llegara como texto (`object` en Python, `chr` en R) indicaría registros sucios, con caracteres no numéricos, que requieren limpieza previa antes de calcular.

## 3. Particularidades técnicas encontradas

- **CSV:** se leyó directamente como tabla en ambos lenguajes (`read_csv` / `pd.read_csv`) y los tipos numéricos se infirieron correctamente.
- **JSON:** en R, `fromJSON()` devolvió directamente un data.frame. En Python, `json.load()` devolvió un diccionario/estructura anidada que hubo que aplanar con `pd.json_normalize()` para obtener una tabla.
- **Excel:** sí hubo que indicar la hoja (`sheet_name="ventas"` en Python, `sheet="ventas"` en R), ya que un archivo xlsx puede contener varias hojas.
- **Categóricas:** `sucursal` y `region` se expresan como texto: `object` en Python y `chr` en R.

## 4. Indicadores para la reunión del lunes

| Indicador | Valor |
|---|---|
| Venta promedio por sucursal | 12.008 (60.040 ÷ 5 sucursales) |
| Ticket promedio (ventas ÷ clientes) | 38,07 (60.040 ÷ 1.577 clientes); por sucursal entre 37,07 y 40,67 |
| Sucursal con mayor venta | Guayaquil Centro (15.200) |
| Sucursal con menor venta | Cuenca (8.540) |
| Región con mayor venta total | Sierra (30.860, frente a 29.180 de Costa) |

## 5. Conclusiones y recomendación

1. Los tres formatos (CSV, JSON y Excel) contienen la misma información: 5 filas y 4 columnas, con tipos numéricos correctos en `ventas` y `clientes`, por lo que no se detectaron datos sucios.
2. Guayaquil Centro es la sucursal con mayor venta y Cuenca la de menor venta; la Sierra lidera las ventas totales por región.
3. Se recomienda validar siempre estructura y tipos al cargar cada fuente (aplanar el JSON y especificar la hoja del Excel) y usar Pandas con `.idxmax()`, `.idxmin()` y `.groupby()` para automatizar estos indicadores.
