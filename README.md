# Tutorial CLI con typer en python
Breve tutorial para hacer un CLI con python usando la libreria Typer.

## Instalación
Para instalar typer junto con todas sus caracteristicas, en suficiente con:

```console
$ pip install typer[all]
```

## Primer ejemplo
Para construir el primer CLI de la manera más sencilla, solo tenemos que escribir el siguiente código:

```python
import typer

# Definimos una función normal, explicitamente declamos el tipo que recibirá.
def saludo(name: str) -> None:
    print(f"Hola {name}")

if __name__ == "__main__":
    # Aquí escribimos envolvemos la función que ejecutaremos con `typer.run()`
    typer.run(saludo)
```

Esa es la manera más sencilla de construir un CLI. Ahora para escribir uno más complejo, toma la siguiente estructura:

```python
import typer

# Instanciaremos un objeto del tipo Typer que guardará los comandos
app = typer.Typer()

# Agregamos un comando nuevo poniendo el decorador @app.command.
@app.command()
def saludo(name: str) -> None:
    """Saluda a alguien usando su nombre."""
    print(f"¡Hola, {name}!")

# Otro comando
@app.command()
def despedida(name: str, formal: bool = False) -> None:
    """Despide a alguien usando su nombre."""
    if formal:
        print(f"Buenas noches, Sr./Sra. {name}")
    else:
        print(f"¡Hasta luego, {name}!")


if __name__ == "__main__":
    # Ejecutamos el CLI invocado el objeto Typer como función principal
    app()
```

Para agregar un nuevo comando, a cada función le anteponemos el decorador `@app.command`. El comando tomará el nombre de la función,  como argumentos tomará los parámetros declarados en la función. Typer es tan inteligente que sabrá que parámetros son obligatorios u opcionales. Los parámetros serán identificados en el CLI con la nomenclatura de las banderas `--blablabla`.

La documentación de los comandos se declara en los docstrings de cada función, y se podrá visualizar con la bandera `--help` en cada correspondiente comando.


## Comandos de Terminación 
Habrá algunas ocasiones en el que se quiera terminar un programa si se cumple alguna condición, no necesariamente que se levante o no un error, sino interrumpirlo.

Para eso existen dos comandos muy utiles:
* `typer.Exit()`: El CLI termina la ejecución del programa sin ejecutar el resto del código. Puede elevarse (`raise`) ya sea con el código 0 o con código 1, indicando que existió un error.
* `typer.Abort()`: Funciona más o menos de la misma forma que Exit, pero levanta un mensaje de *Abort!* explicito, útil para indicar que se abortó el programa.


## Argumentos Obligatorios CLI
Ya vimos que los argumentos obligatorios CLI se pueden declarar directamente como los argumentos obligatorios de una función en python.
```python
def saludo(name: str)
```
Ahora veremos como declararlo con un objeto de Typer, que será útil para personalizarlo más adelante. Para esto, se utilizará el objeto `typer.Argument()`

De esta forma, la definición en la función de python quedaría como:

```python
def saludo(name: str = typer.Argument(...))
```
donde los *...* indican que un valor es requerido por el usuario.

Ahora, también es posible tener argumentos obligatorios con algún valor por default. Esto es, el argumento es obligatorio para funcionar, pero si no se va algún valor, tiene un valor por defecto. Este valor predefinido se para como primer valor dentro de la definición de objeto `typer.Argument(*valor por defecto*)`. Por ejemplo,

```python
def saludo(name: str = typer.Argument("Juan"))
```

Inclusive es posible pasarle ese valor predefinido, si le pasamos una función que nos retorna el valor deseado.

```python
def get_name():
    return random.choice(["Alex", "Rick", "Mary", "Jane"])

@app.command()
def saludo(name: str = typer.Argument(get_name))
```

Podemos agregarle un mensaje de ayuda que será mostrado al ejecutar el comando con la opción `--help`. Este mensaje describirá al argumento, y puede combinarse perfectamente con la ayuda del comando descrita en el docstring de la función.

```python
def saludo(name: str = typer.Argument("Juan", help="Nombre de la persona que saludarás"), show_default=False)
```
Inclusive con la opción `show_default` puedes pasarle un booleano para mostrar o no el valor por default (si existe) o inclusive personalizarlo con un string personalizado.

También el nombre del argumento que se despliega en la ayuda puede ser personalizado con la opción  `metavar` de `typer.Argument`. Puede incluir emojis.💥 

Con la opción `rich_help_panel` que acepta un string, los argumentos se pueden agrupar en diferentes paneles cuando sean desplegados en la ayuda. Esto ayuda en mucho a la visualización.

Puedes ocultar o no la información desplegada en la ayuda con la opción  `hidden`.

