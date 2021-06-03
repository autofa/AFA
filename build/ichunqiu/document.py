from data.config import Config
import os
import os.path
from dockerfile_parse import DockerfileParser
from os.path import join

from jinja2 import Template

__dir__ = os.path.dirname(os.path.abspath(__file__))

def generate(dir: str, config: Config, dest: str):
    dest = join(dest, f"ctf赛题设计说明.md")
    with open(join(__dir__, "./template.md")) as f:
        tpl = Template(f.read())
    with open(join(dir, "WRITEUP.MD"), "r") as f:
        writeup = f.read()
    env = ""
    try:
        with open(join(dir, "problem", "Dockerfile"), "r") as f:
            dfp = DockerfileParser()
            dfp.content = f.read()
            env = ','.join(dfp.parent_images)
    except:
        pass
    r = tpl.render({
        "config": config,
        "env": env,
        "writeup": writeup
    })
    print(dest)
    with open(dest, "w") as f:
        f.write(r)
    