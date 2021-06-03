from data.config import Config
from os.path import join
import os.path
from openpyxl import load_workbook

__dir__ = os.path.dirname(os.path.abspath(__file__))


def generate(dir: str, config: Config, dest: str):
    wb = load_workbook(join(__dir__, "./template.xlsx"))
    sheet = wb["Sheet1"]
    sheet["B2"] = config.problem.name
    sheet["C2"] = config.problem.type
    sheet["D2"] = config.problem.difficulty
    sheet["E2"] = config.name
    sheet["F2"] = config.contact
    sheet["G2"] = config.email
    sheet["I2"] = config.problem.comment
    sheet["M2"] = ' '.join(config.problem.point)
    sheet["O2"] = str(config.bank_id)
    sheet["P2"] = config.bank_name
    sheet["Q2"] = str(config.id)
    wb.save(join(dest, "题目及出题人信息.xlsx"))
