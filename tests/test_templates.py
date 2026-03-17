"""Tests for legal document templates."""

import pytest

from docdraft.models import DocumentType, NDAVariant, Party, Term
from docdraft.templates.employment import EmploymentAgreementTemplate
from docdraft.templates.freelance import FreelanceContractTemplate
from docdraft.templates.nda import NDATemplate
from docdraft.templates.privacy import PrivacyPolicyTemplate
from docdraft.templates.service import ServiceAgreementTemplate
from docdraft.templates.terms import TermsOfServiceTemplate


@pytest.fixture
def party1():
    return Party(name="Acme Corporation", address="123 Main St, NY")


@pytest.fixture
def party2():
    return Party(name="Jane Smith", address="456 Oak Ave, CA")


class TestNDATemplate:
    def test_mutual_nda(self, party1, party2):
        template = NDATemplate()
        doc = template.generate(party1, party2, variant=NDAVariant.MUTUAL)

        assert doc.title == "MUTUAL NON-DISCLOSURE AGREEMENT"
        assert doc.document_type == DocumentType.NDA
        assert len(doc.parties) == 2
        assert len(doc.clauses) >= 8
        assert doc.metadata["variant"] == "mutual"
        assert "mutual" in doc.preamble.lower() or "Mutual" in doc.preamble

    def test_unilateral_nda(self, party1, party2):
        template = NDATemplate()
        doc = template.generate(party1, party2, variant=NDAVariant.UNILATERAL)

        assert doc.title == "UNILATERAL NON-DISCLOSURE AGREEMENT"
        assert doc.metadata["variant"] == "unilateral"
        assert "Disclosing Party" in doc.preamble

    def test_nda_has_key_clauses(self, party1, party2):
        template = NDATemplate()
        doc = template.generate(party1, party2)

        clause_ids = [c.id for c in doc.clauses]
        assert "nda-definition" in clause_ids
        assert "nda-exclusions" in clause_ids
        assert "nda-obligations" in clause_ids
        assert "nda-return" in clause_ids
        assert "nda-remedies" in clause_ids
        assert "nda-governing-law" in clause_ids

    def test_nda_has_signature_block(self, party1, party2):
        template = NDATemplate()
        doc = template.generate(party1, party2)

        assert doc.signature_block
        assert party1.name in doc.signature_block
        assert party2.name in doc.signature_block

    def test_nda_contains_legal_language(self, party1, party2):
        template = NDATemplate()
        doc = template.generate(party1, party2)

        definition = doc.get_clause("nda-definition")
        assert definition is not None
        assert "trade secrets" in definition.body
        assert "proprietary" in definition.body

        remedies = doc.get_clause("nda-remedies")
        assert remedies is not None
        assert "irreparable harm" in remedies.body
        assert "equitable relief" in remedies.body


class TestEmploymentAgreementTemplate:
    def test_employment_agreement(self, party1, party2):
        template = EmploymentAgreementTemplate()
        doc = template.generate(
            employer=party1,
            employee=party2,
            job_title="Software Engineer",
            salary="$150,000",
        )

        assert doc.title == "EMPLOYMENT AGREEMENT"
        assert doc.document_type == DocumentType.EMPLOYMENT
        assert len(doc.clauses) >= 8
        assert doc.metadata["job_title"] == "Software Engineer"
        assert doc.metadata["salary"] == "$150,000"

    def test_employment_has_key_clauses(self, party1, party2):
        template = EmploymentAgreementTemplate()
        doc = template.generate(employer=party1, employee=party2)

        clause_ids = [c.id for c in doc.clauses]
        assert "emp-position" in clause_ids
        assert "emp-compensation" in clause_ids
        assert "emp-confidentiality" in clause_ids
        assert "emp-ip" in clause_ids
        assert "emp-termination" in clause_ids

    def test_employment_non_compete_is_optional(self, party1, party2):
        template = EmploymentAgreementTemplate()
        doc = template.generate(employer=party1, employee=party2)

        non_compete = doc.get_clause("emp-non-compete")
        assert non_compete is not None
        assert non_compete.is_optional is True
        assert non_compete.jurisdiction_notes is not None

    def test_employment_contains_legal_language(self, party1, party2):
        template = EmploymentAgreementTemplate()
        doc = template.generate(employer=party1, employee=party2)

        ip_clause = doc.get_clause("emp-ip")
        assert ip_clause is not None
        assert "works made for hire" in ip_clause.body
        assert "assigns" in ip_clause.body


