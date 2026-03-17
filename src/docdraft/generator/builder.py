"""DocumentBuilder assembles documents from templates and user inputs."""

from __future__ import annotations

from docdraft.generator.customizer import ClauseCustomizer
from docdraft.generator.formatter import DocumentFormatter
from docdraft.models import (
    Document,
    DocumentType,
    Industry,
    Jurisdiction,
    NDAVariant,
    OutputFormat,
    Party,
    Term,
)
from docdraft.templates import TEMPLATE_REGISTRY


class DocumentBuilder:
    """Assembles legal documents from templates, user inputs, and customizations."""

    def __init__(
        self,
        jurisdiction: Jurisdiction = Jurisdiction.US_GENERAL,
        industry: Industry = Industry.GENERAL,
        output_format: OutputFormat = OutputFormat.MARKDOWN,
    ):
        self.jurisdiction = jurisdiction
        self.industry = industry
        self.output_format = output_format
        self.customizer = ClauseCustomizer()
        self.formatter = DocumentFormatter()

    def build_nda(
        self,
        party1_name: str,
        party2_name: str,
        variant: NDAVariant = NDAVariant.MUTUAL,
        party1_address: str = "[ADDRESS]",
        party2_address: str = "[ADDRESS]",
        term: Term | None = None,
        **kwargs,
    ) -> tuple[Document, str]:
        """Build an NDA document and return (document, formatted_output)."""
        template = TEMPLATE_REGISTRY["nda"]()
        party1 = Party(name=party1_name, address=party1_address)
        party2 = Party(name=party2_name, address=party2_address)

        doc = template.generate(
            disclosing_party=party1,
            receiving_party=party2,
            variant=variant,
            term=term,
            **kwargs,
        )
        return self._finalize(doc)

    def build_employment(
        self,
        employer_name: str,
        employee_name: str,
        job_title: str = "[JOB TITLE]",
        salary: str = "[SALARY]",
        employer_address: str = "[ADDRESS]",
        employee_address: str = "[ADDRESS]",
        term: Term | None = None,
        **kwargs,
    ) -> tuple[Document, str]:
        """Build an employment agreement."""
        template = TEMPLATE_REGISTRY["employment"]()
        employer = Party(name=employer_name, address=employer_address, entity_type="corporation")
        employee = Party(name=employee_name, address=employee_address)

        doc = template.generate(
            employer=employer,
            employee=employee,
            job_title=job_title,
            salary=salary,
            term=term,
            **kwargs,
        )
        return self._finalize(doc)

    def build_service(
        self,
        provider_name: str,
        client_name: str,
        services_description: str = "[DESCRIPTION OF SERVICES]",
        fee: str = "[FEE AMOUNT]",
        provider_address: str = "[ADDRESS]",
        client_address: str = "[ADDRESS]",
        term: Term | None = None,
        **kwargs,
    ) -> tuple[Document, str]:
        """Build a service agreement."""
        template = TEMPLATE_REGISTRY["service"]()
        provider = Party(name=provider_name, address=provider_address, entity_type="corporation")
        client = Party(name=client_name, address=client_address, entity_type="corporation")

        doc = template.generate(
            provider=provider,
            client=client,
            services_description=services_description,
            fee=fee,
            term=term,
            **kwargs,
        )
        return self._finalize(doc)

    def build_freelance(
        self,
        freelancer_name: str,
        client_name: str,
        project_description: str = "[PROJECT DESCRIPTION]",
        rate: str = "[RATE]",
        freelancer_address: str = "[ADDRESS]",
        client_address: str = "[ADDRESS]",
        term: Term | None = None,
        **kwargs,
    ) -> tuple[Document, str]:
        """Build a freelance contract."""
        template = TEMPLATE_REGISTRY["freelance"]()
        freelancer = Party(name=freelancer_name, address=freelancer_address)
        client = Party(name=client_name, address=client_address, entity_type="corporation")

        doc = template.generate(
            freelancer=freelancer,
            client=client,
            project_description=project_description,
            rate=rate,
            term=term,
            **kwargs,
        )
        return self._finalize(doc)

    def build_privacy(
        self,
        company_name: str,
        website: str = "[WEBSITE URL]",
        company_address: str = "[ADDRESS]",
        company_email: str | None = None,
        **kwargs,
    ) -> tuple[Document, str]:
        """Build a privacy policy."""
        template = TEMPLATE_REGISTRY["privacy"]()
        company = Party(
            name=company_name,
            address=company_address,
            entity_type="corporation",
            email=company_email,
        )

        doc = template.generate(company=company, website=website, **kwargs)
        return self._finalize(doc)

    def build_terms(
        self,
        company_name: str,
        website: str = "[WEBSITE URL]",
        service_name: str = "[SERVICE NAME]",
        company_address: str = "[ADDRESS]",
        company_email: str | None = None,
        **kwargs,
    ) -> tuple[Document, str]:
        """Build terms of service."""
        template = TEMPLATE_REGISTRY["terms"]()
        company = Party(
            name=company_name,
            address=company_address,
            entity_type="corporation",
            email=company_email,
        )

        doc = template.generate(
            company=company, website=website, service_name=service_name, **kwargs
        )
        return self._finalize(doc)

    def build(self, doc_type: str, **kwargs) -> tuple[Document, str]:
        """Generic build method that dispatches to the appropriate builder."""
        builders = {
            "nda": self.build_nda,
            "employment": self.build_employment,
            "service": self.build_service,
            "freelance": self.build_freelance,
            "privacy": self.build_privacy,
            "terms": self.build_terms,
        }
        builder_fn = builders.get(doc_type)
        if builder_fn is None:
            raise ValueError(
                f"Unknown document type: {doc_type}. "
                f"Available types: {', '.join(builders.keys())}"
            )
        return builder_fn(**kwargs)

    def _finalize(self, doc: Document) -> tuple[Document, str]:
        """Apply customization and formatting to a document."""
        doc.jurisdiction = self.jurisdiction
        doc.industry = self.industry

        self.customizer.customize(doc, self.jurisdiction, self.industry)

        formatted = self.formatter.format(doc, self.output_format)
        return doc, formatted
