from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR.joinpath("src/")

ENV_PATH = ROOT_DIR.joinpath(".env")
LOGGING_DIR = ROOT_DIR.joinpath("logs/")

STATIC_PATH = ROOT_DIR.joinpath("static/")
TEMPLATES_PATH = ROOT_DIR.joinpath("templates/")