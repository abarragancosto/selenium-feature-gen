> Este artículo explica cómo convertir un archivo `.feature` y una captura del DOM de una página web en código Java completamente funcional, listo para ser ejecutado con Selenium. Todo el proceso se realiza localmente utilizando el modelo Llama 3.2 a través de Ollama, evitando así el uso de APIs externas y preservando la confidencialidad de los datos.
> 
> El flujo propuesto permite generar automáticamente las Step Definitions y los Page Objects necesarios para ejecutar las pruebas, con tiempos de respuesta razonables incluso en equipos con recursos limitados.

## 1. Motivación

En el primer artículo de esta serie ya mostramos cómo transformar requisitos escritos en lenguaje natural en archivos `.feature` utilizando un modelo de lenguaje ejecutado en local. Hoy damos un paso más: a partir de ese archivo `.feature` generado, vamos a obtener todo el código necesario para lanzar una prueba automática con Selenium. Sin escribir ni una línea de código manualmente.

Este flujo permite ir directamente **de requisitos a código ejecutable**, manteniendo todo el proceso en un entorno local. Esto significa:

- Sin necesidad de subir datos sensibles a la nube.  
- Sin depender de APIs externas ni servicios de terceros.  
- Sin comprometer la confidencialidad del DOM o los escenarios de prueba.  

La web que queremos testear se despliega también en local, y el modelo Llama 3.2 trabaja exclusivamente con los archivos locales generados: el `.feature` y la estructura del DOM exportada en JSON. Esta estrategia garantiza un entorno cerrado y seguro, ideal para proyectos que manejan información privada o para equipos que buscan independencia tecnológica.

## 2. Requisitos previos

Antes de ejecutar el flujo completo, es necesario tener instaladas algunas herramientas clave:

- **Ollama + Llama 3.2**  
  Para servir el modelo de lenguaje en local. ( Si ya lo instalaste en el primer artículo, no hace falta instalarlo puesto que ya lo tienes)
  ```bash
  brew install ollama       # macOS
  ollama pull llama3:2
  ```

- **Playwright para Python**  
  Se utilizará para capturar el DOM de la web. Se utiliza Playwright ya que para futuros proyectos lo utilizaremos.
  ```bash
  pip install playwright
  playwright install chromium
  ```

- **Maven 3.9 o superior**  
  Para compilar y lanzar las pruebas automáticas.
  ```bash
  brew install maven       # macOS
  ```

- **Git**  
  Para clonar los repositorios necesarios.
  ```bash
  git clone <url>
  ```

> En sistemas Linux o Windows, los comandos son equivalentes utilizando el gestor de paquetes correspondiente (`apt`, `choco`, etc.).

## 3. Guía paso a paso

### 3.1 Clonar el proyecto

```bash
git clone https://github.com/abarragancosto/selenium-feature-gen.git
```
Para facilitar la prueba, se han añadido dentro del mismo repositorio todo el código necesario para la prueba. El proyecto consta de:

- **`login_example`**  
  Contiene una página HTML sencilla con un formulario de login. Se utilizará como aplicación bajo prueba y se servirá localmente.

- **`selenium-bdd-base`**  
  Proyecto base en Java con Maven y estructura BDD. Aquí se ubicarán los Page Objects y Steps generados, y desde aquí se ejecutarán las pruebas automáticas.

- **`generate_code_selenium.py`**  
  Código Python encargado de:
  - Capturar el DOM con Playwright.
  - Invocar al modelo Llama 3.2 con el contexto adecuado.
  - Generar automáticamente el código Java (Page Object + Step Definitions).
- **`dom_snapshot.py`**  
  Código Python encargado de:
  - Capturar el DOM con Playwright.

### 3.2 Iniciar los servicios necesarios

#### a) Servir la web de ejemplo

```bash
cd login_example
python -m http.server 8000 &
cd ..
```

Esto dejará la web accesible en `http://localhost:8000/login.html`.

#### b) Iniciar el modelo Llama 3.2

```bash
ollama serve &
```

Y si no lo has descargado aún:

```bash
ollama pull llama3:2
```

### 3.3 Capturar el DOM
Para instalar dependencias:
```bash
pip install playwright
playwright install chromium
```

