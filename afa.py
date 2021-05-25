#!/usr/bin/env python3
from build import build
from init import init
import click
import coloredlogs
from verboselogs import VerboseLogger as getLogger
coloredlogs.install(fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s')

logger = getLogger("AFA")

@click.group()
@click.option("--verbose", "-v", count=True)
def cli(verbose):
    """Auto fuck anheng"""
    logger.setLevel("WARNING")
    if verbose == 1:
        logger.setLevel("INFO")
    elif verbose >= 2:
        logger.setLevel("DEBUG")
    pass

cli.add_command(init)
cli.add_command(build)

if __name__ == "__main__":
    cli()