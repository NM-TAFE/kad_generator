from pathlib import Path
from src.lap import lap, run_cli
import pytest

AI_SKILLSET = Path("/Users/jordan/NMTAFE/Course Content/AI Skillset")


def test_lap():
    lap(AI_SKILLSET)
