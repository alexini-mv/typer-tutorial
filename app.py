from typing import List, Optional
import typer


app = typer.Typer()


@app.command()
def main(
    user: Optional[List[str]] = typer.Option(
        None,
        rich_help_panel="Config"
    )
):
    """Una asombrosa aplicación CLI
    """
    if not user:
        print("No provided users")
        raise typer.Abort()
    for u in user:
        print(f"Processing user: {u}")


@app.command()
def scrapy(urls: List[str]):
    for idx, url in enumerate(urls, start=1):
        print(idx, " ", url)


@app.command()
def lanzar():
    """Lanza una bonita imagen"""
    typer.launch("EhE0ruYWoAUY85U.jpeg", locate=False)


if __name__ == "__main__":
    app()
