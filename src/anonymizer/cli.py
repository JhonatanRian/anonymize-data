from rich.console import Console
from typer import Typer, Argument

from .anonymizer import MaskString

console = Console()
app = Typer()


@app.command()
def anonymize(
    value: str = Argument(help="The string you want to anonymize"),
    type_mask: str = Argument(default="string", help="The type mask to use"),
    size_anonymization: float = Argument(
        default=0.7, help="The size anonymization factor"
    ),
) -> None:
    """
    cli anonymization string
    """
    string_mask = MaskString(
        value, type_mask, size_anonymization=size_anonymization
    ).anonymize()
    console.print(string_mask, style="#ccc010 bold")
