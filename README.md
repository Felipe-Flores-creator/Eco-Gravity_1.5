# Eco_Gravity 1.5 (Beta)

**Eco_Gravity** es una herramienta gratuita para **QGIS** que calcula un **índice ambiental** basado en un modelo de atracción gravitacional modificado. Es ideal para comparar áreas geográficas según su influencia positiva o negativa sobre un punto de interés, usando información territorial vectorial.

---

## 🚀 ¿Para qué sirve?

Eco_Gravity permite:
- Calcular un **índice ambiental** considerando factores como vegetación, cuerpos de agua, vertederos, etc.
- Evaluar zonas de manera rápida, numérica y espacialmente explícita.
- Visualizar cómo los distintos elementos del territorio (positivos o negativos) influyen sobre puntos específicos.

---

## 📐 Lógica del índice

Inspirado en la ley de gravedad de Newton:

F = (masa1 * masa2) / distancia²



- **Área** y **Densidad** deben estar en los atributos de los polígonos (valores preferiblemente enteros).
- **Distancia**: desde cada polígono al punto de análisis.
- El índice se **normaliza** dividiendo por 10.000 para mayor legibilidad.

---

## 🟩 Polígonos positivos

Representan elementos que **mejoran** la calidad ambiental:
- Bosques, áreas verdes, cuerpos de agua limpios, humedales, etc.

✔ Aumentan el valor del índice.

---

## 🟥 Polígonos negativos

Representan elementos que **dañan** el medio ambiente:
- Vertederos, industrias contaminantes, sitios de deforestación.

❌ **Reducen** el valor del índice (efecto contrario).

---

## 📍 Punto de evaluación

- El usuario debe ingresar una **capa de puntos** (por ejemplo, puntos de interés, zonas pobladas, etc.).
- El cálculo del índice se realiza automáticamente sobre esos puntos.
- El resultado aparece en la **tabla de atributos del punto**, incluyendo:
  - `Attraction_Total`: Índice ambiental neto.
  - `Attraction_Positive`: Influencia positiva.
  - `Attraction_Negative`: Influencia negativa.

---

## ⚠️ Recomendaciones de uso

- Las capas de polígonos deben contener campos llamados:
  - `Densidad` (valor ecológico asignado).
  - `Area` (en unidades coherentes con tu proyección).
- Para **uso comercial o profesional**, se recomienda mejorar la herramienta:
  - Por ejemplo, **reemplazar la columna `Densidad` en cuerpos de agua** por indicadores como `calidad del agua`, `pH`, `turbidez`, etc.

---

## 🧪 Código fuente (QGIS Processing Python)

La herramienta está programada en Python usando la API de procesamiento de QGIS.  
Puedes consultar el código completo en el script `GravitationalAttraction.py`.

---

## 📥 Entradas requeridas

- Capas de polígonos ambientales positivos (`.shp`, múltiples capas).
- (Opcional) Capas de polígonos negativos (`.shp`, múltiples capas).
- Capa de puntos para evaluación (`.shp`, puntos únicos o múltiples).

---

## 📤 Salida

Una **tabla** sin geometría asociada con los resultados del cálculo para cada punto.

---

## 💸 Licencia

**Versión gratuita** para uso personal, académico o de investigación.  
Si deseas emplearla en **proyectos profesionales, comerciales o institucionales**, te sugerimos contactar al autor para personalizar la herramienta.

---

## 🧑‍💻 Autor

**Felipe Flores**  
📧 [felipe.ignacio.geo@gmail.com](mailto:felipe.ignacio.geo@gmail.com)

---

## 🌱 ¡Colabora!

¿Te gustaría colaborar o sugerir mejoras?  
Abre un *issue* o contacta al autor directamente. ¡Toda ayuda es bienvenida!
