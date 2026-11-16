Examen Final — AutoScraping Essentials
======================================

**Proyecto:** Product Search Scraper  
**Sitio objetivo:** [https://alabamatienda.com.ar/](https://alabamatienda.com.ar/)  
**Duración máxima:** 3 horas  
**Modalidad:** Individual  
**Lenguaje:** Python  
**Entrega:** Pull Request (PR) en GitHub

* * *

1. Objetivo del examen

----------------------

Desarrollar un scraper en Python capaz de realizar búsquedas de productos en una tienda de comercio electrónico, extraer información estructurada y almacenar los resultados en un archivo JSON.

El scraper deberá utilizar como entrada un archivo CSV que contendrá diferentes términos de búsqueda (_queries_).

Para cada término, deberá buscar los productos correspondientes en el sitio web, extraer la información solicitada y generar una salida que respete estrictamente el esquema definido.

**Este examen evalúa la capacidad de desarrollar una solución funcional, organizada y mantenible de manera autónoma.**

2. Sitio objetivo

-----------------

La extracción deberá realizarse exclusivamente sobre el siguiente sitio:

[**https://alabamatienda.com.ar/**](https://alabamatienda.com.ar/)

El scraper deberá ser capaz de:

* Realizar búsquedas utilizando los términos proporcionados.

* Identificar los productos correspondientes a cada búsqueda.

* Obtener la información de los productos.

* Identificar las variantes disponibles de cada producto.

* Procesar múltiples búsquedas durante una misma ejecución.

* Generar un único archivo JSON con todos los resultados.

La implementación deberá contemplar que una búsqueda puede devolver múltiples productos o ningún resultado.

3. Archivo de entrada

---------------------

El programa deberá leer las búsquedas desde:

`input/product.csv`

El archivo CSV contendrá una única columna llamada `query`.

**Ejemplo:**
    queryzapatillascamperaollaspantalon

### Requerimientos

* El archivo deberá leerse dinámicamente.

* No se permite definir las búsquedas directamente en el código.

* Cada fila representará una búsqueda independiente.

* El programa deberá procesar todas las queries válidas del archivo.

* Se deberá conservar el término de búsqueda original en la salida.

* Las filas vacías no deberán generar búsquedas.
4. Archivo de salida

--------------------

Los resultados deberán almacenarse en:

`output/output.json`

El archivo deberá contener una lista de objetos, donde cada objeto represente una query del CSV.

### Estructura general

    [  {    "query": "zapatillas",    
            "data": [  
                {
                    "url": "https://example.com/producto",        
                    "id": "12345",        
                    "name": "Zapatillas deportivas",       
                    "description": "Descripción del producto",        
                    "category_list": [        
                        "Calzado",          
                        "Zapatillas"       
                        ],        
                    "images": [          "https://example.com/image1.jpg"        ],        "variants": [    
                        {           
                            "id": "VAR-001",            
                            "group_id": "12345",            
                            "price": 45000.0,            
                            "list_price": 50000.0,           
                            "discount_percentage": 10,           
                            "available": true,            
                            "options": [              
                                {                
                                    "name": "Talle",                
                                    "value":"40"              
                                }            
                            ]
                        }        
                        ]     
                }    
            ]  
            },  
            {    "query": "ollas",    "data": []  }]

**Importante:** Los valores del ejemplo son ilustrativos y no representan productos reales del sitio.

### Requerimientos del JSON

* El archivo deberá ser un JSON válido.

* Se deberá respetar exactamente la estructura establecida.

* Cada query deberá generar un objeto independiente.

* La propiedad `data` siempre deberá ser una lista.

* Si una búsqueda no devuelve productos, `data` deberá ser `[]`.

* Los productos deberán incluir todos los campos requeridos.

* No se deberán duplicar productos dentro de una misma query.

* El resultado deberá conservar el orden de las queries del CSV.
5. Esquema de datos requerido

-----------------------------

### 5.1. Producto

Cada producto deberá contener los siguientes campos:

| Campo           | Tipo         | Descripción                      |
| --------------- | ------------ | -------------------------------- |
| `url`           | `str`        | URL absoluta del producto        |
| `id`            | `str`        | Identificador único del producto |
| `name`          | `str`        | Nombre del producto              |
| `description`   | `str`        | Descripción del producto         |
| `category_list` | `list[str]`  | Categorías asociadas al producto |
| `images`        | `list[str]`  | URLs absolutas de las imágenes   |
| `variants`      | `list[dict]` | Variantes del producto           |

### 5.2. Variantes

Cada variante deberá contener:

| Campo                 | Tipo         | Descripción                                 |
| --------------------- | ------------ | ------------------------------------------- |
| `id`                  | `str`        | Identificador de la variante                |
| `group_id`            | `str`        | Identificador del producto al que pertenece |
| `price`               | `float`      | Precio actual                               |
| `list_price`          | `float`      | Precio de lista, antes del descuento        |
| `discount_percentage` | `int`        | Porcentaje de descuento                     |
| `available`           | `bool`       | Disponibilidad de la variante               |
| `options`             | `list[dict]` | Opciones que identifican la variante        |

### 5.3. Opciones de variantes

Cada elemento de `options` deberá contener:

| Campo   | Tipo  | Descripción           |
| ------- | ----- | --------------------- |
| `name`  | `str` | Nombre de la opción   |
| `value` | `str` | Valor correspondiente |

Ejemplo:
    {  "name": "Talle",  "value": "40"}

Un producto podrá tener diferentes combinaciones de opciones, como talle, color u otras características.

Las variantes deberán representar las combinaciones reales identificadas en el sitio.

6. Reglas de extracción y normalización

---------------------------------------

### Campos faltantes

Cuando un campo no pueda obtenerse, deberá asignarse el valor `None` en Python, que se serializará como `null` en JSON.

No se permite inventar información para completar campos faltantes.

### Precios

* `price` y `list_price` deberán ser valores numéricos de tipo `float`.

* No deberán incluir símbolos monetarios ni separadores de miles.

* `discount_percentage` deberá ser un entero.

* Cuando existan los datos necesarios, el descuento deberá calcularse a partir del precio de lista y el precio actual.

* Si no existe descuento y ambos precios son iguales, `discount_percentage` deberá ser `0`.

* Si no es posible determinar un valor, deberá utilizarse `None`.

### Disponibilidad

* `true`: variante disponible.

* `false`: variante no disponible.

* `null`: no fue posible determinar la disponibilidad.

### Imágenes y categorías

* Las imágenes deberán representarse mediante una lista de URLs.

* Las categorías deberán representarse mediante una lista de strings.

* No se deberán incluir valores duplicados.

* Si no es posible obtener una lista, se deberá utilizar `None`.

### Variantes

* Cada variante deberá contener todos los campos definidos.

* Los identificadores deberán representarse como strings.

* Si un producto tiene múltiples variantes, deberán incluirse todas las identificadas.

* Si no es posible obtener la información de variantes, se deberá utilizar `None`.
7. Estructura obligatoria del proyecto

--------------------------------------

El proyecto deberá respetar la siguiente organización:

    project/
    ├── main.py
    ├── config.py
    ├── log.py
    ├── web_driver.py
    ├── input/
    │   └── product.csv
    ├── output/
    │   └── output.json
    ├── requirements.txt
    ├── .gitignore
    ├── .env
    └── .env.example


### Responsabilidades de los archivos

| Archivo              | Responsabilidad                                 |
| -------------------- | ----------------------------------------------- |
| `main.py`            | Punto de entrada y coordinación de la ejecución |
| `config.py`          | Configuraciones generales del proyecto          |
| `log.py`             | Sistema de logging proporcionado                |
| `web_driver.py`      | Componente de navegación proporcionado          |
| `input/product.csv`  | Archivo de búsquedas                            |
| `output/output.json` | Resultado de la extracción                      |
| `requirements.txt`   | Dependencias necesarias                         |
| `.gitignore`         | Archivos y directorios excluidos de Git         |
| `.env`               | Variables de entorno locales                    |
| `.env.example`       | Ejemplo de variables de entorno requeridas      |

**Aclaración:** Los archivos `log.py` y `web_driver.py` serán proporcionados por el instructor. Los alumnos deberán utilizarlos según corresponda y desarrollar el resto de la solución.

El archivo `.env` no deberá incluirse en el repositorio ni en el Pull Request.

8. Requerimientos técnicos

--------------------------

La solución deberá cumplir con las siguientes condiciones:

* Estar desarrollada en Python.

* Utilizar los componentes proporcionados por el instructor cuando corresponda.

* Mantener una organización modular y comprensible.

* Gestionar correctamente la lectura del archivo CSV.

* Extraer datos reales del sitio objetivo.

* Contemplar productos con múltiples variantes.

* Gestionar búsquedas sin resultados.

* Evitar que un error aislado interrumpa innecesariamente el procesamiento de las demás queries.

* Registrar información relevante de la ejecución mediante el sistema de logging.

* Generar un JSON válido y correctamente estructurado.

* Declarar las dependencias utilizadas en `requirements.txt`.

* Evitar credenciales y configuraciones sensibles directamente en el código.

El proyecto deberá poder ejecutarse desde `main.py` sin necesidad de modificar manualmente las queries dentro del código.

9. Restricciones del examen

---------------------------

### Prohibido el uso de inteligencia artificial

**Está terminantemente prohibido utilizar herramientas de inteligencia artificial durante el examen, bajo cualquier modalidad.**

Esto incluye, entre otras:

* ChatGPT, Claude, Gemini, Copilot y herramientas equivalentes.

* Asistentes de programación con IA.

* Generadores automáticos de código.

* Extensiones de editores que utilicen modelos de IA.

* Herramientas de IA para analizar, corregir o explicar código.

La prohibición comprende tanto la generación de código como la asistencia para resolver errores, diseñar soluciones o interpretar el sitio objetivo.

### Prohibido reutilizar código externo

No se permite:

* Copiar código de proyectos anteriores.

* Reutilizar scrapers previamente desarrollados.

* Copiar soluciones de otros compañeros.

* Utilizar implementaciones completas obtenidas de Internet.

* Compartir código entre participantes.

**Única excepción:** Se permite utilizar el código base proporcionado por el instructor, específicamente `log.py` y `web_driver.py`.

### Recursos permitidos

Se permite consultar documentación técnica para comprender el funcionamiento de lenguajes, librerías, métodos y herramientas.

Por ejemplo:

* Documentación oficial de Python.

* Documentación de librerías utilizadas.

* Referencias de métodos y funciones.

* Documentación técnica sobre CSV, JSON, HTTP y HTML.

La consulta de documentación no autoriza copiar implementaciones completas ni soluciones del examen.

10. Control de versiones y entrega

----------------------------------

La entrega se realizará mediante GitHub.

### Requerimientos de Git

1. Cada alumno deberá crear una rama individual para desarrollar su examen.

2. Todo el trabajo deberá realizarse dentro de esa rama.

3. Los cambios deberán registrarse mediante commits.

4. Al finalizar, el alumno deberá crear un **Pull Request (PR)** hacia la rama principal del proyecto.

5. El Pull Request deberá contener la solución desarrollada durante el examen.

No se permite trabajar directamente sobre la rama principal ni modificar el trabajo de otros participantes.

El Pull Request será considerado la entrega formal del examen.

11. Tiempo disponible

---------------------

<escape>**Duración total: 3 horas (180 minutos).**</escape>

El tiempo comienza a contar desde el inicio oficial del examen.

Durante este período, cada alumno deberá analizar el sitio, desarrollar su solución, realizar las pruebas necesarias y presentar su Pull Request.

No se aceptarán modificaciones posteriores al tiempo establecido, salvo autorización expresa del instructor.

12. Criterios de evaluación

---------------------------

La evaluación considerará los siguientes aspectos:

| Criterio                                       | Ponderación |
| ---------------------------------------------- | ----------- |
| Lectura y procesamiento del CSV                | 10%         |
| Búsqueda y extracción de productos             | 25%         |
| Extracción de variantes y precios              | 25%         |
| Estructura y tipos del JSON                    | 15%         |
| Organización del código y uso de archivos base | 10%         |
| Manejo de errores y logging                    | 10%         |
| Uso correcto de Git y Pull Request             | 5%          |
| **Total**                                      | **100%**    |

Se evaluará tanto el funcionamiento de la solución como la calidad de su implementación.

Una solución que se ejecute sin errores, pero que no respete el esquema solicitado, no será considerada completamente correcta.

El incumplimiento de las restricciones sobre inteligencia artificial, reutilización de código o colaboración no autorizada podrá implicar la invalidación del examen.

13. Solución oficial

--------------------

Una vez finalizado el tiempo del examen, se habilitará la rama:

`rama_answer`

Esta rama contendrá la solución de referencia desarrollada por el instructor.

Los alumnos podrán utilizarla para comparar sus implementaciones, identificar posibles mejoras y revisar los requerimientos que no hayan logrado completar.

**La rama** `**rama_answer**` **estará disponible únicamente después de finalizar el examen.**

* * *

14. Consideraciones finales

---------------------------

Este examen busca integrar los conocimientos adquiridos durante el curso **AutoScraping Essentials**, mediante el desarrollo de un proyecto práctico basado en un sitio real.

Se espera que cada alumno pueda demostrar autonomía para analizar una página web, diseñar una estrategia de extracción, procesar información y generar datos estructurados.

**El objetivo no es únicamente conseguir que el scraper funcione, sino demostrar que se comprenden los fundamentos necesarios para construirlo.**

**¡Éxitos en el examen final!**

_AutoScraping Essentials — Evaluación Final_