Para ejecutar la captura del DOM
```
python dom_snapshot.py http://localhost:8000/login.html
```
Esto navegará hasta la pantalla de login y generará todo el DOM en un fichero llamado dom.json

### 3.4 Generar el código con IA
Desde el proyecto llm-code-gen, ejecutamos el script que genera automáticamente el código Java necesario para lanzar las pruebas:

```bash
python generate_code_selenium.py ./selenium-bdd-base/src/test/resources/features/login.feature dom.json \\
  --po-dir ./selenium-bdd-base/src/main/java/pageobjects \\
  --steps-dir ./selenium-bdd-base/src/test/java/steps
  ```
Este script acepta los siguientes argumentos:

- **`feature`**  
  Ruta al archivo .feature que contiene el escenario en lenguaje Gherkin.

- **`dom`**  
  Archivo dom.json generado anteriormente con Playwright; contiene la estructura HTML de la página a testear.

- **`--po-dir`**  
  Directorio donde se guardará el Page Object generado (LoginPage.java).
  Por defecto: src/main/java/pageobjects.

- **`--steps-dir`**  
  Directorio donde se guardarán las Step Definitions (LoginSteps.java).
  Por defecto: src/test/java/steps.

Tras la ejecución, encontrarás el código generado en las rutas indicadas, listo para ser compilado y probado con Maven.


### 3.5 Ejecutar las pruebas

```bash
cd selenium-bdd-base
mvn test
```

El informe de resultados en formato HTML estará disponible en:

```
target/cucumber-report.html
```

Tras el lanzamiento, también se vería por consola el resultado de los test.

## 4. Próximos pasos

Este flujo ya nos permite generar pruebas automatizadas funcionales desde requisitos, sin intervención manual y manteniendo la privacidad de los datos. El siguiente objetivo será **completar el ciclo con un sistema de reporting automatizado**.

La idea es generar un resumen a partir del informe HTML de Cucumber, procesarlo con el modelo en local y enviarlo automáticamente por correo. De esta forma, cerraremos todo el flujo: desde la especificación de requisitos hasta la comunicación final del resultado, todo asistido por inteligencia artificial y sin depender de servicios externos.

## 5. Líneas de mejora

Este proyecto demuestra el flujo en un escenario muy acotado: una sola pantalla con un formulario de login. Es una prueba de concepto simple, pero funcional.

En los próximos artículos abordaremos casos más complejos que incluyan **navegación entre pantallas y flujos dinámicos**. Para ello, utilizaremos una variante más avanzada del proyecto con **Playwright MCP**, una extensión que permitirá:

- Recorrer múltiples pantallas automáticamente.  
- Capturar y entender flujos de navegación.  
- Generar Page Objects y Steps de forma encadenada.  

Esto abre la puerta a generar suites completas de testing funcional a partir de modelos de lenguaje, con un nivel de autonomía mucho mayor.

## 6. Conclusión

Este ejemplo demuestra cómo se puede automatizar la generación de código de pruebas funcionales a partir de un simple archivo `.feature`, pero no pretende reemplazar el criterio ni la experiencia de un QA experto.

El código generado es una base funcional que **debe ser revisada, mejorada y adaptada**. En escenarios reales, será necesario **reutilizar Page Objects entre pantallas**, aplicar buenas prácticas de diseño, validar selectores y mantener una arquitectura mantenible a largo plazo.

Lo que aquí mostramos es un primer paso hacia una forma más ágil y asistida de trabajar, sin perder el control ni la calidad técnica.

## 7. ¿Te interesa este enfoque?

Este artículo forma parte de una serie en la que exploro cómo aplicar modelos de lenguaje en local para facilitar tareas complejas de automatización sin comprometer la privacidad de los datos.

Me interesa saber tu opinión:  
- ¿Te resulta útil este tipo de enfoque?
- ¿Qué te gustaría que profundizase en los siguientes artículos?
- ¿Quieres ver ejemplos más complejos o enfocados a otros entornos (API, móviles, CI/CD...)?

Puedes dejar tu feedback en comentarios, mensajes o directamente en el repositorio.
