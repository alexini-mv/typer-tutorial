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



## Referencias
* Documentación oficial de [Typer](https://typer.tiangolo.com/)