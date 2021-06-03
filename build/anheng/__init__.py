import os
import os.path
from os.path import join
import shutil
import tempfile
from . import meta, xlsx, doc, docker

import click
import yaml
from dockerfile_parse import DockerfileParser
from verboselogs import VerboseLogger as getLogger

from data.config import Config
from data.problem import Problem

SLASH_N = "\n"

logger = getLogger("AFA")


def missing_file(name: str):
    logger.error(f"Missing {name} in directory")
    exit(1)


def capture_missing_file(f):
    def _f(*args, **kargs):
        try:
            return f(*args, **kargs)
        except FileNotFoundError as e:
            missing_file(e.filename)
    return _f

@capture_missing_file
def build(dir: str, output: str, no_zip: bool, no_directory: bool, flag=""):
    """Build project directory"""
    dir = os.path.abspath(dir)
    yaml_path = join(dir, "config.yaml")
    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)
    if not config["problem"].get("name"):
        config["problem"]["name"] = os.path.basename(dir)
    problem = Problem(**config["problem"])
    problem.flag = problem.flag or flag or find_flag(dir)
    config = Config(**config["basic"], problem=problem)
    gen_directory = join(output, config.generated_name)
    gen_zip = join(output, config.generated_name)
    if os.path.exists(gen_directory):
        if click.confirm(f"Output directory {gen_directory} exist, remove?", default=True):
            shutil.rmtree(gen_directory)
            os.makedirs(gen_directory, exist_ok=True)
        else:
            logger.warning(f"Use temp directory {gen_directory}")
            gen_directory = tempfile.mkdtemp(prefix=config.generated_name)
    os.makedirs(gen_directory, exist_ok=True)
    copy("Video", join(dir, "video"), join(gen_directory, "解题视频"))
    copy("Attachments", join(dir, "attachments"), join(gen_directory, f"{config.problem.type}附件"))
    copy("Exploit", join(dir, "exp"), join(gen_directory, "exp"))
    copy("Source", join(dir, "problem", "app"), join(gen_directory, "源代码"))
    logger.info("Generate meta")
    meta.generate(dir, config, gen_directory)
    logger.info("Generate xlsx")
    xlsx.generate(dir, config, gen_directory)
    logger.info("Generate writeup")
    doc.generate(dir, config, gen_directory)
    logger.info("Generate docker")
    docker.generate(dir, config, gen_directory)
    logger.success("Build Finish")
    if not no_zip:
        if os.path.exists(gen_zip+".zip"):
            if click.confirm(f"Output zip {gen_zip+'.zip'} exist, remove?", default=True):
                os.unlink(gen_zip+'.zip')
            else:
                logger.warning(f"Skip output zip")
                no_zip = True
    if not no_zip:
        logger.success("Create zip archive")
        shutil.make_archive(gen_zip, "zip", gen_directory)
    if no_directory:
        shutil.rmtree(gen_directory)


def find_flag(dir: str):
    try:
        with open(join(dir, "problem", "Dockerfile"), "r") as f:
            dfp = DockerfileParser()
            dfp.content = f.read()
            flag = dfp.envs.get("FLAG")
            if flag:
                return flag
            flag = dfp.envs.get("flag")
            if flag:
                return flag
        with open(join(dir, "problem", "docker-compose.yml")) as f:
            docker_compose = yaml.safe_load(f)
            for services in docker_compose["services"].values():
                env = services["environment"]
                if env:
                    for e in env:
                        [name, value] = e.split("=", 1)
                        if name.upper() == "FLAG":
                            return value
    except (FileNotFoundError, KeyError):
        pass
    return ""


def copy(name: str, dir: str, dest: str):
    logger.info(f"Copy {dir} to {dest}")
    if os.path.isdir(dir):
        shutil.copytree(dir, dest)
    else:
        os.mkdir(dest)