Se le puede indicar a typer que tome el valor de un argumento de una o varias variables de entorno, con la opción `envvar`, además de indicar si será mostrada o no en la información de ayuda.

```python
def saludo(name: str = typer.Argument(..., envvar=["NAME", "GOD_NAME"],  show_envvar=False)
```

## Opciones CLI
De forma muy similar a los argumentos CLI, podemos declarar a las opciones CLI mediante el objeto `typer.Option()`, donde el primer argumento tomará el valor por default.

```python
@app.command()
def saludo(
    name: str,
    lastname: str = typer.Option("", help="Apellido de la persona que saludarás"),
    formal: bool = typer.Option(False, help="Saludo formal")):
```

Al igual como vimos antes, es posible agrupar en la ayuda a las opciones mediante paneles, con la opción `rich_help_panel`.

Las opciones CLI se pueden invocar mediante `--notation` de doble guión, las opciones tambien pueden ser opcionales u obligatorias, es decir, que necesite pasarles un valor explicitamente, mediante pasandole *...* en la primera opción de `typer.Option()`

```python
@app.command()
def saludo(
    name: str,
    lastname: str = typer.Option(..., help="Apellido de la persona que saludarás"),
    formal: bool = typer.Option(False, help="Saludo formal")):
```

Y se invocará como:
```console
$ python main.py saludo Alejandro --lastname Peréz
```
Si no se le pasa ningún valor a la opción CLI, lanzará un error. En lugar de eso, se le puede agregar la opción `prompt=True` para que espere recibir un valor desde el prompt y no lanzar el error. También es posible pasarle un string para personalizar el mensaje que se desplejará en el prompt al pedir el valor.

Adicionalmente, podemos pedir que el prompt se lance por segunda vez para pedir una confirmación con `confirmation_prompt=True`. Esto es relevante cuando se pide un valor delicado, que no permite errores como número de cuentas, contraseñas, etc.

Cuando se trata de contraseñas, se puede ocultar los carácteres del input con la opción `hide_input`.

Se pueden declarar una personalización en el nombre de la opción CLI. Por defecto, typer tomará el nombre de la función como nombre del parámetro declarado en la función, pero se puede personalizar pasandole como segundo argumento posicional del `typer.Option`

```python
@app.command()
def saludo(
    name: str,
    lastname: str = typer.Option(..., "--apellido", "-a" help="Apellido de la persona que saludarás"),
    formal: bool = typer.Option(False, help="Saludo formal")):
```
De la misma forma, se puede declarar un nombre corto (una letra precedida por un solo guión), que tiene la ventaja de poder unirse con junto con otras nombres cortos de una sola letra. (Recuerdese el comando `$ ls -lah` en Linux).

### CLI Opciones con Callbacks y Contexto
Habrá veces que se quiera tratar o validar el valor de los argumentos bajo alguna lógica, antes de ser enviados a la función principal. Para eso, puede ser validados por otra función por medio de callback.

```python
def name_callback(value: str):
    if value != "Alejandro":
        raise typer.BadParameter("Sólo el nombre de Alejandro está permitido")
    return value

@app.command()
def main(name: str = typer.Option(..., 
                                  callback=name_callback)
        ):
    print(f"Hello {name}")
```
Lo que hace es que el valor es pasado a la función callback, es verificado, modificado y tratato. Y el valor que retorna el callback es el que finalmente captura la función principal.

Al usar los callbacks, se generará un comportamiento no deseado al solicitar el "autocompletado" al presionar el tabulador. Internamente, el autocompletado envia ciertos datos para que se ejecute el programa y regrese las opciones disponibles. Pero al invocar el callback, se ejecutaran las funciones sin tener los argumentos completos, por lo que generará un error.

Para solventarlo, se hace uso del objeto `typer.Context`. Este objeto tiene información adicional acerca de la ejecución del programa que servirá para que no se generen errores, ya que identifica cuando se utiliza el autocompletado o se ejecuta el programa.

```python
def name_callback(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return

    if value != "Alejandro":
        raise typer.BadParameter("Sólo el nombre de Alejandro está permitido")
    return value
```
El objeto `typer.Context.resilient_parsing` es True cuando se maneja un autocompletado, por lo que retorna la función sin ejecutar el resto del código del callback. En cambio, su valor es False cuando se invoca como un programa normal, por lo que ignorará el primer return y ejecutará el resto del programa.

Es casos especiales, tal vez quedrá saber que argumento es el que se está validando en el callback. En ese caso puedes declarar entre los argumentos del Callback el objeto `typer.CallbackParam`, el cual tendrá el atributo `typer.CallbackParam.name` que tendrá justamente el nombre del argumento desde el cual fue invocado dicho callback.

