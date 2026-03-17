"""Document generation reporting."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from docdraft.models import Document


class DocumentReport(BaseModel):
    """Report entry for a generated document."""

    title: str
    document_type: str
    parties: list[str]
    clause_count: int
    jurisdiction: str
    industry: str
    generated_at: datetime = Field(default_factory=datetime.now)
    word_count: int = 0
    has_optional_clauses: bool = False


class ReportGenerator:
    """Generates summary reports for created documents."""

    def __init__(self) -> None:
        self._reports: list[DocumentReport] = []

    @property
    def reports(self) -> list[DocumentReport]:
        return list(self._reports)

    def add_document(self, document: Document, formatted_text: str) -> DocumentReport:
        """Create a report entry for a generated document."""
        words = len(formatted_text.split())
        has_optional = any(c.is_optional for c in document.clauses)

        report = DocumentReport(
            title=document.title,
            document_type=document.document_type.value,
            parties=[p.name for p in document.parties],
            clause_count=len(document.clauses),
            jurisdiction=document.jurisdiction.value,
            industry=document.industry.value,
            generated_at=document.created_at,
            word_count=words,
            has_optional_clauses=has_optional,
        )
        self._reports.append(report)
        return report

    def summary(self) -> str:
        """Generate a text summary of all reports."""
        if not self._reports:
            return "No documents have been generated yet."

        lines = [
            "DOCDRAFT - Document Generation Report",
            "=" * 40,
            f"Total documents generated: {len(self._reports)}",
            "",
        ]

        for i, report in enumerate(self._reports, 1):
            lines.append(f"Document {i}: {report.title}")
            lines.append(f"  Type:         {report.document_type}")
            lines.append(f"  Parties:      {', '.join(report.parties)}")
            lines.append(f"  Clauses:      {report.clause_count}")
            lines.append(f"  Word count:   {report.word_count}")
            lines.append(f"  Jurisdiction:  {report.jurisdiction}")
            lines.append(f"  Industry:      {report.industry}")
            lines.append(f"  Generated:     {report.generated_at.strftime('%Y-%m-%d %H:%M')}")
            if report.has_optional_clauses:
                lines.append("  Note:          Contains optional clauses")
            lines.append("")

        return "\n".join(lines)
