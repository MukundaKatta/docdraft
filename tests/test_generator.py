"""Tests for the document generation engine."""

import pytest

from docdraft.generator.builder import DocumentBuilder
from docdraft.generator.customizer import ClauseCustomizer
from docdraft.generator.formatter import DocumentFormatter
from docdraft.models import (
    Clause,
    Document,
    DocumentType,
    Industry,
    Jurisdiction,
    NDAVariant,
    OutputFormat,
    Party,
)


class TestDocumentBuilder:
    def test_build_nda(self):
        builder = DocumentBuilder()
        doc, text = builder.build_nda("Acme Corp", "Jane Doe")

        assert doc.title == "MUTUAL NON-DISCLOSURE AGREEMENT"
        assert len(doc.clauses) > 0
        assert len(text) > 0

    def test_build_nda_unilateral(self):
        builder = DocumentBuilder()
        doc, text = builder.build_nda("Acme Corp", "Jane Doe", variant=NDAVariant.UNILATERAL)

        assert doc.title == "UNILATERAL NON-DISCLOSURE AGREEMENT"

    def test_build_employment(self):
        builder = DocumentBuilder()
        doc, text = builder.build_employment(
            "TechCo Inc", "John Smith", job_title="Engineer", salary="$120,000"
        )

        assert doc.title == "EMPLOYMENT AGREEMENT"
        assert doc.metadata["job_title"] == "Engineer"

    def test_build_service(self):
        builder = DocumentBuilder()
        doc, text = builder.build_service("Dev Agency", "StartupXYZ")

        assert doc.title == "SERVICE AGREEMENT"

    def test_build_freelance(self):
        builder = DocumentBuilder()
        doc, text = builder.build_freelance("Jane Designer", "BigCorp", rate="$100/hr")

        assert doc.title == "INDEPENDENT CONTRACTOR AGREEMENT"

    def test_build_privacy(self):
        builder = DocumentBuilder()
        doc, text = builder.build_privacy("MyApp Inc", website="https://myapp.com")

        assert doc.title == "PRIVACY POLICY"

    def test_build_terms(self):
        builder = DocumentBuilder()
        doc, text = builder.build_terms("SaaS Corp", website="https://saas.example.com")

        assert doc.title == "TERMS OF SERVICE"

    def test_build_generic_dispatch(self):
        builder = DocumentBuilder()
        doc, text = builder.build("nda", party1_name="A", party2_name="B")

        assert doc.document_type == DocumentType.NDA

    def test_build_unknown_type(self):
        builder = DocumentBuilder()
        with pytest.raises(ValueError, match="Unknown document type"):
            builder.build("unknown_type")

    def test_build_with_jurisdiction(self):
        builder = DocumentBuilder(jurisdiction=Jurisdiction.US_CALIFORNIA)
        doc, text = builder.build_nda("Acme", "Bob")

        assert doc.jurisdiction == Jurisdiction.US_CALIFORNIA
        # Check California governing law was applied
        gov_law = doc.get_clause("nda-governing-law")
        assert gov_law is not None
        assert "California" in gov_law.body

    def test_build_with_industry(self):
        builder = DocumentBuilder(industry=Industry.TECHNOLOGY)
        doc, text = builder.build_nda("Acme", "Bob")

        assert doc.industry == Industry.TECHNOLOGY

    def test_build_plain_format(self):
        builder = DocumentBuilder(output_format=OutputFormat.PLAIN)
        doc, text = builder.build_nda("Acme", "Bob")

        # Plain text should not contain markdown headers
        assert "# " not in text
        assert "==" in text


