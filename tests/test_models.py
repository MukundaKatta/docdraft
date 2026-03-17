"""Tests for pydantic models."""

from datetime import date

import pytest

from docdraft.models import (
    Clause,
    Document,
    DocumentType,
    Industry,
    Jurisdiction,
    NDAVariant,
    OutputFormat,
    Party,
    Term,
)


class TestParty:
    def test_create_party_minimal(self):
        party = Party(name="Acme Corp")
        assert party.name == "Acme Corp"
        assert party.address == "[ADDRESS]"
        assert party.entity_type == "individual"
        assert party.representative is None

    def test_create_party_full(self):
        party = Party(
            name="TechCo Inc",
            address="123 Main St, San Francisco, CA",
            entity_type="corporation",
            representative="John Doe",
            title="CEO",
            email="john@techco.com",
            state_of_incorporation="Delaware",
        )
        assert party.name == "TechCo Inc"
        assert party.entity_type == "corporation"
        assert party.representative == "John Doe"
        assert party.email == "john@techco.com"

    def test_party_requires_name(self):
        with pytest.raises(Exception):
            Party(name="")


class TestTerm:
    def test_default_term(self):
        term = Term()
        assert term.start_date == date.today()
        assert term.end_date is None
        assert term.auto_renewal is False
        assert term.notice_period_days == 30

    def test_indefinite_term(self):
        term = Term()
        assert term.is_indefinite is True

    def test_fixed_term(self):
        term = Term(duration_months=12)
        assert term.is_indefinite is False
        assert term.duration_months == 12

    def test_auto_renewal_term(self):
        term = Term(duration_months=12, auto_renewal=True, renewal_period_months=6)
        assert term.auto_renewal is True
        assert term.renewal_period_months == 6


class TestClause:
    def test_create_clause(self):
        clause = Clause(
            id="test-clause",
            title="Test Clause",
            body="This is the body of the clause.",
            section_number="1",
        )
        assert clause.id == "test-clause"
        assert clause.title == "Test Clause"
        assert clause.is_optional is False

    def test_optional_clause(self):
        clause = Clause(
            id="opt-clause",
            title="Optional Clause",
            body="This clause is optional.",
            is_optional=True,
        )
        assert clause.is_optional is True


class TestDocument:
    def test_create_document(self):
        doc = Document(
            title="Test Agreement",
            document_type=DocumentType.NDA,
        )
        assert doc.title == "Test Agreement"
        assert doc.document_type == DocumentType.NDA
        assert len(doc.clauses) == 0
        assert doc.jurisdiction == Jurisdiction.US_GENERAL

    def test_add_clause(self):
        doc = Document(title="Test", document_type=DocumentType.NDA)
        clause = Clause(id="c1", title="First", body="Body text")
        doc.add_clause(clause)
        assert len(doc.clauses) == 1
        assert doc.clauses[0].id == "c1"

    def test_get_clause(self):
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(Clause(id="c1", title="First", body="Body"))
        doc.add_clause(Clause(id="c2", title="Second", body="Body"))

        found = doc.get_clause("c2")
        assert found is not None
        assert found.title == "Second"

        assert doc.get_clause("nonexistent") is None

    def test_remove_clause(self):
        doc = Document(title="Test", document_type=DocumentType.NDA)
        doc.add_clause(Clause(id="c1", title="First", body="Body"))
        doc.add_clause(Clause(id="c2", title="Second", body="Body"))

        assert doc.remove_clause("c1") is True
        assert len(doc.clauses) == 1
        assert doc.remove_clause("nonexistent") is False


class TestEnums:
    def test_document_types(self):
        assert DocumentType.NDA.value == "nda"
        assert DocumentType.EMPLOYMENT.value == "employment"
        assert DocumentType.SERVICE.value == "service"
        assert DocumentType.FREELANCE.value == "freelance"
        assert DocumentType.PRIVACY.value == "privacy"
        assert DocumentType.TERMS.value == "terms"

    def test_nda_variants(self):
        assert NDAVariant.MUTUAL.value == "mutual"
        assert NDAVariant.UNILATERAL.value == "unilateral"

    def test_output_formats(self):
        assert OutputFormat.MARKDOWN.value == "markdown"
        assert OutputFormat.PLAIN.value == "plain"

    def test_jurisdictions(self):
        assert len(Jurisdiction) == 9

    def test_industries(self):
        assert Industry.TECHNOLOGY.value == "technology"
        assert Industry.HEALTHCARE.value == "healthcare"
        assert Industry.FINANCE.value == "finance"
        assert Industry.GENERAL.value == "general"
