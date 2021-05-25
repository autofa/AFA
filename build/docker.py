import re
from data.config import Config
from os.path import join
import os.path
import shutil
import subprocess
import os
from verboselogs import VerboseLogger as getLogger
logger = getLogger("AFA")


def generate(dir: str, config: Config, dest: str):
    if not os.path.exists(join(dir, "problem", "Dockerfile")):
        logger.warning("No Dockerfile, skip docker build")
        return
    tag = f"afa-{re.compile('[^a-zA-Z0-9]').sub('-', config.problem.name)}"
    shutil.copytree(join(dir, "problem"), join(dest, "Docker镜像构建所需文件"))
    os.makedirs(join(dest, "Docker导出镜像"))
    subprocess.check_call(
        ["docker", "build", join(dir, "problem"), "-t", tag], )
    subprocess.check_call(["docker", "save", tag, "-o",
                          join(dest, "Docker导出镜像", tag+".tar")])
