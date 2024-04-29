import os
from os import environ as env
import click
from docx import Document
from docx.table import Table, _Cell
from docx.styles.styles import Styles
from docx.shared import Inches
import frontmatter
from pathlib import Path
from pandas import DataFrame

os.environ["ROOT_DIR"] = str(Path(__file__).parent.parent.absolute().resolve())


ROOT = env["ROOT_DIR"]
AI_SKILLSET = Path("/Users/jordan/NMTAFE/Course Content/AI Skillset")

TOPICS = Path("KADS/1 LAP/topics.md")

import re
from typing import List, Dict

def add_tuples(*arg):
    return tuple(map(sum, zip(*arg)))

def parse_markdown_headers(path: Path) -> List[Dict[str, str]]:
    """
    Parses a Markdown string into an iterable of sections based on Markdown headers.

    :param md_content: A string containing the Markdown content.
    :return: A list of dictionaries with 'header' and 'content' keys.
    """

    with open(path) as file:
        md_content = file.read()
        # Define a regex to match markdown headers
        header_regex = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)

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

def add_paragraph_with_style(document, text, style):
    """Add a new paragraph with specific style."""
    paragraph = document.add_paragraph(style=style)
    run = paragraph.add_run(text)
    return paragraph, run

def markdown_to_word_styles(md_content, document):
    """
    Parses Markdown content and applies corresponding Word styles.
    Indented lists are also accounted for.
    
    :param md_content: String containing the Markdown content.
    :param document: docx Document object.
    """
    # Split content into lines for processing.
    lines: list[str] = md_content.split('\n')
    list_buffer = []
    list_levels = {}
    in_code_block = False

    def flush_buffer():
        """Flush buffer and insert paragraphs to document."""
        prev_level = 0
        for item_text, level in list_buffer:
            if level > prev_level:
                style = 'List Bullet'  # Word style for continued list, which may be indented.
            else:
                style = 'List Bullet' if item_text.startswith('-') else 'ListNumber'
            paragraph, run = add_paragraph_with_style(document, item_text[2:], style)
            # Indent as required.
            for _ in range(level):
                if paragraph.paragraph_format.left_indent is None:
                    paragraph.paragraph_format.left_indent = Inches(0.25)
                paragraph.paragraph_format.left_indent = Inches(0.25)
            prev_level = level
        list_buffer.clear()

    last_indentation: int = 0
    for line in lines:
        if line.startswith("```"):  # Code block check
            in_code_block = not in_code_block
            continue

        if in_code_block:  # Inside a code block
            continue

        if line.lstrip().startswith((r'\#\s', r'\-\s', r'\* ', r'\+ ', r'\d\.\s')):
            level = len(line.lstrip(' '))
            
            # Regular or indented bullet/numbered lists
            if list_buffer and not line.startswith(' '):  # New list, flush buffer
                flush_buffer()
            # Count leading spaces to determine level
            list_levels[level] = list_levels.get(level, 0) + 1
            list_buffer.append((line.lstrip(' '), level))
            last_indentation = level
        else:
            if list_buffer:  # Non-list line after list, flush buffer
                flush_buffer()
            if line.strip() == '':
                # Empty line denotes new paragraph
                document.add_paragraph()
            else:
                # Regular paragraph
                paragraph, run = add_paragraph_with_style(document, line, 'Normal')
                apply_inline_formatting(run, line)

    if list_buffer:
        flush_buffer()  # Catch any end of document lists

def apply_inline_formatting(run, text):
    """Apply inline formatting based on Markdown syntax."""
    bold_re = re.compile(r'\*\*(.*?)\*\*')
    italic_re = re.compile(r'_(.*?)_')

    start = 0
    for match in bold_re.finditer(text):
        before = text[start:match.start()]
        run.add_text(before)
        bold_text = match.group(1)
        bold_run = run.add_text(bold_text)
        bold_run.bold = True
        start = match.end()
    rest = text[start:]
    for match in italic_re.finditer(rest):
        before = rest[:match.start()]
        italic_text = match.group(1)
        run.add_text(before)
        italic_run = run.add_text(italic_text)
        italic_run.italic = True
        rest = rest[match.end():]
    run.add_text(rest)


def lap(course_directory: Path):
    print(Path.cwd())
    doc = Document(ROOT / Path("templates/lap.docx"))
    doc = doc

    styles: Styles = doc.styles

    # print(dir(doc))
    Path("test/test.docx").resolve().parent.mkdir(parents=True, exist_ok=True)
    table = doc.add_table(rows=2, cols=2)
    # print(dir(doc.tables[0]))
    # print(doc.tables[0].cell(0, 0).text)
    # doc.tables[0].cell(0, 0).text = "Hello"
    # print(doc.tables[0].cell(0, 0).text)
    for table in doc.tables:
        print(DataFrame([[cell.text for cell in row.cells] for row in table.rows]))
    print()
    print("Columns:")
    print()
    for table in doc.tables:
        print(
            DataFrame(
                [[cell.text for cell in column.cells] for column in table.columns]
            )
        )

    ## Qualification
    ## Delivery Period
    ## Cluster Name
    doc.tables[0]

    # National ID
    # Name of Unit
    doc.tables[1]

    # Topics
    topics = parse_markdown_headers(course_directory / TOPICS)
    start_coords = (2, 3)
    table: Table = doc.tables[5]
    # table.autofit = True
    for idx, topic in enumerate(topics):
        print(idx)
        coords = add_tuples((idx, 0), start_coords)
        
        table.cell(*coords).add_paragraph(topic.get("header"), styles[f"Heading {topic.get("level", 1)}"])
        markdown_to_word_styles(topic.get("content"), table.cell(*coords))
        # table.cell(*coords).add_paragraph(topic.get("content"), styles[f"Normal"])

    # for row in doc.tables[5].rows:
    #     for cell in row.cells:
    #         cell.text = "1"

    doc.save("test/test.docx")


@click.command()
# @click.argument("course_directory", type=click.Path(exists=True, path_type=Path))
def run_cli():
    """
    CLI tool to write YAML header data from Markdown file to Word document as custom properties.
    """
    lap(AI_SKILLSET)


if __name__ == "__main__":
    run_cli()
