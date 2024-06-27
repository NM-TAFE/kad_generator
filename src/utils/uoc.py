"""Module for fetching and parsing training.gov.au unit of competencies"""

from __future__ import annotations
from rich import print

import logging
import re

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

import requests
import typer

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
app = typer.Typer()

EXCEPTIONS = {"processes for operating and running variables through algorithms"}


class UOCSections(Enum):
    """
    Enumeration representing different sections of a Unit of Competency.
    """

    APPLICATION = "Application"
    PERFORMANCE_EVIDENCE = "Performance Evidence"
    KNOWLEDGE_EVIDENCE = "Knowledge Evidence"
    ELEMENTS_AND_CRITERIA = "Elements and Performance Criteria"

    @property
    def attribute_name(self) -> str:
        """
        Convert enum value to snake_case to use it as an attribute name.
        """
        if self.value == UOCSections.ELEMENTS_AND_CRITERIA.value:
            return "elements_and_criteria"
        return self.value.replace(" ", "_").lower()


@dataclass
class UnitOfCompetencyData:
    """
    Data class representing the extracted information from a Unit of Competency.
    """

    unit_code: str
    aqf_level: int
    application: str = field(default="")
    performance_evidence: str = field(default="")
    knowledge_evidence: str = field(default="")
    elements_and_criteria: dict[str, str] = field(default_factory=dict)


class UnitOfCompetencyError(Exception):
    """Base class for all errors in this module"""


class UnitOfCompetencyNotFoundError(UnitOfCompetencyError):
    """Raised when a unit of competency cannot be found"""

    def __init__(self, unit_code: str):
        self.unit_code = unit_code
        self.message = f"Unit of competency {unit_code} not found"
        super().__init__(self.message)


