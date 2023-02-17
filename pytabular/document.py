"""`document.py` is where a specific part of pytabular start.

This module can generate pages in markdown for use in Docusaurus.
"""
import logging

from pathlib import Path

from pytabular.table import PyTable
from pytabular.column import PyColumn
from pytabular.culture import PyCulture
from pytabular.measure import PyMeasure
from pytabular.pytabular import Tabular
from typing import List, Dict

logger = logging.getLogger("PyTabular")


class ModelDocumenter:
    """The ModelDocumenter class can generate documentation.

    This is based on the tabular object model and it will generate it suitable for docusaurus.
    TODO: Add a General Pages template with Roles and RLS Expressions.
    TODO: Create a Sub Page per table for all columns, instead of one big page?
    TODO: Add Depencies per Measure with correct links.
    """

    def __init__(
        self,
        model: Tabular,
        friendly_name: str = str(),
        save_location: str = "docs",
        general_page_url: str = "index.md",
        measure_page_url: str = "measures.md",
        roles_page_url: str = "roles.md",
        table_folder: str = "tables",
        # table_page_url: str = "3-tables.md",
        # column_page_url: str = "4-columns.md",
    ):
        """Init will set attributes based on arguments given.

        See `generate_documentation_pages()` and `save_documentation()`
        for info on how to execute and retrieve documentation.

        Args:
            model (Tabular): Main `Tabular()` class to pull metadata from for documentation.
            friendly_name (str, optional): Replaces the model name to a friendly string,
                so it can be used in an URL. Defaults to `str()`.
            save_location (str, optional): The save location where the files will be stored.
                Defaults to "docs".
            general_page_url (str, optional): Name of the `md` file for general information.
                Defaults to "index.md".
            measure_page_url (str, optional): Name of the `md` file for measures.
                Defaults to "measures.md".
            table_folder (str, optional): Name of the folder where columns info is stored.
                Defaults to "table_folder".
            roles_page_url (str, optional): Name of the `md` file for roles.
                Defaults to "roles.md".
        """
        self.model = model
        self.model_name = friendly_name or model.Catalog or model.Database.Name
        self.friendly_name: str = str()
        self.save_path: Path
        self.save_location: str = save_location

        # Translation information
        self.culture_include: bool = False
        self.culture_selected: str = "en-US"
        self.culture_object: PyCulture

        # Documentation Parts
        self.general_page: str = str()
        self.general_page_url: str = general_page_url

        self.measure_page: str = str()
        self.measure_page_url: str = measure_page_url

        self.roles_page: str = str()
        self.roles_page_url: str = roles_page_url

        self.table_page: str = str()
        self.table_folder: str = table_folder

        # Generate an url friendly name for the model / folder
        self.friendly_name: str = self.set_url_friendly_name(self.model_name)

        # Initialize Save path so checks can be run against it.
        self.save_path = self.set_save_path()

    def create_object_reference(self, object: str, object_parent: str) -> str:
        """Create a Custom ID for link sections in the docs.

        This is based on the technical names in the model,
        so not the once in the translations. This makes it
        possible to link based on dependencies.
        (Scope is only Docusaurus)

        Args:
            object (str): Object Name
            object_parent (str): Object Parent (e.g. Table)

        Returns:
            str: String that can be used for custom linking
        """
        url_reference = f"{object_parent}-{object}".replace(" ", "")
        return f"{{#{url_reference}}}"

    def generate_documentation_pages(self) -> None:
        """Generate Documentation for each specific part of the model."""
        self.measure_page = self.generate_markdown_measure_page()
        self.table_page = self.generate_markdown_table_page()
        self.general_page = self.generate_general_info_file()

    def get_object_caption(self, object_name: str, object_parent: str) -> str:
        """Retrieves the caption of an object, based on the translations in the culture.

        If no culture is present, the object_name is returned.

        Args:
            object_name (str): Object Name
            object_parent (str): Object Parent Name

        Returns:
            str: Translated object.
        """
        if self.culture_include:
            return str(
                self.culture_object.get_translation(
                    object_name=object_name, object_parent_name=object_parent
                ).get("object_translation")
            )

        return object_name

    def set_translations(
        self, enable_translations: bool = False, culture: str = "en-US"
    ) -> None:
        """Set translations to active or inactive, depending on the needs of the users.

        Args:
            enable_translations (bool, optional): Flag to enable or disable translations.
                Defaults to False.
            culture (str, optional): Set culture that needs to be used in the docs.
                Defaults to "en-US".
        """
        logger.info(f"Using Translations set to > {enable_translations}")

        if enable_translations:
            try:
                self.culture_object = self.model.Cultures[culture]
                self.culture_selected = culture
                self.culture_include = enable_translations
            except IndexError:
                self.culture_include = False
                logger.warn(
                    "Culture not found, reverting back to orginal setting > False"
                )
            else:
                logger.info(f"Setting culture to {self.culture_selected}")

        else:
            self.culture_include = enable_translations

    def set_save_path(self) -> Path:
        """Set the location of the documentation.

        Returns:
            Path: Path where the docs are saved.
        """
        return Path(f"{self.save_location}/{self.friendly_name}")

    def save_page(self, content: str, page_name: str, keep_file: bool = False) -> None:
        """Save the content of the documentation to a file.

        Based on the class setup.
        - Save Location
        - Model Friendly Name
        - Page to be written

        Args:
            content (str): File content to write to file.
            page_name (str): Name of the file that will be used.
            keep_file (bool): The file will only be overwritten if
                the keep_file is set to False.

        Returns:
            None
        """
        target_file = self.save_path / page_name

        if target_file.parent.exists() is False:
            target_file.parent.mkdir(parents=True, exist_ok=True)

        if keep_file and target_file.exists():
            logger.info(f"{page_name} already exists -> file will not overwritten.")
        else:
            logger.info(f"Results are written to -> {page_name}.")

            with target_file.open("w", encoding="utf-8") as f:
                f.write(content)
                f.close()

    def save_documentation(self) -> None:
        """Generate documentation of the model, based on the meta-data in the model definitions.

        This first checks if the folder exists,
        and then starts to export the files that are needed
        for the documentatation.
        - General Information Page -> Free format page to create.
        - Measure Page -> Describes the measures in the model.
        - Tables Page -> Describes the tables in the model.
        - Columns Page -> Describes all columns in the model per table.
        - Roles Page -> Describes the roles in the model.

        Args:
            self (ModelDocumenter): Model object for documentation.

        Returns:
            None
        """
        if self.save_path.exists():
            logger.info(
                f"Path exists -> Generating documentation for {self.friendly_name}"
            )
        else:
            logger.info(
                f"Path does not exist -> Creating directory for {self.friendly_name}"
            )
            self.save_path.mkdir(parents=True, exist_ok=True)

        if self.general_page:
            self.save_page(
                content=self.general_page,
                keep_file=True,
                page_name=self.general_page_url,
            )

        if self.measure_page:
            self.save_page(
                content=self.measure_page,
                keep_file=False,
                page_name=self.measure_page_url,
            )

        for table in self.create_markdown_for_table_and_column():
            table = table.items()
            page_name, page_content = list(table)[0]
            self.save_page(
                content=page_content,
                keep_file=False,
                page_name=f"{self.table_folder}/{page_name}",
            )

        if self.roles_page:
            self.save_page(
                content=self.roles_page, keep_file=False, page_name=self.roles_page_url
            )

    def create_markdown_for_measure(self, object: PyMeasure) -> str:
        """Create Markdown for a specific measure.

        That can later on be used for generating the whole measure page.

        Args:
            object (PyMeasure): The measure to document.

        Returns:
            str: Markdown section for specific Measure
        """
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )

        obj_description = (object.Description or "No Description available").replace(
            "\\n", ""
        )

        obj_description = obj_description.replace("<>", "not equal to ")

        object_properties = [
            {"Measure Name": object.Name},
            {"Display Folder": object.DisplayFolder},
            {"Format String": object.FormatString},
            {"Is Hidden": "Yes" if object.IsHidden else "No"},
        ]

        obj_text = [
            f"### {object_caption}",
            "**Description**:",
            f"> {obj_description}",
            "",
            "" f"{self.generate_object_properties(object_properties)}" "",
            f'```dax title="Technical: {object.Name}"',
            f"  {object.Expression}",
            "```",
            "---",
        ]
        return "\n".join(obj_text)

    def generate_markdown_measure_page(self) -> str:
        """This function generates the meausure documation page.

        Returns:
            str: The full markdown text that is needed
                make it compatible with Docusaurus.
        """
        prev_display_folder = ""
        markdown_template = [
            "---",
            "sidebar_position: 1",
            "title: Measures",
            "description: This page contains all measures for "
            f"the {self.model.Name} model, including the description, "
            "format string, and other technical details.",
            "---",
            "",
            f"# Measures for {self.model.Name}",
        ]

        measures = sorted(
            self.model.Measures, key=lambda x: x.DisplayFolder, reverse=False
        )

        for measure in measures:
            logger.debug(f"Creating docs for {measure.Name}")
            display_folder = measure.DisplayFolder or "Other"
            display_folder = display_folder.split("\\")[0]

            if prev_display_folder != display_folder:
                markdown_template.append(f"""## {display_folder}""")
                prev_display_folder = display_folder

            markdown_template.append(self.create_markdown_for_measure(measure))

        return "\n".join(markdown_template)

    def create_markdown_for_table_and_column(self) -> list:
        """Create Pages for Tables and Columns.

        Based on the model this functions creates a general
        overview pages for all tables and then with per
        table a page with all column details.

        Returns:
            list: List of dicts per page.

        Example:
            ```
                {
                    "Overview": "Content",
                    "Table1": "Content",
                    "Table2": "Content",
                }

        """
        obj_content = [{"index.md": self.generate_markdown_table_page()}]

        for idx, table in enumerate(self.model.Tables):
            obj_caption = (
                self.get_object_caption(
                    object_name=table.Name, object_parent=table.Parent.Name
                )
                or table.Name
            )

            obj_caption = obj_caption.replace("[", "").replace("]", "")

            key = f"{self.set_url_friendly_name(obj_caption)}.md"
            value = self.generate_markdown_column_page(
                object=table, object_caption=obj_caption, page_index=idx + 2
            )

            obj_content.append({key: value})

        return obj_content

    def create_markdown_for_table(self, object: PyTable) -> str:
        """This functions returns the markdown for a table.

        Args:
            object (PyTable): Based on the PyTabular Package.

        Returns:
            str: Will be appended to the page text.
        """
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )

        obj_description = (object.Description or "No Description available").replace(
            "\\n", ""
        )

        object_properties = [
            {"Measures (#)": len(object.Measures)},
            {"Columns (#)": len(object.Columns)},
            {"Partiton (#)": len(object.Partitions)},
            {"Data Category": object.DataCategory or "Regular Table"},
            {"Is Hidden": object.IsHidden},
            {"Table Type": object.Partitions[0].ObjectType},
            {"Source Type": object.Partitions[0].SourceType},
        ]

        obj_description = obj_description.replace("<>", "not equal to ")

        partition_type = ""
        partition_source = ""

        logger.debug(f"{object_caption} => {str(object.Partitions[0].SourceType)}")

        if str(object.Partitions[0].SourceType) == "Calculated":
            partition_type = "dax"
            partition_source = object.Partitions[0].Source.Expression
        elif str(object.Partitions[0].SourceType) == "M":
            partition_type = "powerquery"
            partition_source = object.Partitions[0].Source.Expression
        elif str(object.Partitions[0].SourceType) == "CalculationGroup":
            partition_type = ""
            partition_source = ""
        else:
            partition_type = "sql"
            partition_source = object.Partitions[0].Source.Query

        obj_text = [
            f"### {object_caption}",
            "**Description**: ",
            f"> {obj_description}",
            "",
            f"{self.generate_object_properties(object_properties)}",
            "",
            f'```{partition_type} title="Table Source: {object.Name}"',
            f"   {partition_source}",
            "```",
            "---",
        ]

        return "\n".join(obj_text)

    def generate_markdown_table_page(self) -> str:
        """This function generates the markdown for table documentation.

        Returns:
            str: Will be appended to the page text.
        """
        markdown_template = [
            "---",
            "sidebar_position: 2",
            "sidebar_label: Tables",
            "description: This page contains all columns with "
            f"tables for {self.model.Name}, including the description, "
            "and technical details.",
            "---",
            "",
            f"# Tables {self.model.Name}",
        ]

        markdown_template.extend(
            self.create_markdown_for_table(table) for table in self.model.Tables
        )
        return "\n".join(markdown_template)

    def create_markdown_for_column(self, object: PyColumn) -> str:
        """Generates the Markdown for a specifc column.

        If a columns is calculated, then it also shows the expression for
        that column in DAX.

        Args:
            object (PyColumn): Needs PyColumn objects input

        Returns:
            str: Will be appended to the page text.
        """
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )

        obj_description = (
            object.Description.replace("\\n", "") or "No Description available"
        )

        obj_description = obj_description.replace("<>", "not equal to ")

        obj_heading = f"""{object_caption}"""

        object_properties = [
            {"Column Name": object.Name},
            {"Object Type": object.ObjectType},
            {"Type": object.Type},
            {"Is Available In Excel": object.IsAvailableInMDX},
            {"Is Hidden": object.IsHidden},
            {"Data Category": object.DataCategory},
            {"Data Type": object.DataType},
            {"Display Folder": object.DisplayFolder},
        ]

        obj_text = [
            f"### {obj_heading}",
            "**Description**:",
            f"> {obj_description}",
            "",
            f"{self.generate_object_properties(object_properties)}",
        ]

        if str(object.Type) == "Calculated":
            obj_text.extend(
                (
                    f'```dax title="Technical: {object.Name}"',
                    f"  {object.Expression}",
                    "```",
                )
            )
        obj_text.append("---")

        return "\n".join(obj_text)

    def generate_markdown_column_page(
        self, object: PyTable, object_caption: str, page_index: int = 2
    ) -> str:
        """This function generates the markdown for the colums documentation.

        Returns:
            str: Will be appended to the page text.
        """
        markdown_template = [
            "---",
            f"sidebar_position: {page_index}",
            f"sidebar_label: {object_caption}",
            f"title: {object_caption}",
            f"description: This page contains all columns with "
            f"Columns for {self.model.Name} "
            "including the description, format string, and other technical details.",
            "---",
            "",
        ]

        markdown_template.extend(
            self.create_markdown_for_column(column)
            for column in object.Columns
            if "RowNumber" not in column.Name
        )
        return "\n".join(markdown_template)

    def generate_general_info_file(self) -> str:
        """Index.md file for the model.

        Basic text for an introduction page.

        Returns:
            str: Markdown str for info page
        """
        return "\n".join(
            [
                "---",
                "sidebar_position: 1",
                f"title: {self.model_name}",
                "description: This page contains all measures for the Model model,"
                "including the description,"
                "format string, and other technical details.",
                "---",
                "",
                "## General information",
                "### Business Owners",
                "",
                "## Information Sources",
            ]
        )

    @staticmethod
    def generate_object_properties(properties: List[Dict[str, str]]) -> str:
        """Generate the section for object properties.

        You can select your own properties to display
        by providing a the properties in a list of
        dicts.

        Args:
            properties (dict): The ones you want to show.

        Returns:
            str: HTML used in the markdown.

        Example:
            ```python
                [
                    { "Display Folder": "Sales Order Information" },
                    { "Is Hidden": "False" },
                    { "Format String": "#.###,## }
                ]
            ```
            Returns:
            ```
            <dl>
                <dt>Display Folder</dt>
                <dd>Sales Order Information</dd>

                <dt>Is Hidden</dt>
                <dd>False</dd>

                <dt>Format String</dt>
                <dd>#.###,##</dd>
            </dl>
            ```
        """
        obj_text = ["<dl>"]

        for obj_prop in properties:
            for caption, text in obj_prop.items():
                save_text = str(text).replace("\\", " > ")
                obj_text.extend(
                    (f"  <dt>{caption}</dt>", f"  <dd>{save_text}</dd>", "")
                )
        obj_text.extend(("</dl>", ""))
        return "\n".join(obj_text)

    @staticmethod
    def set_url_friendly_name(page_name: str) -> str:
        """Replaces the model name to a friendly string, so it can be used in an URL.

        Returns:
            str: Friendly model name used in url for docs.
        """
        # return (self.model_name).replace(" ", "-").replace("_", "-").lower()
        return (
            page_name.replace(" ", "-")
            .replace("_", "-")
            .lower()
            .replace("[", "")
            .replace("]", "")
        )
