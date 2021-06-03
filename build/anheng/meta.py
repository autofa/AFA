import os
import os.path
from os.path import join
from typing import List, Tuple

from data.config import Config
from verboselogs import VerboseLogger as getLogger

SLASH_N = "\n"

logger = getLogger("AFA")


def _scan_attachments(base: str) -> List[Tuple[str, str]]:
    res: List[Tuple[str, str]] = []
    for i in os.listdir(base):
        if os.path.isfile(join(base, i)):
            logger.info(f"Get attachment: {join(base, i)}")
            res.append((join(base, i), i))
        else:
            res += _scan_attachments(join(base, i))
    return res


def scan_attachments(dir: str) -> List[Tuple[str, str]]:
    logger.info("Scaning attachments")
    return [(i[0].split(os.path.sep, 2)[-1], i[1]) for i in _scan_attachments(join(dir, "attachments"))]


def generate(dir: str, config: Config, dest: str):
    filename = join(dir, "meta.txt")
    attachments = scan_attachments(dir)
    template = f"""
<question>{config.problem.description}
<id>DBAPP-LAB-{config.problem.type}-{config.timestamp}
<title>{config.problem.name}
<score>{config.problem.difficulty * 100}
<level>{config.problem.difficulty_text}
<global>1
<qatype>{config.problem.type}
<tags>{' '.join(config.problem.point)}
<anstype>实操
<answer>{config.problem.flag}
{SLASH_N.join([f'<prompt>{i}.{s}' for (i, s) in enumerate(config.problem.prompt)])}
<ansattachfile>{config.problem.type}解题思路/{config.problem.name}_writeup.pdf
<ansattachname>"{config.problem.name}"的解题思路
{SLASH_N.join([f'<attachfile>{i}{SLASH_N}<attachname>{s}' for (i, s) in attachments])}
    """.strip()
    with open(join(dest, "meta.txt"), "w") as f:
        f.write(template)
