from . import ichunqiu, anheng

import click
from verboselogs import VerboseLogger as getLogger

logger = getLogger("AFA")


@click.command("build")
@click.argument("dir", default=".")
@click.argument("output", default=".")
@click.option("--format", default="anheng", type=click.Choice(["anheng", "ichunqiu"], case_sensitive=False))
@click.option("--no-directory", default=False)
@click.option("--no-zip", default=False)
@click.argument("flag", required=False)
def build(format: str, dir: str, output: str, no_zip: bool, no_directory: bool, flag=""):
    """Build project directory"""
    
    if format.lower() == "anheng":
        platform = anheng
    elif format.lower() == "ichunqiu":
        platform = ichunqiu
    else:
        platform = anheng
    platform.build(dir, output, no_zip, no_directory, flag)