class TestServiceAgreementTemplate:
    def test_service_agreement(self, party1, party2):
        template = ServiceAgreementTemplate()
        doc = template.generate(
            provider=party1, client=party2, fee="$10,000 per month"
        )

        assert doc.title == "SERVICE AGREEMENT"
        assert doc.document_type == DocumentType.SERVICE
        assert len(doc.clauses) >= 9

    def test_service_has_key_clauses(self, party1, party2):
        template = ServiceAgreementTemplate()
        doc = template.generate(provider=party1, client=party2)

        clause_ids = [c.id for c in doc.clauses]
        assert "svc-scope" in clause_ids
        assert "svc-compensation" in clause_ids
        assert "svc-ip" in clause_ids
        assert "svc-confidentiality" in clause_ids
        assert "svc-liability" in clause_ids
        assert "svc-indemnification" in clause_ids

    def test_service_independent_contractor(self, party1, party2):
        template = ServiceAgreementTemplate()
        doc = template.generate(provider=party1, client=party2)

        misc = doc.get_clause("svc-miscellaneous")
        assert misc is not None
        assert "independent contractor" in misc.body.lower()


class TestFreelanceContractTemplate:
    def test_freelance_contract(self, party1, party2):
        template = FreelanceContractTemplate()
        doc = template.generate(
            freelancer=party2, client=party1, rate="$100 per hour"
        )

        assert doc.title == "INDEPENDENT CONTRACTOR AGREEMENT"
        assert doc.document_type == DocumentType.FREELANCE
        assert len(doc.clauses) >= 8

    def test_freelance_has_contractor_relationship(self, party1, party2):
        template = FreelanceContractTemplate()
        doc = template.generate(freelancer=party2, client=party1)

        relationship = doc.get_clause("free-relationship")
        assert relationship is not None
        assert "independent contractor" in relationship.body.lower()
        assert "not an employee" in relationship.body.lower()
        assert "self-employment taxes" in relationship.body.lower()

    def test_freelance_ip_portfolio_rights(self, party1, party2):
        template = FreelanceContractTemplate()
        doc = template.generate(freelancer=party2, client=party1)

        ip_clause = doc.get_clause("free-ip")
        assert ip_clause is not None
        assert "Portfolio Rights" in ip_clause.body


class TestPrivacyPolicyTemplate:
    def test_privacy_policy(self):
        company = Party(name="MyApp Inc", email="privacy@myapp.com")
        template = PrivacyPolicyTemplate()
        doc = template.generate(company=company, website="https://myapp.com")

        assert doc.title == "PRIVACY POLICY"
        assert doc.document_type == DocumentType.PRIVACY
        assert len(doc.clauses) >= 9

    def test_privacy_has_key_sections(self):
        company = Party(name="MyApp Inc")
        template = PrivacyPolicyTemplate()
        doc = template.generate(company=company)

        clause_ids = [c.id for c in doc.clauses]
        assert "priv-collection" in clause_ids
        assert "priv-use" in clause_ids
        assert "priv-sharing" in clause_ids
        assert "priv-cookies" in clause_ids
        assert "priv-security" in clause_ids
        assert "priv-rights" in clause_ids
        assert "priv-children" in clause_ids

    def test_privacy_children_clause(self):
        company = Party(name="MyApp Inc")
        template = PrivacyPolicyTemplate()
        doc = template.generate(company=company)

        children = doc.get_clause("priv-children")
        assert children is not None
        assert "thirteen (13)" in children.body

    def test_privacy_no_signature_block(self):
        company = Party(name="MyApp Inc")
        template = PrivacyPolicyTemplate()
        doc = template.generate(company=company)
        assert doc.signature_block == ""


class TestTermsOfServiceTemplate:
    def test_terms_of_service(self):
        company = Party(name="SaaS Corp")
        template = TermsOfServiceTemplate()
        doc = template.generate(company=company, website="https://saas.example.com")

        assert doc.title == "TERMS OF SERVICE"
        assert doc.document_type == DocumentType.TERMS
        assert len(doc.clauses) >= 12

    def test_terms_has_key_sections(self):
        company = Party(name="SaaS Corp")
        template = TermsOfServiceTemplate()
        doc = template.generate(company=company)

        clause_ids = [c.id for c in doc.clauses]
        assert "tos-eligibility" in clause_ids
        assert "tos-accounts" in clause_ids
        assert "tos-acceptable-use" in clause_ids
        assert "tos-content" in clause_ids
        assert "tos-ip" in clause_ids
        assert "tos-disclaimers" in clause_ids
        assert "tos-liability" in clause_ids

    def test_terms_disclaimers_uppercase(self):
        company = Party(name="SaaS Corp")
        template = TermsOfServiceTemplate()
        doc = template.generate(company=company)

        disclaimers = doc.get_clause("tos-disclaimers")
        assert disclaimers is not None
        assert "AS IS" in disclaimers.body
        assert "AS AVAILABLE" in disclaimers.body

    def test_terms_no_signature_block(self):
        company = Party(name="SaaS Corp")
        template = TermsOfServiceTemplate()
        doc = template.generate(company=company)
        assert doc.signature_block == ""
