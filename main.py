import typer
from rich import print
# Instanciaremos un objeto del tipo Typer que guardará los comandos
app = typer.Typer(
    rich_markup_mode="rich",
    help="Ejemplo de una aplicación CLI usando la libreria Typer de Python.",
)

# Agregamos un comando a la app CLI principal.
# Los argumentos y opciones de este comando, se declaran directamente
# en la función.

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


def name_callback(ctx: typer.Context, param: typer.CallbackParam, valor: str):
    if ctx.resilient_parsing:
        return

    print(f"Validando {param.name}")
    return valor.upper()


def completion_lastname():
    return ["Martínez", "Hernádez", "Pérez", "Méndez", "Flores"]


@app.command(rich_help_panel="Utils")
def saludo(
    name: str = typer.Argument(...,
                               help="Nombre de alguien muy famoso.",
                               show_default=False,
                               metavar="✨username✨",
                               hidden=False,
                               envvar="NAME",
                               show_envvar=False,
                               callback=name_callback,
                               rich_help_panel="Información Personal"),
    lastname: str = typer.Option("Perez",
                                 "--apellido",
                                 "-a",
                                 help="Apellido de alguien muy famoso.",
                                 show_default=False,
                                 prompt="¿Cuál es tu apellido?",
                                 confirmation_prompt="Escribe de nuevo tu apellido",
                                 autocompletion=completion_lastname,
                                 rich_help_panel="Información Personal"),
    password: str = typer.Option(None,
                                 help="Tu contraseña super segura.",
                                 prompt="¿Cuál es tu contraseña?",
                                 confirmation_prompt="Repite tu contraseña",
                                 hide_input=True,
                                 show_default=False,
                                 rich_help_panel="Información Personal"),
    version: bool = typer.Option(False,
                                 "--version",
                                 "-v",
                                 callback=version_callback,
                                 is_eager=True,
                                 rich_help_panel="Ayuda")
) -> None:
    """Saluda a alguien usando su nombre."""
    print(f"¡Hola, {name} {lastname}!")

# Otro nuevo comando agregado a la app.


@app.command(
    rich_help_panel="Utils",
    epilog="Te extrañaré con todo mi :heart: en [bold red]Marte.[/bold red]"
)
def despedida(name: str, formal: bool = False) -> None:
    """Despide a alguien usando su nombre."""
    if formal:
        print(f"¡Buenas noches, Sr./Sra. {name}!")
    else:
        print(f"¡Hasta luego, {name}!")


@app.command(deprecated=True)
def main():
    """Imprime un bonito mensaje con el estilo del paquete [bold green]Rich[/bold green]"""
    print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")
    raise typer.Abort()


if __name__ == "__main__":
    app()
