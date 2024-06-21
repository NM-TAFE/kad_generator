from pathlib import Path
from src.assessment_tools import assess_tool
from src.lap import lap
import pytest

from src.mapping_matrix import mapping_matrix

COURSE_CONTENT = Path("~/NMTAFE/Course Content/AI Skillset").expanduser()
OUTPUT_LOCATION = Path("~/NMTAFE/content_generator/example").expanduser()


def test_generate_lap():
    lap(COURSE_CONTENT, OUTPUT_LOCATION)


def test_generate_assessments():
    assess_tool(COURSE_CONTENT, OUTPUT_LOCATION)


def test_generate_mapping_matrix():
    mapping_matrix(COURSE_CONTENT, OUTPUT_LOCATION)
