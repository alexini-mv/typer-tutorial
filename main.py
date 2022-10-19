import typer

# Instanciaremos un objeto del tipo Typer que guardará los comandos
app = typer.Typer()


@app.command()
def saludo(name: str) -> None:
    """Saluda a alguien usando su nombre."""
    print(f"¡Hola, {name}!")


@app.command()
def despedida(name: str, formal: bool = False) -> None:
    """Despide a alguien usando su nombre."""
    if formal:
        print(f"¡Buenas noches, Sr./Sra. {name}!")
    else:
        print(f"¡Hasta luego, {name}!")


if __name__ == "__main__":
    app()
