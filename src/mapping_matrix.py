import os
from os import environ as env
import click
from docx import Document
from docx.table import Table, _Cell, _Column
from docx.styles.styles import Styles
from docx.enum.style import WD_STYLE_TYPE, WD_BUILTIN_STYLE as WD_STYLE
from docx.document import Document as _Document
from docx.shared import Pt
from docx.section import _Header, _Footer, Section, Sections
from pathlib import Path
from pandas import DataFrame

from src.utils.markdown import markdown_to_word, parse_md
from src.utils.math import add_tuples


os.environ["ROOT_DIR"] = str(Path(__file__).parent.parent.resolve())

# Absolute Path of course content folder from env
assert "COURSE_CONTENT" in env, "COURSE_CONTENT is undefined"
assert "OUTPUT_LOCATION" in env, "OUTPUT_LOCATION is undefined"

COURSE_CONTENT = Path(env["COURSE_CONTENT"]).resolve()
OUTPUT_LOCATION = Path(env["OUTPUT_LOCATION"]).resolve()

# Source code locations:
ROOT = env["ROOT_DIR"]  # repo root location
TEMPLATES = Path("templates/")

# Implementation Specific
TEMPLATE = TEMPLATES / Path("Assessment Mapping Matrix (F122A8).docx")
OUTPUT_FILE = Path("Assessment Mapping Matrix (F122A8).docx")

# Relative Path of Content Files (Input and Output):
ASSESSMENTS = Path("2 KAD/5 Assess Tool/")
MAPPING_MATRIX = Path("2 KAD/7 Assess Mapping Matrix/")


import re
from typing import List, Dict


def parse_markdown_headers(md_content: str) -> List[Dict[str, str]]:
    """
    Parses a Markdown string into an iterable of sections based on Markdown headers.

    :param md_content: A string containing the Markdown content.
    :return: A list of dictionaries with 'header' and 'content' keys.
    """

    # Define a regex to match markdown headers
    header_regex = re.compile(r"^(#{1})\s+(.*)", re.MULTILINE)

    sections = []
    last_pos = 0
    for match in header_regex.finditer(md_content):
        # Extract header level and text
        header_level = len(match.group(1))
        header_text = match.group(2).strip()

        # Find the position of the header
        start_pos = match.start()
        # Get content up to this header
        content = md_content[last_pos:start_pos].strip()

        # If there is a previous section, update its content
        if sections:
            sections[-1]["content"] = content

        # Create a new section for the current header
        section = {"header": header_text, "content": "", "level": header_level}
        sections.append(section)

        last_pos = match.end()

    # Add the content for the last section
    if sections:
        sections[-1]["content"] = md_content[last_pos:].strip()

    return sections


def mapping_matrix(course_directory: Path, output_location: Path):
    assert course_directory.is_dir()
    assert output_location.is_dir()

    assessments = course_directory / ASSESSMENTS
    unit_assessment_mapping = {}
    for assessment in assessments.rglob("assessment.md"):

        doc: _Document = Document(ROOT / TEMPLATE)
        styles: Styles = doc.styles

        if not assessment.is_file():
            continue

        markdown = parse_md(assessment)

        name = markdown.get("name")
        units = markdown.get("units")

        for unit in units:
            ## Initialize unit mapping matrix if needed:
            unit_assessment_mapping.setdefault(
                unit["id"],
                {
                    "assessments": [],
                    "unit": unit,
                    "qualification": markdown.get(
                        "qualification_national_code_and_title"
                    ),
                },
            )
            ## add assessment to unit mapping matrix
            unit_assessment_mapping.get(unit["id"]).get("assessments").append(markdown)

    for id, mapping_matrix in unit_assessment_mapping.items():

        unit = mapping_matrix.get("unit")
        header: _Header = doc.sections[0].header
        table_header: Table = header.tables[0]

        # Set Unit national codes and titles
        cell: _Cell = table_header.cell(1, 1)
        cell.text = f'{unit.get("id")} {unit.get("name")}'

        # Set qualification national codes and titles
        cell: _Cell = table_header.cell(0, 1)
        cell.text = f'{mapping_matrix.get("qualification")}'

        # TODO: auto insert uoc elements etc

        # TODO: set each column up for every assessment (names etc..)

        # TODO: Implement actual mapping of assessment elements to criteria etc

        # TODO: Implement main disclosure statements

        output: Path = output_location / MAPPING_MATRIX / (id + " " + str(OUTPUT_FILE))
        output.parent.mkdir(exist_ok=True, parents=True)
        doc.save(output)


@click.command()
# @click.argument("course_directory", type=click.Path(exists=True, path_type=Path))
def run_cli():
    """
    CLI tool to write YAML header data from Markdown file to Word document as custom properties.
    """
    assess_tool(COURSE_CONTENT, OUTPUT_LOCATION)


if __name__ == "__main__":
    run_cli()
