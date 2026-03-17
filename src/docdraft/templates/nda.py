"""Non-Disclosure Agreement (NDA) template with mutual and unilateral variants."""

from __future__ import annotations

from docdraft.models import Clause, Document, DocumentType, NDAVariant, Party, Term


class NDATemplate:
    """Generates NDA documents with mutual or unilateral variants."""

    name = "Non-Disclosure Agreement"
    document_type = DocumentType.NDA
    description = "Protects confidential information shared between parties."

    def generate(
        self,
        disclosing_party: Party,
        receiving_party: Party,
        variant: NDAVariant = NDAVariant.MUTUAL,
        term: Term | None = None,
        **kwargs,
    ) -> Document:
        if term is None:
            term = Term(duration_months=24, notice_period_days=30)

        if variant == NDAVariant.MUTUAL:
            title = "MUTUAL NON-DISCLOSURE AGREEMENT"
            preamble = self._mutual_preamble(disclosing_party, receiving_party)
        else:
            title = "UNILATERAL NON-DISCLOSURE AGREEMENT"
            preamble = self._unilateral_preamble(disclosing_party, receiving_party)

        doc = Document(
            title=title,
            document_type=DocumentType.NDA,
            parties=[disclosing_party, receiving_party],
            term=term,
            preamble=preamble,
            metadata={"variant": variant.value},
        )

        clauses = self._build_clauses(disclosing_party, receiving_party, variant)
        for clause in clauses:
            doc.add_clause(clause)

        doc.signature_block = self._signature_block(disclosing_party, receiving_party)
        return doc

    def _mutual_preamble(self, party1: Party, party2: Party) -> str:
        return (
            f'This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of '
            f"the date last signed below (the \"Effective Date\"), by and between "
            f'{party1.name} ("{self._short_name(party1)}") and '
            f'{party2.name} ("{self._short_name(party2)}"), '
            f"each individually a \"Party\" and collectively the \"Parties.\"\n\n"
            f"WHEREAS, the Parties wish to explore a potential business relationship "
            f"(the \"Purpose\") and, in connection therewith, each Party may disclose "
            f"certain Confidential Information (as defined below) to the other Party; and\n\n"
            f"WHEREAS, the Parties desire to protect the confidentiality of such "
            f"information and to restrict its use and disclosure;\n\n"
            f"NOW, THEREFORE, in consideration of the mutual covenants and agreements "
            f"set forth herein, and for other good and valuable consideration, the receipt "
            f"and sufficiency of which are hereby acknowledged, the Parties agree as follows:"
        )

    def _unilateral_preamble(self, disclosing: Party, receiving: Party) -> str:
        return (
            f'This Non-Disclosure Agreement ("Agreement") is entered into as of the date '
            f"last signed below (the \"Effective Date\"), by and between "
            f'{disclosing.name} (the "Disclosing Party") and '
            f'{receiving.name} (the "Receiving Party").\n\n'
            f"WHEREAS, the Disclosing Party possesses certain confidential and proprietary "
            f"information relating to its business, products, services, technical data, "
            f"trade secrets, and other proprietary information; and\n\n"
            f"WHEREAS, the Receiving Party desires to receive certain Confidential "
            f"Information for the purpose of evaluating a potential business relationship "
            f"(the \"Purpose\");\n\n"
            f"NOW, THEREFORE, in consideration of the mutual covenants contained herein "
            f"and other good and valuable consideration, the receipt and sufficiency of "
            f"which are hereby acknowledged, the Parties agree as follows:"
        )

    def _build_clauses(
        self, party1: Party, party2: Party, variant: NDAVariant
    ) -> list[Clause]:
        clauses = []

        if variant == NDAVariant.MUTUAL:
            conf_body = (
                '"Confidential Information" means any and all non-public, proprietary, '
                "or confidential information disclosed by either Party to the other Party, "
                "whether orally, in writing, electronically, or by any other means, including "
                "but not limited to: (a) trade secrets, inventions, ideas, processes, formulas, "
                "source and object codes, data, programs, software, other works of authorship, "
                "know-how, improvements, discoveries, developments, designs, and techniques; "
                "(b) information regarding plans for research, development, new products, "
                "marketing and selling, business plans, budgets and unpublished financial "
                "statements, licenses, prices and costs, suppliers, and customers; "
                "(c) information regarding the skills and compensation of employees, "
                "contractors, and any other service providers of the Disclosing Party; and "
                "(d) any other information that a reasonable person would understand to be "
                "confidential given the nature of the information and the circumstances of "
                "disclosure. Confidential Information includes all notes, analyses, compilations, "
                "studies, summaries, and other material prepared by the Receiving Party containing "
                "or based, in whole or in part, upon any information furnished by the Disclosing "
                "Party."
            )
        else:
            conf_body = (
                '"Confidential Information" means any and all non-public, proprietary, '
                "or confidential information disclosed by the Disclosing Party to the "
                "Receiving Party, whether orally, in writing, electronically, or by any "
                "other means, including but not limited to: (a) trade secrets, inventions, "
                "ideas, processes, formulas, source and object codes, data, programs, "
                "software, other works of authorship, know-how, improvements, discoveries, "
                "developments, designs, and techniques; (b) information regarding plans for "
                "research, development, new products, marketing and selling, business plans, "
                "budgets and unpublished financial statements, licenses, prices and costs, "
                "suppliers, and customers; (c) information regarding the skills and "
                "compensation of employees, contractors, and any other service providers; "
                "and (d) any other information that a reasonable person would understand to "
                "be confidential given the nature of the information and the circumstances "
                "of disclosure."
            )

        clauses.append(
            Clause(
                id="nda-definition",
                title="Definition of Confidential Information",
                section_number="1",
                body=conf_body,
            )
        )

        clauses.append(
            Clause(
                id="nda-exclusions",
                title="Exclusions from Confidential Information",
                section_number="2",
                body=(
                    "Confidential Information shall not include information that: "
                    "(a) is or becomes publicly available through no fault of or action by "
                    "the Receiving Party; (b) was already in the Receiving Party's possession "
                    "prior to disclosure, as demonstrated by written records; "
                    "(c) is independently developed by the Receiving Party without use of or "
                    "reference to the Disclosing Party's Confidential Information, as "
                    "demonstrated by written records; (d) is rightfully received by the "
                    "Receiving Party from a third party without restriction on disclosure and "
                    "without breach of any obligation of confidentiality; or (e) is required "
                    "to be disclosed by law, regulation, or court order, provided that the "
                    "Receiving Party gives the Disclosing Party prompt written notice of such "
                    "requirement prior to disclosure and cooperates with the Disclosing Party's "
                    "efforts to obtain a protective order or other appropriate remedy."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-obligations",
                title="Obligations of the Receiving Party",
                section_number="3",
                body=(
                    "The Receiving Party shall: (a) hold the Confidential Information in "
                    "strict confidence and take all reasonable precautions to protect such "
                    "Confidential Information, including, without limitation, all precautions "
                    "the Receiving Party employs with respect to its own confidential materials; "
                    "(b) not disclose any Confidential Information to any third parties without "
                    "the prior written consent of the Disclosing Party, except to those employees, "
                    "agents, or subcontractors of the Receiving Party who need to know such "
                    "information for the Purpose and who are bound by confidentiality obligations "
                    "no less restrictive than those contained herein; (c) not use any Confidential "
                    "Information for any purpose other than the Purpose; and (d) promptly notify "
                    "the Disclosing Party in writing of any unauthorized use or disclosure of "
                    "Confidential Information."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-return",
                title="Return of Materials",
                section_number="4",
                body=(
                    "Upon the termination or expiration of this Agreement, or upon the written "
                    "request of the Disclosing Party at any time, the Receiving Party shall "
                    "promptly return or destroy all copies, whether in written, electronic, or "
                    "other form, of the Confidential Information in its possession or control, "
                    "and shall certify in writing to the Disclosing Party that it has complied "
                    "with this requirement. Notwithstanding the foregoing, the Receiving Party "
                    "may retain one (1) archival copy of the Confidential Information solely "
                    "for the purpose of ensuring compliance with the terms of this Agreement, "
                    "provided that such copy remains subject to the confidentiality obligations "
                    "set forth herein."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-no-rights",
                title="No Grant of Rights",
                section_number="5",
                body=(
                    "Nothing in this Agreement shall be construed as granting any rights, by "
                    "license or otherwise, to the Receiving Party in or to any Confidential "
                    "Information, except the limited right to use such Confidential Information "
                    "for the Purpose as expressly set forth herein. The Disclosing Party retains "
                    "all right, title, and interest in and to its Confidential Information, "
                    "including without limitation all intellectual property rights therein."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-term",
                title="Term and Termination",
                section_number="6",
                body=(
                    "This Agreement shall remain in effect for a period of two (2) years from "
                    "the Effective Date, unless earlier terminated by either Party upon thirty "
                    "(30) days' prior written notice to the other Party. The obligations of "
                    "confidentiality set forth herein shall survive the termination or expiration "
                    "of this Agreement for a period of three (3) years following such termination "
                    "or expiration."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-remedies",
                title="Remedies",
                section_number="7",
                body=(
                    "The Receiving Party acknowledges and agrees that any breach or threatened "
                    "breach of this Agreement may cause irreparable harm to the Disclosing Party "
                    "for which monetary damages may be inadequate. Accordingly, the Disclosing "
                    "Party shall be entitled to seek equitable relief, including injunction and "
                    "specific performance, in addition to all other remedies available at law or "
                    "in equity, without the necessity of proving actual damages or posting any "
                    "bond or other security."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-miscellaneous",
                title="Miscellaneous",
                section_number="8",
                body=(
                    "(a) Entire Agreement. This Agreement constitutes the entire agreement between "
                    "the Parties with respect to the subject matter hereof and supersedes all prior "
                    "and contemporaneous agreements, understandings, negotiations, and discussions, "
                    "whether oral or written. (b) Amendment. This Agreement may not be amended or "
                    "modified except by a written instrument signed by both Parties. "
                    "(c) Waiver. No waiver of any provision of this Agreement shall be effective "
                    "unless in writing and signed by the Party granting the waiver. "
                    "(d) Severability. If any provision of this Agreement is found to be "
                    "unenforceable, the remaining provisions shall continue in full force and effect. "
                    "(e) Assignment. Neither Party may assign this Agreement without the prior "
                    "written consent of the other Party. (f) Counterparts. This Agreement may be "
                    "executed in counterparts, each of which shall be deemed an original."
                ),
            )
        )

        clauses.append(
            Clause(
                id="nda-governing-law",
                title="Governing Law",
                section_number="9",
                body=(
                    "This Agreement shall be governed by and construed in accordance with the "
                    "laws of the State of [STATE], without regard to its conflict of laws "
                    "principles. Any dispute arising out of or in connection with this Agreement "
                    "shall be subject to the exclusive jurisdiction of the state and federal "
                    "courts located in [STATE]."
                ),
            )
        )

        return clauses

    def _signature_block(self, party1: Party, party2: Party) -> str:
        return (
            f"IN WITNESS WHEREOF, the Parties have executed this Agreement as of the "
            f"Effective Date.\n\n"
            f"{party1.name}\n\n"
            f"Signature: ___________________________\n"
            f"Name: {party1.representative or '[AUTHORIZED REPRESENTATIVE]'}\n"
            f"Title: {party1.title or '[TITLE]'}\n"
            f"Date: ___________________________\n\n"
            f"{party2.name}\n\n"
            f"Signature: ___________________________\n"
            f"Name: {party2.representative or '[AUTHORIZED REPRESENTATIVE]'}\n"
            f"Title: {party2.title or '[TITLE]'}\n"
            f"Date: ___________________________"
        )

    @staticmethod
    def _short_name(party: Party) -> str:
        parts = party.name.split()
        if len(parts) > 1:
            return parts[0]
        return party.name
