#!/usr/bin/env python3

import argparse, pathlib, re, requests, textwrap

MODEL = "llama3.2"
URL   = "http://localhost:11434/api/generate"
REGEX = r'```java(?:\s+title="([^"]+)")?\s*\r?\n(.*?)```'

def pkg_from_dir(dir_path:str) -> str:
    p = pathlib.Path(dir_path).resolve()
    parts = p.parts
    return ".".join(parts[parts.index("java")+1:] if "java" in parts else parts)

ST_PROMPT = textwrap.dedent("""Eres un QA Automation senior.
Crea SOLO las Step Definitions Java para Cucumber v7 usando Selenium:

* Archivo: {name}Steps.java
* Paquete: {steps_pkg}
* Imports obligatorios:
    import io.cucumber.java.en.*;
    import {po_pkg}.{name}Page;
    import support.DriverFactory;
    import org.openqa.selenium.WebDriver;

* Declara:
    private final WebDriver driver = DriverFactory.getDriver();
    private final {name}Page page = new {name}Page(driver);

* NO inicialices ni cierres driver aquí; eso lo hace Hooks.java.
* Implementa métodos Given/When/Then en español según el escenario.
INSTRUCCIONES EXTRA (obligatorias)

* Genera **un único método Given/When/Then por frase única** del Gherkin.
  - Si la frase se repite en varios escenarios, **reutiliza el mismo método**.
  - No crees “Login válido” y luego “Login válido (2)”.
* Convierte los literales entre comillas en parámetros. Los parámetros corchete abierto string corchete cerrado
* El nombre del método debe ser en minúscula y descriptivo
  (por ejemplo, **introduceCredenciales(String,String)**).
* NO dupliques imports, NO dupliques código.
Devuelve un bloque:
```java title="{name}Steps.java"
...
```
Sin texto extra.

DOM:
{dom}
Gherkin:
{feature}
""")

PO_PROMPT = textwrap.dedent("""Eres un QA Automation senior.
Crea SOLO el Page Object Java basado en las Step Definitions adjuntas:

* Archivo: {name}Page.java
* Paquete: {po_pkg}
* Imports obligatorios:
    import org.openqa.selenium.support.PageFactory;
    import org.openqa.selenium.support.FindBy;
    import org.openqa.selenium.WebElement;
    import org.openqa.selenium.WebDriver;
    
* Constructor recibe WebDriver driver y llama a PageFactory.initElements(driver,this)
* Implementa TODOS los métodos invocados en las Steps
* Usa @FindBy(id="...") sobre WebElements protected siempre que haya elementos identificables por id.

Devuelve un bloque:
```java title="{name}Page.java"
...
```
Sin texto extra.

DOM:
{dom}

Step Definitions:
{steps_code}
""")

def ask(prompt:str)->str:
    r = requests.post(URL,json={"model":MODEL,"prompt":prompt,"stream":False},timeout=1800)
    r.raise_for_status()
    return r.json()["response"]

def extract(resp:str, default:str):
    m=re.search(REGEX, resp, re.S)
    if not m: return default, None
    fname, code = m.groups()
    return fname or default, code.rstrip()+"\n"

def main():
    import sys
    ap=argparse.ArgumentParser()
    ap.add_argument("feature"); ap.add_argument("dom")
    ap.add_argument("--po-dir",default="src/main/java/pageobjects")
    ap.add_argument("--steps-dir",default="src/test/java/steps")
    args=ap.parse_args()

    name=pathlib.Path(args.feature).stem.capitalize()
    dom=pathlib.Path(args.dom).read_text()[:4000]
    feature=pathlib.Path(args.feature).read_text()
    po_pkg=pkg_from_dir(args.po_dir)
    st_pkg=pkg_from_dir(args.steps_dir)

    # Steps
    steps_prompt = ST_PROMPT.format(name=name,steps_pkg=st_pkg,po_pkg=po_pkg,
                                    dom=dom,feature=feature)
    steps_fname, steps_code = extract(ask(steps_prompt), f"{name}Steps.java")
    if not steps_code:
        sys.exit("LLM no devolvió Steps")

    # Page Object
    po_prompt = PO_PROMPT.format(name=name,po_pkg=po_pkg,dom=dom,steps_code=steps_code)
    po_fname, po_code = extract(ask(po_prompt), f"{name}Page.java")
    if not po_code:
        sys.exit("LLM no devolvió Page Object")

    pathlib.Path(args.po_dir).mkdir(parents=True,exist_ok=True)
    pathlib.Path(args.steps_dir).mkdir(parents=True,exist_ok=True)
    (pathlib.Path(args.steps_dir)/steps_fname).write_text(steps_code)
    (pathlib.Path(args.po_dir)/po_fname).write_text(po_code)
    print("[OK]",po_fname,"y",steps_fname)

if __name__=="__main__":
    main()
