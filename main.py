import typer
from rich import print
# Instanciaremos un objeto del tipo Typer que guardará los comandos
app = typer.Typer()

# Agregamos un comando a la app CLI principal.
# Los argumentos y opciones de este comando, se declaran directamente
# en la función.


@app.command()
def saludo(
    name: str = typer.Argument("Juan",
                               help="Nombre de alguien muy famoso.",
                               show_default=False,
                               metavar="✨username✨",
                               hidden=False,
                               envvar="NAME",
                               show_envvar=False),
    lastname: str = typer.Option("Perez",
                                 "--apellido",
                                 "-a",
                                 help="Apellido de alguien muy famoso.",
                                 show_default=False,
                                 prompt="¿Cuál es tu apellido?",
                                 confirmation_prompt="Escribelo de nuevo"),
    password: str = typer.Option(...,
                                 help="Tu contraseña super segura.",
                                 prompt="¿Cuál es tu contraseña?",
                                 confirmation_prompt="Repite tu contraseña",
                                 hide_input=True,
                                 show_default=False,)
) -> None:
    """Saluda a alguien usando su nombre."""
    print(f"¡Hola, {name} {lastname}!")

# Otro nuevo comando agregado a la app.


@app.command()
def despedida(name: str, formal: bool = False) -> None:
    """Despide a alguien usando su nombre."""
    if formal:
        print(f"¡Buenas noches, Sr./Sra. {name}!")
    else:
        print(f"¡Hasta luego, {name}!")


@app.command()
def main():
    print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")
    raise typer.Abort()


if __name__ == "__main__":
    app()
