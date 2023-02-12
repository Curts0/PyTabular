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
        general_page_url: str = "1-general-information.md",
        measure_page_url: str = "2-measures.md",
        table_page_url: str = "3-tables.md",
        column_page_url: str = "4-columns.md",
        roles_page_url: str = "5-roles.md",
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
                Defaults to "1-general-information.md".
            measure_page_url (str, optional): Name of the `md` file for measures.
                Defaults to "2-measures.md".
            table_page_url (str, optional): Name of the `md` file for tables.
                Defaults to "3-tables.md".
            column_page_url (str, optional): Name of the `md` file for columns.
                Defaults to "4-columns.md".
            roles_page_url (str, optional): Name of the `md` file for roles.
                Defaults to "5-roles.md".
        """
        self.model = model
        self.model_name = friendly_name or model.Catalog or model.Database.Name
        self.friendly_name: str = str()
        self.save_path: Path
        self.save_location: str = save_location

        # Translation information
        self.culture_include: bool = False
        self.culture_selected: str = "en-US"
        self.culture_object: PyCulture = None

        # Documentation Parts
        self.general_page: str = str()
        self.measure_page: str = str()
        self.table_page: str = str()
        self.column_page: str = str()
        self.roles_page: str = str()
        self.category_page: str = str()

        self.category_file_name: str = "_category_.yml"
        self.general_page_url: str = general_page_url
        self.measure_page_url: str = measure_page_url
        self.table_page_url: str = table_page_url
        self.column_page_url: str = column_page_url
        self.roles_page_url: str = roles_page_url

        # Generate an url friendly name for the model / folder
        self.friendly_name: str = self.set_model_friendly_name()

        # Initialize Save path so checks can be run against it.
        self.save_path = self.set_save_path()

    def create_object_reference(self, object: str, object_parent: str) -> str:
        """Create a Custom ID for link sections in the docs.

        This is based on the technical names in the model,
        so not the once in the translations. This makes it
        possible to link based on dependencies.
        """
        url_reference = f"{object_parent}-{object}".replace(" ", "")
        return f"{{#{url_reference}}}"

    def generate_documentation_pages(self) -> None:
        """Generate Documentation for each specific part of the model."""
        self.measure_page = self.generate_markdown_measure_page()
        self.table_page = self.generate_markdown_table_page()
        self.column_page = self.generate_markdown_column_page()
        self.category_page = self.generate_category_file()

    def get_object_caption(self, object_name: str, object_parent: str):
        """Retrieves the caption of an object, based on the translations in the culture."""
        if self.culture_include:
            return self.culture_object.get_translation(
                object_name=object_name, object_parent_name=object_parent
            ).get("object_translation")

        return object_name

    def set_translations(
        self, enable_translations: bool = False, culture: str = "en-US"
    ) -> None:
        """Set translations to active or inactive, depending on the needs of the users."""
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

    def set_model_friendly_name(self):
        """Replaces the model name to a friendly string, so it can be used in an URL."""
        return (self.model_name).replace(" ", "-").replace("_", "-").lower()

    def set_save_path(self) -> Path:
        """Set the location of the documentation."""
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
        - Measure Page -> Describes the measures in the model. (Incl. OLS?)
        - Tables Page -> Describes the tables in the model. (Incl. OLS?)
        - Columns Page -> Describes all columns in the model. (Incl. OLS?)
        - Roles Page -> Describes the roles in the model, (incl. RLS?)

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

        if self.category_page:
            self.save_page(
                content=self.category_page,
                keep_file=True,
                page_name=self.category_file_name,
            )

        # Create General information page.
        if self.general_page:
            self.save_page(
                content="General Info", keep_file=True, page_name=self.general_page_url
            )

        if self.measure_page:
            self.save_page(
                content=self.measure_page,
                keep_file=False,
                page_name=self.measure_page_url,
            )

        if self.table_page:
            self.save_page(
                content=self.table_page, keep_file=False, page_name=self.table_page_url
            )

        if self.column_page:
            self.save_page(
                content=self.column_page,
                keep_file=False,
                page_name=self.column_page_url,
            )

        if self.roles_page:
            self.save_page(
                content=self.roles_page, keep_file=False, page_name=self.roles_page_url
            )

    def create_markdown_for_measure(self, object: PyMeasure) -> str:
        """Create Markdown for a specific measure.

        That can later on be used for generating the whole measure page.
        """
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )

        object_description = (object.Description or "No Description available").replace(
            "\\n", ""
        )

        object_properties = ''

        obj_text = [
            f"### {object_caption}",
            "**Description**:",
            f"> {object_description}",
            ""
            f"{object_properties}",
            "",
            f'```dax title="Technical: {object.Name}"',
            f"  {object.Expression}",
            "```",
            "---"
        ]
        return "\n".join(obj_text)

    def generate_markdown_measure_page(self) -> str:
        """Based on the measure objects it generates a measure page."""
        prev_display_folder = ""
        markdown_template = [
            "---",
            "sidebar_position: 3",
            "title: Measures",
            f"description: This page contains all measures for the {self.model.Name} model, including the description, format string, and other technical details."
            "---"
            "",
            f"# Measures for {self.model.Name}"
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

        object_description = (object.Description or "No Description available").replace(
            "\\n", ""
        )

        object_details = ''
        """
            <dl>
            <dt>Measures (#)</dt>
            <dd>{len(object.Measures)}</dd>

            <dt>Columns (#)</dt>
            <dd>{len(object.Columns)}</dd>

            <dt>Partitions (#)</dt>
            <dd>{len(object.Partitions)}</dd>

            <dt>Data Category</dt>
            <dd>{object.DataCategory or "Regular Table"}</dd>

            <dt>Is Hidden</dt>
            <dd>{object.IsHidden}</dd>

            <dt>Table Type</dt>
            <dd>{object.Partitions[0].ObjectType}</dd>

            <dt>Source Type</dt>
            <dd>{object.Partitions[0].SourceType}</dd>
            </dl>
        """

        partition_type = ""
        partition_source = ""

        if str(object.Partitions[0].SourceType) == "Calculated":
            partition_type = "dax"
            partition_source = object.Partitions[0].Source.Expression
        elif str(object.Partitions[0].SourceType) == "M":
            partition_type = "powerquery"
            partition_source = object.Partitions[0].Source.Expression
        else:
            partition_type = "sql"
            partition_source = object.Partitions[0].Source.Query

        obj_text = [
            f"### {object_caption}",
            "**Description**: ",
            "> {object_description}",
            "",
            f"{object_details}",
            "", 
            f"```{partition_type} title="Table Source: {object.Name}",
            f"   {partition_source}",
            "```",
            "---"
        ]

    def generate_markdown_table_page(self) -> str:
        """This function generates the markdown tables documentation for the tables in the Model."""
        markdown_template = [
            "---",
            "sidebar_position: 2",
            "title: Tables",
            f"description: This page contains all columns with tables for {self.model.Name}, including the description, and technical details.",
            "---",
            f"# Tables {self.model.Name}"
        ]

        for table in self.model.Tables:
            markdown_template.append(self.create_markdown_for_table(table))

        return "\n".join(markdown_template) 

    def generate_markdown_column_page(self) -> str:
        """This function generates the markdown for documentation about columns in the Model."""
        markdown_template = [
            "---"
            "sidebar_position: 4"
            f"title: Columns description: This page contains all columns with Columns for {self.model.Name}, including the description, format string, and other technical details."
            "---"
        ]

        for table in self.model.Tables:
            markdown_template.append(f"## Columns for {table.Name}")

            for column in table.Columns:
                if "RowNumber" in column.Name:
                    continue

                markdown_template.append(self.create_markdown_for_column(column))

        return "\n".join(markdown_template)

    def create_markdown_for_column(self, object: PyColumn) -> str:
        """Generates the Markdown for a specifc column.

        If a colums is calculated, then it also shows
        the expression for that column in DAX.
        """
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )

        object_description = object.Description.replace("\\n", "") or "No Description available"

        object_heading = f"""{object_caption} {self.create_object_reference( object=object.Name, object_parent=object.Parent.Name)}"""

        object_details = ''
        """
        <dl>
            <dt>Column Name</dt>
            <dd>{object.Name}</dd>

            <dt>Object Type</dt>
            <dd>{object.ObjectType}</dd>

            <dt>Type</dt>
            <dd>{object.Type}</dd>

            <dt>Is Available In Excel</dt>
            <dd>{object.IsAvailableInMDX}</dd>

            <dt>Is Hidden</dt>
            <dd>{object.IsHidden}</dd>

            <dt>Data Category</dt>
            <dd>{object.DataCategory}</dd>

            <dt>Data Type</dt>
            <dd>{object.DataType}</dd>

            <dt>DisplayFolder</dt>
            <dd>{object.DisplayFolder}</dd>

        </dl>"""
        obj_text = [
            f"### {object_heading}", 
            "**Description**:"
            f"> {object_description}"
            "",
            f"{object_details}"
        ]

        if str(object.Type) == "Calculated":
            obj_text.append[
                f"```dax title="Technical: {object.Name}",
                f"  {object.Expression}",
                "```"
            ]

        obj_text.append("---")

        return "\n".join(obj_text)
        
    def generate_category_file(self):
        """Docusaurs can generate an index.

        The category yaml will make that happen.
        """

        obj_text = [
            "position: 2 # float position is supported",
            f"label: '{self.model_name}'",
            "collapsible: true # make the category collapsible",
            "collapsed: true # keep the category open by default",
            "   link:",
            "   type: generated-index",
            "   title: Documentation Overview",
            "customProps:",
            "   description: To be added in the future."
        ]    

        return "\n".join(obj_text)
    @staticmethod 
    def select_object_properties(self, properties : list[dict]) -> str:
        """
        Generate the section for object properties,
        you can select your own properties to display
        by providing a the properties in a list of 
        dicts.

        Args:
            Self.
            Properties (dict): The ones you want to show. 
    
        Returns:
            str:
    
        Examples: 
        
            Input
            ```
                [
                    { "Display Folder": "Sales Order Information" },
                    { "Is Hidden": "False" }, 
                    { "Format String": "#.###,## }
                ]
            ```
            
            Output: 
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

        obj_text = [
            "<dl>"
        ]

        for obj_prop in properties:
            for caption, text in obj_prop.items():
                obj_text.append(f"  <dt>{caption}</dt>")
                obj_text.append(f"  <dd>{text}</dd>")
                obj_text.append(f"")

        obj_text.append("</dl>")

        return "\n".join(obj_text)
