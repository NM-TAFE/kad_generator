import os
from pathlib import Path

os.environ["ROOT_DIR"] = str(Path(__file__).parent.parent.absolute().resolve())
