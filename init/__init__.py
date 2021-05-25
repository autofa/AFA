import os
import os.path
import subprocess

import click
from verboselogs import VerboseLogger as getLogger

logger = getLogger("AFA")


@click.command("init")
@click.argument("dir", default=".")
@click.argument("template", default="https://github.com/autofa/AFA-Template-Base")
def init(dir: str, template: str):
    """Init project directory"""
    dir = os.path.abspath(dir)
    try:
        os.mkdir(dir)
        logger.info(f"Create directory {dir}")
    except FileExistsError:
        try:
            if len(os.listdir(dir)):
                logger.error(
                    f"Directory {dir} existing, remove and try again.")
                exit(1)
        except NotADirectoryError:
            logger.error("Name is occupied by file, remove and try again.")
            exit(1)
    logger.info("Clone template")
    subprocess.check_call(["git", "clone", template, dir])
    subprocess.check_call(["git", "remote", "remove", "origin"], cwd=dir)
    logger.success("Success")
