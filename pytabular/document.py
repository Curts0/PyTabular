import logging

from pathlib import Path

from measure import PyMeasure
from table import PyTable
from column import PyColumn
from culture import PyCulture

from .pytabular import Tabular

logger = logging.getLogger("PyTabular")


class ModelDocumenter:
    def __init__(
        self,
        model: Tabular,
        friendly_name: str = str(),
        save_location: str = "model-docs",
        general_page_url: str = "1-general-information.md",
        measure_page_url: str = "2-measures.md",
        table_page_url: str = "3-tables.md",
        column_page_url: str = "4-columns.md",
        roles_page_url: str = "5-roles.md",
    ):
        self.model = model
        self.save_path: Path
        self.friendly_name: str = str()
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

        self.category_file_name: str = "_category_.yml"
        self.general_page_url: str = general_page_url
        self.measure_page_url: str = measure_page_url
        self.table_page_url: str = table_page_url
        self.column_page_url: str = column_page_url
        self.roles_page_url: str = roles_page_url

        # Gen
        if friendly_name:
            self.friendly_name: str = self.set_model_friendly_name()
        else:
            self.friendly_name: str = friendly_name

        # Initialize Save path so checks can be run against it.
        self.save_path = self.set_save_path()

    def generate_documentation_pages(self) -> None:
        self.measure_page = self.generate_markdown_measure_page()
        self.table_page = self.generate_markdown_table_page()
        self.column_page = self.generate_markdown_column_page()
        self.category_page = self.generate_category_file()

    def get_object_caption(self, object_name: str, object_parent: str):
        return self.culture_object.get_translation(
            object_name=object_name, object_parent_name=object_parent
        ).get("object_translation")

    def set_translations(
        self, enable_translations: bool = False, culture: str = "en-US"
    ) -> None:
        """
        Set translations to active or inactive, depending on the needs of the users.
        """

        logger.info(f"Using Translations set to > {enable_translations}")

        if enable_translations:
            try:
                self.culture_object = self.model.Cultures[culture]
                self.translation_culture = culture
                self.translation_include = enable_translations
            except IndexError:
                self.translation_include = False
                logger.warn(
                    "Culture not found, reverting back to orginal setting > False"
                )
            else:
                logger.info(f"Setting culture to {self.translation_culture}")

        else:
            self.translation_include = enable_translations

    def set_model_friendly_name(self):
        """
        Replaces the model name to a friendly string,
        so it can be used in an URL.
        """
        return (self.model.Catalog).replace(" ", "-").replace("_", "-").lower()

    def set_save_path(self) -> Path:
        return Path(f"{self.save_location}/{self.friendly_name}")

    def save_page(self, content: str, page_name: str, keep_file: bool = False) -> None:
        """Save the content of the documentation to a file, based on
            the class setup.
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
            logger.info(f"{page_name} already exists -> fill will not overwritten.")
        else:
            logger.info(f"Results are written to -> {page_name}.")

            with target_file.open("w", encoding="utf-8") as f:
                f.write(content)
                f.close()

    def save_documentation(self) -> None:
        """Generate documentation of the model, based on the meta-data
            in the model definitions. This first checks if the folder
            exists, and then starts to export the files that are needed
            for the documentatation.
                - General Information Page -> Free format page to create.
                - Measure Page -> Describes the measures in the model. (Incl. OLS?)
                - Tables Page -> Describes the tables in the model. (Incl. OLS?)
                - Columns Page -> Describes all columns in the model. (Incl. OLS?)
                - Roles Page -> Describes the roles in the model, (incl. RLS?)

        Args:
            self (Docs): Model object for documentation.

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
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )
        return f"""
### {object_caption}
Description: {object.Description or 'No Description available'}
<dl>

<dt>Display Folder</dt>
<dd>{object.DisplayFolder}</dd>

<dt>Table Name</dt>
<dd>{object.Parent.Name}</dd>

<dt>Format String</dt>
<dd>{object.FormatString}</dd>

<dt>Is Hidden</dt>
<dd>{object.IsHidden}</dd>

</dl>

```dax title="Technical: {object.Name}"
{
    object.Expression
}
```

---
"""

    def generate_markdown_measure_page(self) -> str:
        prevDisplayFolder = ""
        markdown_template = [
            f"""---
sidebar_position: 3
title: Measures
description: This page contains all measures for the {self.model.Name} model, including the description, format string, and other technical details.
---

# Measures for {self.model.Name}
"""
        ]

        measures = sorted(
            self.model.Measures, key=lambda x: x.DisplayFolder, reverse=False
        )

        for measure in measures:
            logger.debug(f"Creating docs for {measure.Name}")
            displayFolder = measure.DisplayFolder or "Other"
            displayFolder = displayFolder.split("\\")[0]

            if prevDisplayFolder != displayFolder:
                markdown_template.append(f"""## {displayFolder}""")
                prevDisplayFolder = displayFolder

            markdown_template.append(self.create_markdown_for_measure(measure))

        return "".join(markdown_template)

    def create_markdown_for_table(self, object: PyTable) -> str:
        """
        This functions returns the markdwon that can be used
        for the documentation page for Tables.

        Args:
            object: PyTable -> Based on the PyTabular Package.

        Returns:
            Markdown text: str -> Will be append to the page text.
        """
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )
        return f"""
### {object_caption}
Description: {object.Description or 'No Description available'}
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

```{'dax' if str(object.Partitions[0].SourceType) == 'Calculated' else 'powerquery'} title="Table Source: {object.Name}"
{
    object.Partitions[0].Source.Expression if str(object.Partitions[0].SourceType) != "CalculationGroup" else 'N/A'
}
```

---

"""

    def generate_markdown_table_page(self) -> str:
        """
        This function generates the markdown tables documentation for the Calculated columns in the Model.
        TODO:
            - Add the Translations for tables.
        """
        markdown_template = f"""---
sidebar_position: 2
title: Tables
description: This page contains all columns with tables for {self.model.Name}, including the description, and technical details.
---

# Tables {self.model.Name}

    """

        for table in self.model.Tables:
            markdown_template += self.create_markdown_for_table(table)

        return markdown_template

    def generate_markdown_column_page(self) -> str:
        """
        This function generates the markdown tables documentation for the Calculated columns in the Model.
        TODO:
            - Add the Translations for tables.
        """
        markdown_template = f"""---
sidebar_position: 4
title: Columns
description: This page contains all columns with Columns for {self.model.Name}, including the description, format string, and other technical details.
---

    """

        for table in self.model.Tables:
            markdown_template += f"""
## Columns: {table.Name}
                                """

            for column in table.Columns:
                if "RowNumber" in column.Name:
                    continue

                markdown_template += self.create_markdown_for_column(column)

        return markdown_template

    def create_markdown_for_column(self, object: PyColumn) -> str:
        object_caption = (
            self.get_object_caption(
                object_name=object.Name, object_parent=object.Parent.Name
            )
            or object.Name
        )
        basic_info = f"""
### [{object.Parent.Name}]{object_caption}
Description: {object.Description or 'No Description available'}
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

</dl>
"""

        if str(object.Type) == "Calculated":
            basic_info += f"""
```dax title="Technical: {object.Name}"
{
    object.Expression
}
```
    """
        return (
            basic_info
            + """
---
    """
        )

    def generate_category_file(self):
        return f"""position: 2 # float position is supported
label: '{self.model.Catalog}'
collapsible: true # make the category collapsible
collapsed: true # keep the category open by default
link:
  type: generated-index
  title: Documentation Overview
customProps:
  description: To be added in the future.
    """
