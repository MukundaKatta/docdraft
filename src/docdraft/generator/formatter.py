"""DocumentFormatter outputs documents in markdown or plain text."""

from __future__ import annotations

from docdraft.models import Document, OutputFormat


class DocumentFormatter:
    """Formats Document objects into markdown or plain text output."""

    def format(self, document: Document, output_format: OutputFormat = OutputFormat.MARKDOWN) -> str:
        if output_format == OutputFormat.MARKDOWN:
            return self._format_markdown(document)
        return self._format_plain(document)

    def _format_markdown(self, doc: Document) -> str:
        lines: list[str] = []

        # Title
        lines.append(f"# {doc.title}")
        lines.append("")

        # Effective date
        lines.append(f"**Effective Date:** {doc.effective_date.strftime('%B %d, %Y')}")
        lines.append("")

        # Preamble
        if doc.preamble:
            lines.append(doc.preamble)
            lines.append("")

        # Clauses
        for clause in doc.clauses:
            section = f"{clause.section_number}. " if clause.section_number else ""
            lines.append(f"## {section}{clause.title}")
            lines.append("")

            if clause.is_optional:
                lines.append("*[Optional Clause]*")
                lines.append("")

            lines.append(clause.body)
            lines.append("")

            if clause.jurisdiction_notes:
                lines.append(f"> **Jurisdiction Note:** {clause.jurisdiction_notes}")
                lines.append("")

        # Signature block
        if doc.signature_block:
            lines.append("---")
            lines.append("")
            lines.append("## Signatures")
            lines.append("")
            lines.append(doc.signature_block)
            lines.append("")

        return "\n".join(lines)

    def _format_plain(self, doc: Document) -> str:
        lines: list[str] = []
        width = 78

        # Title
        lines.append("=" * width)
        lines.append(doc.title.center(width))
        lines.append("=" * width)
        lines.append("")

        # Effective date
        lines.append(f"Effective Date: {doc.effective_date.strftime('%B %d, %Y')}")
        lines.append("")

        # Preamble
        if doc.preamble:
            lines.append(doc.preamble)
            lines.append("")

        lines.append("-" * width)
        lines.append("")

        # Clauses
        for clause in doc.clauses:
            section = f"{clause.section_number}. " if clause.section_number else ""
            header = f"{section}{clause.title}".upper()
            lines.append(header)
            lines.append("-" * len(header))
            lines.append("")

            if clause.is_optional:
                lines.append("[Optional Clause]")
                lines.append("")

            lines.append(clause.body)
            lines.append("")

            if clause.jurisdiction_notes:
                lines.append(f"[Jurisdiction Note: {clause.jurisdiction_notes}]")
                lines.append("")

        # Signature block
        if doc.signature_block:
            lines.append("=" * width)
            lines.append("SIGNATURES".center(width))
            lines.append("=" * width)
            lines.append("")
            lines.append(doc.signature_block)
            lines.append("")

        return "\n".join(lines)
