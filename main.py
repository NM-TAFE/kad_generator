from pathlib import Path

from requests import RequestException
from src.lap import lap
from src.assessment_tools import assess_tool
from os import environ as env

from src.mapping_matrix import mapping_matrix
from src.utils.logger import log

assert "COURSE_CONTENT" in env, "COURSE_CONTENT is undefined"
assert "OUTPUT_LOCATION" in env, "OUTPUT_LOCATION is undefined"
COURSE_CONTENT = Path(env["COURSE_CONTENT"]).resolve()
OUTPUT_LOCATION = Path(env["OUTPUT_LOCATION"]).resolve()


def generate_lap():
    lap(COURSE_CONTENT, OUTPUT_LOCATION)


def generate_assessments():
    assess_tool(COURSE_CONTENT, OUTPUT_LOCATION)


def generate_matrix():
    mapping_matrix(COURSE_CONTENT, OUTPUT_LOCATION)


def main():
    generate_lap()
    generate_assessments()
    # try:
    generate_matrix()
    # except (RequestException, Exception):
    #     log.warn(
    #         "Matrix not generated! Cannot access UoC on training.gov Check connectivity."
    #     )


if __name__ == "__main__":
    main()