Algunas veces, cuando en varios argumentos los pasamos por callback, su validación se hará según el orden en el que se pasen los parámetros en la invocación del programa principal. Habrá veces que quedremos que al levantarse alguna bandera, no importando el orden, se ejecute primero su callback. Para eso, dentro del objeto `typer.Option` se le agregará la opción `is_eager=True`, lo que indicará que siempre se debe ejecutar primero esa validación antes que todas las demás.

Para sugerir las opciones validas utilizando el autocompletado con [TAB][TAB], se puede pasar un callback dentro de la opción `autocompletion=completion_names`. Este callback será invocado cuando se presione los tabuladores.

### Formatos dentro del decorador @app.command

Se puede agregar una descripción general de la app dentro de la opción de ayuda:
```python
app = typer.Typer(help="Awesome CLI user manager.")
```

Tambien se puede reescribir la ayuda de cada comando y no usar el docstring de la función, para mostrarlo en el --help.

```python
@app.command(help="Create a new user with USERNAME.")
```

Podemos de manera fácil y sencilla mostrar que se depreca algún comando de la siguente manera:

```python
@app.command(deprecated=True)
```

Podemos hacer que la ayuda se muestre con el formato de texto enriquecido de Rich, declarandolo desde el principio el instanciar la app:

```python
app = typer.Typer(rich_markup_mode="rich")
```
O podemos usar también el formato de Markdown:

```python
app = typer.Typer(rich_markup_mode="markdown")
```

Podemos agrupar los comandos en grupos que sean similares, para tener el texto de la ayuda más ordenado

```python
@app.command(rich_help_panel="Utils and Configs")
```

Al igual que se puede ordenar los comandos por grupos, también se pueden ordenar las argumentos o las opciones para ser mostrados en la ayuda, con la misma opción.

Finalmente, se puede agregar un epilogo, mensaje final en la página de la ayuda, con la siguiente opción:
```python
@app.command(epilog="Made with :heart: in [blue]Venus[/blue]")
```
### Personalizando el nombre del comando
Se puede personalizar el nombre del comando, y que no tome el nombre de la función de python para asignarle el nombre al comando. Esto se hace pasandole un str posicional al decorador, de la siguiente forma:

```python
@app.command("create")
def cli_create_user(username: str):
```

### Callback globales
Se puede ejecutar un callback independientemente del comando o subcomando que se invoca. Para esto se puede invocar de dos formas diferentes, pero equivalentes.

La primera es mediante el decorador `@app.callback()` de la siguiente forma:

```python
@app.callback()
def main(verbose: bool):
```
La app registra que existe un callback global y se que siempre se ejecutará.    

La otra forma es declarandolo directamente durante la instanciación del objeto Typer:

```python
def callback():
    print("Algo bonito")

app = typer.Typer(callback=callback)
```
Ambas formas son equivalentes.

Si se pasa un callback al instanciar el objeto Typer, este puede ser sobreescrito después con el decorador `@app.callback()`.

Normalmente se utiliza el callback para pasarle a la aplicación CLI un docstring que se desplegará durante la ayuda.

```python
def callback():
    """Una asombrosa aplicación CLI."""

app = typer.Typer(callback=callback)
```

### Tipos de Parámetros CLI
Typer procurará parsear los parámetros al tipo de dato que se declara en python. Los tipos de datos validos para los parámetros pueden ser:

1. **Números**
```python
def main(id: int = typer.Argument(..., min=0, max=1000),
         rank: int = typer.Option(0, max=10, clamp=True),
         score: float = typer.Option(0, min=0, max=100, clamp=True),
):
```
A los tipos numéricos pueden recibir opciones para definir un rango máximo o mínimo validos, y levantar una excepción si se pasa un valor fuera del rango.

Otra opción es usar `clamp=True` que hace que sí se da un valor numérico fuera del rango, ajustarlo al número más cercano dentro del rango, ya sea el máximo o el mínimo.

2. **Booleanos**
Como ya vimos anteriormente, al declarar un argumento del tipo booleano, nos genera dos banderas (--bandera, --no-bandera). Para evitar que nos genere las dos banderas, debemos de definir explicitamente el nombre de la bandera:

```python
def main(bandera: bool = typer.Option(False, "--bandera")):
```

Inclusive, si se quiere tener las dos banderas, se pueden personalizar ambas banderas al mismo tiempo para que tengan sentido, de la siguiente manera:

```python
def main(aceptar: bool = typer.Option(False, "--aceptar/--rechazar", "-f/-F")):
```
Tanto para la bandera de nombre largo, como para el nombre corto, se separa la opción positiva / negativa.

Sí se quiere mostrar solamente la opción negativa en la ayuda, se puede declarar de la siguiente forma:

```python
def main(in_prod: bool = typer.Option(True, " /--dev", " /-d")):
```
Tenga en cuenta que hay un espacio en blanco antes del slash con la opción negativa " /--dev".