class UnitOfCompetency:
    """
    Class representing a Unit of Competency from training.gov.au.
    Responsible for fetching and parsing relevant data.
    """

    base_url = "https://training.gov.au/training/details/"

    def __init__(self, unit_code: str, sections: Iterable[UOCSections] = UOCSections):
        # exrtract aqf level from unit code (also validates unit code)
        match = re.search(r"\d", unit_code)
        if not match:
            raise UnitOfCompetencyError(f"Invalid unit code {unit_code}")
        self.aqf_level = int(match.group())
        self.unit_code = unit_code
        self.sections = sections
        self.url = self.base_url + unit_code
        self._soup = BeautifulSoup(self._fetch_page(), "html.parser")
        self.data = self._get_data(self.sections)

    def parse_assessment_conditions(self):
        # Find the section of interest, the 'assessment_conditions' header
        assessment_conditions_section = self._soup.find(
            "h2", string="Assessment Conditions"
        )
        if not assessment_conditions_section:
            return {}  # Return an empty dictionary if the desired section is not found

        _dict = (
            {}
        )  # Dictionary to store the final assessment_conditions elements and their sub-points
        current_key = (
            None  # To keep track of the current main assessment_conditions element
        )

        # Iterate over the siblings immediately following the 'assessment_conditions' header
        for sibling in assessment_conditions_section.find_next_siblings():
            if sibling.name == "h2":
                break  # Stop the loop if the next header tag is found, marking the end of the current section

            set_this_loop = False
            if sibling.name == "p" and len(sibling.text) > 0:
                _dict[sibling.text] = []
                continue
            for li in sibling.find_all("li"):
                text = li.get_text(strip=True)
                if current_key and current_key.endswith(":") and not text in EXCEPTIONS:
                    _dict[current_key].append(text)
                else:
                    current_key = li.text
                    _dict[current_key] = []
                    set_this_loop = True

            if current_key and current_key.endswith(":") and not set_this_loop:
                current_key = None

        return _dict

    def parse_performance_evidence(self):
        # Find the section of interest, the 'performance Evidence' header
        performance_section = self._soup.find("h2", string="Performance Evidence")
        if not performance_section:
            return {}  # Return an empty dictionary if the desired section is not found

        _dict = (
            {}
        )  # Dictionary to store the final performance elements and their sub-points
        current_key = None  # To keep track of the current main performance element

        # Iterate over the siblings immediately following the 'performance Evidence' header
        for sibling in performance_section.find_next_siblings():
            if sibling.name == "h2":
                break  # Stop the loop if the next header tag is found, marking the end of the current section

            set_this_loop = False
            if sibling.name == "p" and len(sibling.text) > 0:
                _dict[sibling.text] = []
                continue
            for li in sibling.find_all("li"):
                text = li.get_text(strip=True)
                if current_key and current_key.endswith(":") and not text in EXCEPTIONS:
                    _dict[current_key].append(text)
                else:
                    current_key = li.text
                    _dict[current_key] = []
                    set_this_loop = True

            if current_key and current_key.endswith(":") and not set_this_loop:
                current_key = None

        return _dict

    def parse_knowledge_criteria(self):
        # Find the section of interest, the 'Knowledge Evidence' header
        knowledge_section = self._soup.find("h2", string="Knowledge Evidence")
        if not knowledge_section:
            return {}  # Return an empty dictionary if the desired section is not found

        criteria_dict = (
            {}
        )  # Dictionary to store the final knowledge elements and their sub-points
        current_key = None  # To keep track of the current main knowledge element

        # Iterate over the siblings immediately following the 'Knowledge Evidence' header
        for sibling in knowledge_section.find_next_siblings()[1:]:
            set_this_loop = False
            if sibling.name == "h2":
                break  # Stop the loop if the next header tag is found, marking the end of the current section
            for li in sibling.find_all("li"):
                text = li.get_text(strip=True)
                if current_key and current_key.endswith(":") and not text in EXCEPTIONS:
                    criteria_dict[current_key].append(text)
                else:
                    current_key = li.text
                    criteria_dict[current_key] = []
                    set_this_loop = True

            if current_key and current_key.endswith(":") and not set_this_loop:
                current_key = None

        return criteria_dict

    def _fetch_page(self) -> str:
        """
        Fetch the web page containing the Unit of Competency details.
        """
        logger.debug(f"Fetching page {self.url}")
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            logging.error(f"Failed to fetch page {self.url}: {e}")
            raise UnitOfCompetencyNotFoundError(self.unit_code) from e

    def _get_data(self, sections: Iterable[UOCSections]) -> UnitOfCompetencyData:
        """
        Extract relevant data from the web page based on the specified sections.
        """
        data_dict = {"unit_code": self.unit_code, "aqf_level": self.aqf_level}

        for section in sections:
            if section == UOCSections.ELEMENTS_AND_CRITERIA:
                data_dict[section.attribute_name] = (
                    self._get_elements_and_performance_criteria()
                )
            else:
                data_dict[section.attribute_name] = self._get_section_text(
                    section.value
                )
        return UnitOfCompetencyData(**data_dict)

    def _get_section_text(self, section: str) -> str:
        """
        Extract the text from a specific section of the web page.
        """
        # Locate the section header
        if not (section_header := self._soup.find("h2", string=section)):
            raise UnitOfCompetencyError(f"Could not find {section} section")

        # Extract relevant text based on sibling elements of the section header
        text = ""
        for sibling in section_header.find_next_siblings():
            if sibling.name and sibling.name.startswith("h2"):  # type: ignore
                break
            if sibling.name == "p":  # type: ignore
                text += sibling.get_text(strip=True) + "\n"
            elif sibling.name == "ul":  # type: ignore
                text += (
                    "\n".join(
                        [
                            li.get_text(strip=True) for li in sibling.find_all("li")  # type: ignore
                        ]
                    )
                    + "\n"
                )
        return text.strip()

    def _get_elements_and_performance_criteria(self) -> dict[str, str]:
        """
        Extract the elements and performance criteria from the web page.
        """
        # Locate the section header for elements and performance criteria
        if elements_header := self._soup.find(
            "h2", string=UOCSections.ELEMENTS_AND_CRITERIA.value
        ):
            # Extract data from the table rows
            return {
                row.find_all("td")[0]
                .get_text(strip=True): row.find_all("td")[1]
                .get_text(strip=False)
                for row in elements_header.find_next("table").find_all("tr")[  # type: ignore
                    2:
                ]
            }
        raise UnitOfCompetencyError(
            f"Could not find {UOCSections.ELEMENTS_AND_CRITERIA.value} section"
        )

    def __str__(self) -> str:
        sections_strings = []

        for data in self.sections:
            if data == UOCSections.ELEMENTS_AND_CRITERIA:
                elements_and_criteria_strings = [
                    f"{element}\n{criteria}"
                    for element, criteria in self.data.elements_and_criteria.items()
                ]
                elements_and_criteria_text = "\n\n".join(elements_and_criteria_strings)
                section_string = f"{data.value}\n{elements_and_criteria_text}"
            else:
                section_string = (
                    f"{data.value}\n{getattr(self.data, data.attribute_name)}"
                )
            sections_strings.append(section_string)

        return "\n\n".join(sections_strings)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({self.unit_code!r}, {self.sections!r})"


@app.command()
def print_uoc(
    unit_name: str = typer.Option(..., help="training.gov.au unit of competency code")
):
    """
    Command-line function to print the Unit of Competency data.
    """
    print(UnitOfCompetency(unit_name))


@app.command()
def main(
    unit_name: str = typer.Option(
        "ICTPRG443", help="training.gov.au unit of competency code"
    )
):
    """
    Main function, primarily for testing the Jinja2 template and the UOC class.
    """
    from pathlib import Path

    from jinja2 import Environment, FileSystemLoader

    templates_dir = Path(__file__).parent / "preprompts"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("uoc_prompt")
    logging.basicConfig(level=logging.DEBUG)
    uoc = UnitOfCompetency(unit_name)
    print(uoc.data)
    print("#" * 80)
    print_uoc(unit_name)
    print("#" * 80)
    print("#" * 80)
    result = template.render(uoc=uoc)
    print(result)


if __name__ == "__main__":
    app()
    main()
