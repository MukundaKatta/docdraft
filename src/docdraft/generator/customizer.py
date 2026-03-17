"""ClauseCustomizer adapts clauses to jurisdiction and industry."""

from __future__ import annotations

from docdraft.models import Clause, Document, Industry, Jurisdiction


# Jurisdiction-specific governing law text
_JURISDICTION_LAW: dict[Jurisdiction, str] = {
    Jurisdiction.US_CALIFORNIA: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of the State of California, without regard to its conflict of laws "
        "principles. Any dispute arising out of or in connection with this Agreement "
        "shall be subject to the exclusive jurisdiction of the state and federal "
        "courts located in the County of San Francisco, California."
    ),
    Jurisdiction.US_NEW_YORK: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of the State of New York, without regard to its conflict of laws "
        "principles. Any dispute arising out of or in connection with this Agreement "
        "shall be subject to the exclusive jurisdiction of the state and federal "
        "courts located in the Borough of Manhattan, New York City, New York."
    ),
    Jurisdiction.US_DELAWARE: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of the State of Delaware, without regard to its conflict of laws "
        "principles. Any dispute arising out of or in connection with this Agreement "
        "shall be subject to the exclusive jurisdiction of the Court of Chancery of "
        "the State of Delaware or the federal courts of the District of Delaware."
    ),
    Jurisdiction.US_TEXAS: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of the State of Texas, without regard to its conflict of laws "
        "principles. Any dispute arising out of or in connection with this Agreement "
        "shall be subject to the exclusive jurisdiction of the state and federal "
        "courts located in Travis County, Texas."
    ),
    Jurisdiction.UK: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of England and Wales. Any dispute arising out of or in connection with "
        "this Agreement shall be subject to the exclusive jurisdiction of the courts "
        "of England and Wales."
    ),
    Jurisdiction.EU: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of [MEMBER STATE]. Any dispute arising out of or in connection with "
        "this Agreement shall be resolved in accordance with the dispute resolution "
        "mechanisms provided under applicable European Union regulations."
    ),
    Jurisdiction.CANADA: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of the Province of [PROVINCE] and the federal laws of Canada applicable "
        "therein. Any dispute arising out of or in connection with this Agreement "
        "shall be subject to the exclusive jurisdiction of the courts of [PROVINCE]."
    ),
    Jurisdiction.AUSTRALIA: (
        "This Agreement shall be governed by and construed in accordance with the "
        "laws of the State of [STATE/TERRITORY], Australia. Any dispute arising out "
        "of or in connection with this Agreement shall be subject to the exclusive "
        "jurisdiction of the courts of [STATE/TERRITORY], Australia."
    ),
}

# California-specific non-compete note
_CALIFORNIA_NON_COMPETE_NOTE = (
    "CALIFORNIA NOTICE: Non-competition covenants are generally void and "
    "unenforceable in California pursuant to California Business and Professions "
    "Code Section 16600, with limited exceptions. This clause may not be "
    "enforceable for California-based employees."
)

# Industry-specific confidentiality additions
_INDUSTRY_CONFIDENTIALITY: dict[Industry, str] = {
    Industry.TECHNOLOGY: (
        "\n\nTechnology-Specific Provisions: Confidential Information expressly "
        "includes, without limitation, source code, object code, algorithms, APIs, "
        "system architecture, database schemas, encryption keys, security protocols, "
        "software development methodologies, deployment configurations, cloud "
        "infrastructure details, and any technical specifications or documentation "
        "related to the technology platform."
    ),
    Industry.HEALTHCARE: (
        "\n\nHealthcare-Specific Provisions: The Parties acknowledge that Confidential "
        "Information may include Protected Health Information (\"PHI\") as defined "
        "under the Health Insurance Portability and Accountability Act of 1996 "
        "(\"HIPAA\") and its implementing regulations. Each Party agrees to comply "
        "with all applicable requirements of HIPAA, the HITECH Act, and any "
        "applicable state health privacy laws with respect to any PHI received "
        "under this Agreement. A separate Business Associate Agreement may be "
        "required."
    ),
    Industry.FINANCE: (
        "\n\nFinancial Services-Specific Provisions: Confidential Information "
        "expressly includes, without limitation, financial models, trading "
        "strategies, portfolio data, risk assessments, client account information, "
        "transaction records, regulatory filings, compliance procedures, and any "
        "information subject to the Gramm-Leach-Bliley Act, Dodd-Frank Act, or "
        "applicable securities regulations. Each Party shall comply with all "
        "applicable financial services regulations regarding the handling and "
        "protection of such information."
    ),
}

# GDPR clause for EU jurisdiction
_GDPR_CLAUSE = Clause(
    id="gdpr-compliance",
    title="GDPR Compliance",
    section_number=None,
    body=(
        "Data Protection Addendum: The Parties acknowledge that the processing of "
        "personal data under this Agreement may be subject to Regulation (EU) "
        "2016/679 (the \"General Data Protection Regulation\" or \"GDPR\"). Each "
        "Party shall: (a) process personal data only in accordance with documented "
        "instructions; (b) ensure that persons authorized to process personal data "
        "have committed to confidentiality; (c) implement appropriate technical and "
        "organizational measures to ensure a level of security appropriate to the "
        "risk; (d) assist in responding to data subject requests; (e) notify the "
        "other Party without undue delay after becoming aware of a personal data "
        "breach; and (f) delete or return all personal data upon termination of "
        "this Agreement. The Parties agree to enter into a separate Data Processing "
        "Agreement if required under applicable law."
    ),
    is_optional=False,
    jurisdiction_notes="Required for agreements involving EU personal data.",
)


class ClauseCustomizer:
    """Adapts document clauses based on jurisdiction and industry context."""

    def customize(
        self,
        document: Document,
        jurisdiction: Jurisdiction,
        industry: Industry,
    ) -> Document:
        """Apply jurisdiction and industry customizations to a document."""
        self._apply_jurisdiction(document, jurisdiction)
        self._apply_industry(document, industry)
        self._renumber_clauses(document)
        return document

    def _apply_jurisdiction(self, document: Document, jurisdiction: Jurisdiction) -> None:
        """Update governing law clauses and add jurisdiction-specific provisions."""
        governing_law_text = _JURISDICTION_LAW.get(jurisdiction)

        for clause in document.clauses:
            # Update governing law clauses
            if "governing law" in clause.title.lower() and governing_law_text:
                clause.body = governing_law_text

            # Handle California non-compete restrictions
            if jurisdiction == Jurisdiction.US_CALIFORNIA:
                if "non-compet" in clause.title.lower() or "non-competition" in clause.title.lower():
                    clause.jurisdiction_notes = _CALIFORNIA_NON_COMPETE_NOTE
                    clause.body += (
                        "\n\nNOTE: " + _CALIFORNIA_NON_COMPETE_NOTE
                    )

        # Add GDPR clause for EU jurisdiction
        if jurisdiction == Jurisdiction.EU:
            has_gdpr = any(c.id == "gdpr-compliance" for c in document.clauses)
            if not has_gdpr:
                document.add_clause(_GDPR_CLAUSE)

    def _apply_industry(self, document: Document, industry: Industry) -> None:
        """Add industry-specific language to relevant clauses."""
        addition = _INDUSTRY_CONFIDENTIALITY.get(industry)
        if not addition:
            return

        for clause in document.clauses:
            if "confidential" in clause.title.lower():
                clause.body += addition
                break

    def _renumber_clauses(self, document: Document) -> None:
        """Ensure clause section numbers are sequential."""
        for i, clause in enumerate(document.clauses):
            if clause.section_number is not None:
                clause.section_number = str(i + 1)
