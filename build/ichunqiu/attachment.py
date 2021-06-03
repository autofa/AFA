import hashlib
import os
import os.path
from posix import listdir
from posixpath import join
import shutil

from data.config import Config


def generate(dir: str, config: Config, dest: str):
    if len(os.listdir(join(dir, "attachments"))) == 0 or os.listdir(join(dir, "attachments"))==['.gitkeep']:
        os.mkdir(join(dest, f"附件：无"))
        exit(0)
    os.mkdir(join(dest, f"附件"))
    shutil.make_archive(join(dest, f"附件", "tmp"), "zip", join(dir, "attachments"))
    with open(join(dest, f"附件", "tmp.zip"), "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
    shutil.move(join(dest, f"附件", "tmp.zip"), join(dest, f"附件", f"attachment_{h}.zip"))
