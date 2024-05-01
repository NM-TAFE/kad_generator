from pathlib import Path
from src.lap import lap
import pytest

COURSE_CONTENT = Path("/Users/jordan/NMTAFE/Course Content/AI Skillset/").resolve()
OUTPUT_LOCATION = Path("/Users/jordan/NMTAFE/content_generator/example").resolve()


def test_generate_lap():
    lap(COURSE_CONTENT, OUTPUT_LOCATION)
