from pathlib import Path
from src.lap import lap, run_cli
import pytest

COURSE_CONTENT = Path("/Users/jordan/NMTAFE/Course Content/AI Skillset").resolve()
OUTPUT_LOCATION = Path("/Users/jordan/NMTAFE/content_generator/test").resolve()


def test_lap():
    lap(COURSE_CONTENT, OUTPUT_LOCATION)
