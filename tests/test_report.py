"""Tests for the report module."""

from docdraft.models import Clause, Document, DocumentType
from docdraft.report import ReportGenerator


class TestReportGenerator:
    def test_empty_report(self):
        gen = ReportGenerator()
        assert gen.summary() == "No documents have been generated yet."
        assert gen.reports == []

    def test_add_document(self):
        gen = ReportGenerator()
        doc = Document(title="Test NDA", document_type=DocumentType.NDA)
        doc.add_clause(Clause(id="c1", title="A", body="Body text here."))

        report = gen.add_document(doc, "Some formatted text with several words")

        assert report.title == "Test NDA"
        assert report.document_type == "nda"
        assert report.clause_count == 1
        assert report.word_count == 7
        assert report.has_optional_clauses is False

    def test_add_document_with_optional_clauses(self):
        gen = ReportGenerator()
        doc = Document(title="Test", document_type=DocumentType.EMPLOYMENT)
        doc.add_clause(Clause(id="c1", title="A", body="B", is_optional=True))

        report = gen.add_document(doc, "text")
        assert report.has_optional_clauses is True

    def test_multiple_documents(self):
        gen = ReportGenerator()

        doc1 = Document(title="NDA", document_type=DocumentType.NDA)
        doc2 = Document(title="Employment", document_type=DocumentType.EMPLOYMENT)

        gen.add_document(doc1, "text one")
        gen.add_document(doc2, "text two")

        assert len(gen.reports) == 2

    def test_summary_format(self):
        gen = ReportGenerator()
        doc = Document(title="Test NDA", document_type=DocumentType.NDA)
        doc.add_clause(Clause(id="c1", title="A", body="Body"))

        gen.add_document(doc, "Some words here")
        summary = gen.summary()

        assert "DOCDRAFT" in summary
        assert "Total documents generated: 1" in summary
        assert "Test NDA" in summary
        assert "nda" in summary