### DateTime
Se puede aceptar strings y se sean parseados como objetos datatime.

```python
from datetime import datetime
import typer

def main(birth: datetime):
```
De forma automática, Typer acepta los siguiente formatos:

* %Y-%m-%d
* %Y-%m-%dT%H:%M:%S
* %Y-%m%d %H:%M:%S

Pero se puede personalizar a cualquier otro formato que se quiera, pasandole la opción format de la siguiente forma:
```python
def main(
    launch_date: datetime = typer.Argument(
        ..., 
        formats=["%m/%d/%Y"]
    )
):
```
Que en este caso, acepta el formato: Primero el mes, después el día y finalmente el año, separados por slash.

### Lista para elegir: Enum - Choices
Para poder desplegar opciones que se pueden elegir a partir de una lista de valores aceptados, se usa la clase estandar `enum.Enum`. 

Para eso, creamos una clase que hereda de `Enum` con las opciones aceptados:

```python
from enum import Enum

class RedesNeuronal(str, Enum):
    full = "full"
    conv = "conv"
    lstm = "lstm"

def main(
    network: RedesNeuronal = typer.Option(RedesNeuronal.full,  
                                          case_sensitive=False)
    ):
```
Con la opción `case_sensitive` se puede especificar si se desactiva la sensibilidad a mayúsculas o minúsculas.

### Rutas (Path)
También es posible parsear rutas, con la ayuda de la libreria estandar `pathlib.Path`, se la siguiente forma:

```python
from pathlib import Path
from typing import Optional

def main(config: Optional[Path] = typer.Option(None)):
```
Como el objeto parseado es una instancia de `Path`, tiene todos su métodos para las validaciones y manipulaciones. Sin embargo, desde el parseo se pueden predefinir las validaciones.

```python
def main(
    config: Optional[Path] = typer.Option(None,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,)
):
```
### Objetos Archivo
Typer integra un tipo de dato que es un objeto de archivo (file-like object), similar al retornado al usar `with open("archivo.txt") as f`, f es ese tipo de objeto. Typer integra una clase especial según la tarea que se requiera realizar, por ejemplo:

1. **Leer un archivo** (typer.FileText)
```python
def main(config: typer.FileText = typer.Option(...)):
    for line in config:
        print(f"Config line: {line}")
```
2. **Escribir sobre un archivo**
```python
def main(config: typer.FileTextWrite = typer.Option(...)):
    config.write("Some config written by the app")
```
3. **Leer y escribir en un archivo binario**
```python
def main(file: typer.FileBinaryRead = typer.Option(...)):
    pass

def main(file: typer.FileBinaryWrite = typer.Option(...)):
    pass
```
4. **Personalización del modo**
```python
# Abrimos el archivo para append nueva info al final del archivo
def main(config: typer.FileText = typer.Option(..., mode="a")):
    config.write("This is a single line\n")
```

### Multiples valores Opcionales de entrada 
Puede declarar una opción CLI que se puede usar varias veces y luego obtener todos los valores.

Para eso se usará la forma estandar List que esperará una lista de strings o enteros o flotantes:

```python
from typing import List, Optional

def main(user: Optional[List[str]] = typer.Option(None)):
```
Como son parámetros opcionales, se pasarán al CLI de la siguiente forma:

```console
$ python main.py --user Camila --user Rick --user Morty
```

También se puede pasar en lugar de una lista, una tupla, especificando el número de elementos y el tipo de dato que tendrá la tupla.

```python
from typing import Tuple

def main(user: Tuple[str, int, bool] = typer.Option((None, None, None))):
```
Pasandolo por el CLI de la siguiente forma:
```console
$ python main.py --user Camila 50 yes
```

### Multiples valores para argumentos
La forma anterior fueron parámetros Opcionales. Ahora veremos como pasar Argumentos con multiples valores. También se hace uso del tipo `List`

```python
def main(files: List[Path]):
```

De la misma forma, puede aceptar una tupla, que especifique exactamente el número de argumentos y su tipo que se pasarán:

```python
def main(
    names: Tuple[str, str, str] = typer.Argument(
        ("Harry", "Hermione", "Ron"), 
        help="Selecciona tres personajes de Harry Potter."
    )
):
```
### Abrir un archivo o lanzar una página o aplicación
Puede iniciar aplicaciones desde su programa CLI con `typer.launch()`. Se iniciará la aplicación adecuada según la URL o el tipo de archivo que le pase:

```python
def lanzar():
    """Lanza una bonita imagen"""
    typer.launch("EhE0ruYWoAUY85U.jpeg")
```
Se puede agregar la opción `locate=True`, para que se abra un explorador de archivos justamente en el directorio donde se encuentra el archivo.

## Referencias
* Documentación oficial de [Typer](https://typer.tiangolo.com/)