import click
from docx import Document
import frontmatter
from pathlib import Path


def set_custom_property(document, name, value):
    document.custom_properties[name] = value


def write_yaml_to_docx(docx_file: Path, markdown_file: Path):
    # Load the docx file
    doc = Document(docx_file)

    # Load the markdown file and parse the front matter
    with open(markdown_file, "r", encoding="utf-8") as file:
        parsed_md = frontmatter.load(file)

    # Loop through front matter data and add as custom properties to the docx
    for key, value in parsed_md.metadata.items():
        set_custom_property(doc, key, str(value))

    # Save the modified docx
    doc.save(docx_file)
    click.echo(f"Updated '{docx_file}' with custom properties from '{markdown_file}'.")


@click.command()
@click.argument("docx_path", type=click.Path(exists=True, path_type=Path))
@click.argument("markdown_path", type=click.Path(exists=True, path_type=Path))
def run_cli(docx_path: Path, markdown_path: Path):
    """
    CLI tool to write YAML header data from Markdown file to Word document as custom properties.
    """
    write_yaml_to_docx(docx_path, markdown_path)


if __name__ == "__main__":
    run_cli()
