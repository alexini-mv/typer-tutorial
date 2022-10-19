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

## Referencias
* Documentación oficial de [Typer](https://typer.tiangolo.com/)