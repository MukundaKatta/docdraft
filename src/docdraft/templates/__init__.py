"""Legal document templates."""

from docdraft.templates.employment import EmploymentAgreementTemplate
from docdraft.templates.freelance import FreelanceContractTemplate
from docdraft.templates.nda import NDATemplate
from docdraft.templates.privacy import PrivacyPolicyTemplate
from docdraft.templates.service import ServiceAgreementTemplate
from docdraft.templates.terms import TermsOfServiceTemplate

TEMPLATE_REGISTRY: dict[str, type] = {
    "nda": NDATemplate,
    "employment": EmploymentAgreementTemplate,
    "service": ServiceAgreementTemplate,
    "freelance": FreelanceContractTemplate,
    "privacy": PrivacyPolicyTemplate,
    "terms": TermsOfServiceTemplate,
}

__all__ = [
    "NDATemplate",
    "EmploymentAgreementTemplate",
    "ServiceAgreementTemplate",
    "FreelanceContractTemplate",
    "PrivacyPolicyTemplate",
    "TermsOfServiceTemplate",
    "TEMPLATE_REGISTRY",
]
