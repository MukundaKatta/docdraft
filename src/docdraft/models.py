"""Pydantic models for legal document structures."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported legal document types."""

    NDA = "nda"
    EMPLOYMENT = "employment"
    SERVICE = "service"
    FREELANCE = "freelance"
    PRIVACY = "privacy"
    TERMS = "terms"


class NDAVariant(str, Enum):
    """NDA sub-variants."""

    MUTUAL = "mutual"
    UNILATERAL = "unilateral"


class Jurisdiction(str, Enum):
    """Supported jurisdictions."""

    US_CALIFORNIA = "us-california"
    US_NEW_YORK = "us-new-york"
    US_DELAWARE = "us-delaware"
    US_TEXAS = "us-texas"
    US_GENERAL = "us-general"
    UK = "uk"
    EU = "eu"
    CANADA = "canada"
    AUSTRALIA = "australia"


class Industry(str, Enum):
    """Industry verticals for clause customization."""

    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    GENERAL = "general"


class OutputFormat(str, Enum):
    """Document output formats."""

    MARKDOWN = "markdown"
    PLAIN = "plain"


class Party(BaseModel):
    """Represents a party to a legal agreement."""

    name: str = Field(..., min_length=1, description="Legal name of the party")
    address: str = Field(default="[ADDRESS]", description="Mailing address")
    entity_type: str = Field(
        default="individual",
        description="Type of entity: individual, corporation, llc, partnership",
    )
    representative: Optional[str] = Field(
        default=None, description="Authorized representative name"
    )
    title: Optional[str] = Field(
        default=None, description="Title of the representative"
    )
    email: Optional[str] = Field(default=None, description="Contact email")
    state_of_incorporation: Optional[str] = Field(
        default=None, description="State/country of incorporation"
    )


class Term(BaseModel):
    """Represents the term/duration of an agreement."""

    start_date: date = Field(
        default_factory=date.today, description="Agreement start date"
    )
    end_date: Optional[date] = Field(
        default=None, description="Agreement end date, if fixed term"
    )
    duration_months: Optional[int] = Field(
        default=None, description="Duration in months"
    )
    auto_renewal: bool = Field(
        default=False, description="Whether the agreement auto-renews"
    )
    renewal_period_months: Optional[int] = Field(
        default=None, description="Auto-renewal period in months"
    )
    notice_period_days: int = Field(
        default=30, description="Notice period for termination in days"
    )

    @property
    def is_indefinite(self) -> bool:
        return self.end_date is None and self.duration_months is None


class Clause(BaseModel):
    """Represents a single clause in a legal document."""

    id: str = Field(..., description="Unique clause identifier")
    title: str = Field(..., description="Clause heading")
    body: str = Field(..., description="Full clause text")
    section_number: Optional[str] = Field(
        default=None, description="Section numbering"
    )
    is_optional: bool = Field(
        default=False, description="Whether this clause is optional"
    )
    jurisdiction_notes: Optional[str] = Field(
        default=None, description="Jurisdiction-specific notes"
    )


class Document(BaseModel):
    """Represents a complete legal document."""

    title: str = Field(..., description="Document title")
    document_type: DocumentType = Field(..., description="Type of legal document")
    parties: list[Party] = Field(default_factory=list, description="Parties involved")
    clauses: list[Clause] = Field(
        default_factory=list, description="Document clauses"
    )
    term: Optional[Term] = Field(default=None, description="Agreement term")
    jurisdiction: Jurisdiction = Field(
        default=Jurisdiction.US_GENERAL, description="Governing jurisdiction"
    )
    industry: Industry = Field(
        default=Industry.GENERAL, description="Industry context"
    )
    effective_date: date = Field(
        default_factory=date.today, description="Effective date"
    )
    preamble: str = Field(default="", description="Document preamble/recitals")
    signature_block: str = Field(default="", description="Signature block text")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    metadata: dict = Field(
        default_factory=dict, description="Additional metadata"
    )

    def add_clause(self, clause: Clause) -> None:
        self.clauses.append(clause)

    def get_clause(self, clause_id: str) -> Optional[Clause]:
        for clause in self.clauses:
            if clause.id == clause_id:
                return clause
        return None

    def remove_clause(self, clause_id: str) -> bool:
        for i, clause in enumerate(self.clauses):
            if clause.id == clause_id:
                self.clauses.pop(i)
                return True
        return False