class TestClauseCustomizer:
    def test_california_jurisdiction(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="gov-law",
                title="Governing Law",
                section_number="1",
                body="Laws of [STATE]",
            )
        )

        customizer.customize(doc, Jurisdiction.US_CALIFORNIA, Industry.GENERAL)

        clause = doc.get_clause("gov-law")
        assert "California" in clause.body

    def test_uk_jurisdiction(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="gov-law",
                title="Governing Law",
                section_number="1",
                body="Laws of [STATE]",
            )
        )

        customizer.customize(doc, Jurisdiction.UK, Industry.GENERAL)

        clause = doc.get_clause("gov-law")
        assert "England and Wales" in clause.body

    def test_eu_adds_gdpr_clause(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="gov-law",
                title="Governing Law",
                section_number="1",
                body="Laws of [STATE]",
            )
        )

        customizer.customize(doc, Jurisdiction.EU, Industry.GENERAL)

        gdpr = doc.get_clause("gdpr-compliance")
        assert gdpr is not None
        assert "GDPR" in gdpr.body

    def test_eu_no_duplicate_gdpr(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="gdpr-compliance",
                title="GDPR",
                section_number="1",
                body="Already here",
            )
        )

        customizer.customize(doc, Jurisdiction.EU, Industry.GENERAL)

        gdpr_clauses = [c for c in doc.clauses if c.id == "gdpr-compliance"]
        assert len(gdpr_clauses) == 1

    def test_california_non_compete_warning(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.EMPLOYMENT)
        doc.add_clause(
            Clause(
                id="non-compete",
                title="Non-Competition",
                section_number="1",
                body="Employee shall not compete.",
            )
        )

        customizer.customize(doc, Jurisdiction.US_CALIFORNIA, Industry.GENERAL)

        clause = doc.get_clause("non-compete")
        assert "California" in clause.body
        assert "16600" in clause.body

    def test_technology_industry(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="conf",
                title="Confidentiality",
                section_number="1",
                body="Keep it confidential.",
            )
        )

        customizer.customize(doc, Jurisdiction.US_GENERAL, Industry.TECHNOLOGY)

        clause = doc.get_clause("conf")
        assert "source code" in clause.body
        assert "APIs" in clause.body

    def test_healthcare_industry(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="conf",
                title="Confidentiality",
                section_number="1",
                body="Keep it confidential.",
            )
        )

        customizer.customize(doc, Jurisdiction.US_GENERAL, Industry.HEALTHCARE)

        clause = doc.get_clause("conf")
        assert "HIPAA" in clause.body
        assert "Protected Health Information" in clause.body

    def test_finance_industry(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="conf",
                title="Confidentiality",
                section_number="1",
                body="Keep it confidential.",
            )
        )

        customizer.customize(doc, Jurisdiction.US_GENERAL, Industry.FINANCE)

        clause = doc.get_clause("conf")
        assert "Gramm-Leach-Bliley" in clause.body

    def test_general_industry_no_additions(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(
            Clause(
                id="conf",
                title="Confidentiality",
                section_number="1",
                body="Keep it confidential.",
            )
        )

        customizer.customize(doc, Jurisdiction.US_GENERAL, Industry.GENERAL)

        clause = doc.get_clause("conf")
        assert clause.body == "Keep it confidential."

    def test_renumber_clauses(self):
        customizer = ClauseCustomizer()
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(Clause(id="c1", title="A", section_number="5", body="A"))
        doc.add_clause(Clause(id="c2", title="B", section_number="10", body="B"))
        doc.add_clause(Clause(id="c3", title="C", section_number="15", body="C"))

        customizer.customize(doc, Jurisdiction.US_GENERAL, Industry.GENERAL)

        assert doc.clauses[0].section_number == "1"
        assert doc.clauses[1].section_number == "2"
        assert doc.clauses[2].section_number == "3"


class TestDocumentFormatter:
    @pytest.fixture
    def sample_doc(self):
        doc = Document(
            title="TEST AGREEMENT",
            document_type=DocumentType.NDA,
            preamble="This is the preamble.",
            signature_block="Sign here: ___",
        )
        doc.add_clause(
            Clause(
                id="c1",
                title="First Clause",
                section_number="1",
                body="Body of first clause.",
            )
        )
        doc.add_clause(
            Clause(
                id="c2",
                title="Optional Clause",
                section_number="2",
                body="Body of optional clause.",
                is_optional=True,
                jurisdiction_notes="Some note.",
            )
        )
        return doc

    def test_markdown_format(self, sample_doc):
        formatter = DocumentFormatter()
        output = formatter.format(sample_doc, OutputFormat.MARKDOWN)

        assert "# TEST AGREEMENT" in output
        assert "## 1. First Clause" in output
        assert "## 2. Optional Clause" in output
        assert "*[Optional Clause]*" in output
        assert "> **Jurisdiction Note:**" in output
        assert "## Signatures" in output
        assert "This is the preamble." in output

    def test_plain_format(self, sample_doc):
        formatter = DocumentFormatter()
        output = formatter.format(sample_doc, OutputFormat.PLAIN)

        assert "TEST AGREEMENT" in output
        assert "1. FIRST CLAUSE" in output
        assert "[Optional Clause]" in output
        assert "[Jurisdiction Note:" in output
        assert "SIGNATURES" in output
        assert "# " not in output  # No markdown

    def test_effective_date_included(self, sample_doc):
        formatter = DocumentFormatter()
        output = formatter.format(sample_doc, OutputFormat.MARKDOWN)
        assert "**Effective Date:**" in output

    def test_no_signature_block(self):
        doc = Document(
            title="TEST",
            document_type=DocumentType.PRIVACY,
            signature_block="",
        )
        formatter = DocumentFormatter()
        output = formatter.format(doc, OutputFormat.MARKDOWN)
        assert "Signatures" not in output
