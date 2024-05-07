from pathlib import Path
from src.lap import lap
from src.assessment_tools import assess_tool
from os import environ as env

assert "COURSE_CONTENT" in env, "COURSE_CONTENT is undefined"
assert "OUTPUT_LOCATION" in env, "OUTPUT_LOCATION is undefined"
COURSE_CONTENT = Path(env["COURSE_CONTENT"]).resolve()
OUTPUT_LOCATION = Path(env["OUTPUT_LOCATION"]).resolve()


def generate_lap():
    lap(COURSE_CONTENT, OUTPUT_LOCATION)


def generate_assessments():
    assess_tool(COURSE_CONTENT, OUTPUT_LOCATION)


def main():
    generate_lap()
    generate_assessments()


if __name__ == "__main__":
    main()
