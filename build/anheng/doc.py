from data.config import Config
import os
import os.path
import subprocess
from os.path import join


from docxtpl import DocxTemplate

from .render import render

__dir__ = os.path.dirname(os.path.abspath(__file__))


def generate(dir: str, config: Config, dest: str):
    dest = join(dest, f"{config.problem.type}解题思路")
    os.makedirs(dest)
    tpl = DocxTemplate(join(__dir__, "./template.docx"))
    with open(join(dir, "WRITEUP.MD"), "r") as f:
        writeup = f.read()
    sub = tpl.new_subdoc()
    render(sub.subdocx, writeup)
    tpl.render({
        "sub": sub,
        "problem": config.problem
    })
    tpl.save(join(dest, f"{config.problem.name}_writeup.docx"))
    subprocess.check_call(["doc2pdf", "-o", join(
        dest, f"{config.problem.name}_writeup.pdf"), join(dest, f"{config.problem.name}_writeup.docx")])
