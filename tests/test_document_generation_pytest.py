from pathlib import Path
from src.assessment_tools import assess_tool
from src.lap import lap
import pytest

COURSE_CONTENT = Path("/Users/jordan/NMTAFE/Course Content/AI Skillset/").resolve()
OUTPUT_LOCATION = Path("/Users/jordan/NMTAFE/content_generator/example").resolve()


def test_generate_lap():
    lap(COURSE_CONTENT, OUTPUT_LOCATION)


def test_generate_assessments():
    assess_tool(COURSE_CONTENT, OUTPUT_LOCATION)
