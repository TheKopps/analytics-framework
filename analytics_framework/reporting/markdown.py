from pathlib import Path
from typing import Any

import pandas as pd

from analytics_framework.core.pipeline_step import PipelineStep


def _escape_markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|")


def dataframe_to_markdown_table(
    df: pd.DataFrame,
    max_rows: int = 10,
) -> str:
    """
    Convert a DataFrame to a simple Markdown table.
    """
    preview = df.head(max_rows).copy()

    columns = [_escape_markdown_cell(column) for column in preview.columns]

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []

    for _, row in preview.iterrows():
        row_values = [_escape_markdown_cell(value) for value in row.tolist()]
        rows.append("| " + " | ".join(row_values) + " |")

    table = "\n".join([header, separator, *rows])

    if len(df) > max_rows:
        table += f"\n\n_Showing {max_rows} of {len(df)} rows._"

    return table


def render_context_value(value: Any, max_rows: int = 10) -> str:
    """
    Render a Python object into Markdown.
    """
    if isinstance(value, pd.DataFrame):
        return dataframe_to_markdown_table(value, max_rows=max_rows)

    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            lines.append(f"- **{key}**: {item}")
        return "\n".join(lines)

    if isinstance(value, list):
        lines = []
        for item in value:
            lines.append(f"- {item}")
        return "\n".join(lines)

    return f"```text\n{value}\n```"


def render_markdown_report(
    title: str,
    sections: list[dict[str, str]],
) -> str:
    """
    Render a Markdown report from a list of sections.
    """
    content = f"# {title}\n\n"

    for section in sections:
        section_title = section["title"]
        section_content = section["content"]

        content += f"## {section_title}\n\n"
        content += f"{section_content}\n\n"

    return content


def write_markdown_report(
    content: str,
    output_path: str | Path,
) -> Path:
    """
    Write Markdown content to a file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(content, encoding="utf-8")

    return output_path


class MarkdownReportStep(PipelineStep):
    """
    Pipeline step used to generate a Markdown report from context values.
    """

    def __init__(
        self,
        title: str,
        output_path: str | Path,
        context_keys: list[str],
        output_key: str = "markdown_report_path",
        max_rows: int = 10,
        name: str = "Generate Markdown Report",
    ):
        super().__init__(name)
        self.title = title
        self.output_path = Path(output_path)
        self.context_keys = context_keys
        self.output_key = output_key
        self.max_rows = max_rows

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        sections = []

        for key in self.context_keys:
            if key not in context:
                raise KeyError(f"Context key not found: {key}")

            sections.append(
                {
                    "title": key.replace("_", " ").title(),
                    "content": render_context_value(
                        context[key],
                        max_rows=self.max_rows,
                    ),
                }
            )

        report_content = render_markdown_report(
            title=self.title,
            sections=sections,
        )

        report_path = write_markdown_report(
            content=report_content,
            output_path=self.output_path,
        )

        context[self.output_key] = report_path

        return context
