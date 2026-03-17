"""Service Agreement template."""

from __future__ import annotations

from docdraft.models import Clause, Document, DocumentType, Party, Term


class ServiceAgreementTemplate:
    """Generates service agreement documents."""

    name = "Service Agreement"
    document_type = DocumentType.SERVICE
    description = "Defines terms for provision of professional services."

    def generate(
        self,
        provider: Party,
        client: Party,
        services_description: str = "[DESCRIPTION OF SERVICES]",
        fee: str = "[FEE AMOUNT]",
        term: Term | None = None,
        **kwargs,
    ) -> Document:
        if term is None:
            term = Term(duration_months=12, auto_renewal=True, renewal_period_months=12)

        preamble = (
            f'This Service Agreement ("Agreement") is entered into as of the date last '
            f"signed below (the \"Effective Date\"), by and between "
            f'{provider.name} (the "Service Provider"), with its principal place of '
            f"business at {provider.address}, and "
            f'{client.name} (the "Client"), with its principal place of business at '
            f"{client.address}.\n\n"
            f"WHEREAS, the Service Provider is in the business of providing professional "
            f"services and possesses the skills, qualifications, and experience necessary "
            f"to perform the services described herein; and\n\n"
            f"WHEREAS, the Client desires to engage the Service Provider to perform such "
            f"services upon the terms and conditions set forth herein;\n\n"
            f"NOW, THEREFORE, in consideration of the mutual covenants and agreements "
            f"herein contained, and for other good and valuable consideration, the receipt "
            f"and sufficiency of which are hereby acknowledged, the Parties agree as follows:"
        )

        doc = Document(
            title="SERVICE AGREEMENT",
            document_type=DocumentType.SERVICE,
            parties=[provider, client],
            term=term,
            preamble=preamble,
            metadata={"services": services_description, "fee": fee},
        )

        for clause in self._build_clauses(provider, client, services_description, fee):
            doc.add_clause(clause)

        doc.signature_block = self._signature_block(provider, client)
        return doc

    def _build_clauses(
        self, provider: Party, client: Party, services: str, fee: str
    ) -> list[Clause]:
        return [
            Clause(
                id="svc-scope",
                title="Scope of Services",
                section_number="1",
                body=(
                    f"1.1 The Service Provider agrees to provide the following services to "
                    f'the Client (the "Services"): {services}\n\n'
                    f"1.2 The Service Provider shall perform the Services in a professional "
                    f"and workmanlike manner, consistent with industry standards and practices, "
                    f"and in compliance with all applicable laws and regulations.\n\n"
                    f"1.3 The specific deliverables, milestones, and timelines for the Services "
                    f"shall be as set forth in one or more Statements of Work (\"SOW\") to be "
                    f"mutually agreed upon by the Parties and attached hereto as exhibits. Each "
                    f"SOW shall be deemed incorporated into and made a part of this Agreement.\n\n"
                    f"1.4 Any changes to the scope of Services shall be documented in a written "
                    f"change order signed by both Parties, specifying the modified scope, "
                    f"additional fees, and revised timeline."
                ),
            ),
            Clause(
                id="svc-compensation",
                title="Compensation and Payment",
                section_number="2",
                body=(
                    f"2.1 In consideration for the Services, the Client shall pay the Service "
                    f"Provider {fee} (the \"Fee\"), payable in accordance with the payment "
                    f"schedule set forth in the applicable SOW.\n\n"
                    f"2.2 The Service Provider shall submit invoices to the Client on a monthly "
                    f"basis, or as otherwise specified in the applicable SOW. All invoices shall "
                    f"be payable within thirty (30) days of receipt.\n\n"
                    f"2.3 Late payments shall bear interest at the rate of one and one-half "
                    f"percent (1.5%) per month, or the maximum rate permitted by applicable law, "
                    f"whichever is less.\n\n"
                    f"2.4 The Client shall reimburse the Service Provider for all reasonable, "
                    f"pre-approved, out-of-pocket expenses incurred in connection with the "
                    f"performance of the Services, upon presentation of appropriate documentation."
                ),
            ),
            Clause(
                id="svc-term",
                title="Term and Termination",
                section_number="3",
                body=(
                    "3.1 This Agreement shall commence on the Effective Date and shall "
                    "continue for a period of twelve (12) months (the \"Initial Term\"), "
                    "unless earlier terminated in accordance with this Section.\n\n"
                    "3.2 Upon expiration of the Initial Term, this Agreement shall automatically "
                    "renew for successive twelve (12) month periods (each a \"Renewal Term\"), "
                    "unless either Party provides written notice of non-renewal at least thirty "
                    "(30) days prior to the expiration of the then-current term.\n\n"
                    "3.3 Either Party may terminate this Agreement for Cause upon written notice "
                    "if the other Party materially breaches any provision of this Agreement and "
                    "fails to cure such breach within thirty (30) days after receipt of written "
                    "notice specifying the breach.\n\n"
                    "3.4 Either Party may terminate this Agreement without Cause upon sixty (60) "
                    "days' prior written notice to the other Party.\n\n"
                    "3.5 Upon termination, the Client shall pay the Service Provider for all "
                    "Services performed and expenses incurred through the effective date of "
                    "termination."
                ),
            ),
            Clause(
                id="svc-ip",
                title="Intellectual Property",
                section_number="4",
                body=(
                    "4.1 Work Product. All deliverables, work product, and materials created "
                    "by the Service Provider specifically for the Client under this Agreement "
                    '(collectively, "Work Product") shall be the sole and exclusive property '
                    "of the Client upon full payment therefor. The Service Provider hereby "
                    "assigns to the Client all right, title, and interest in and to the Work "
                    "Product, including all intellectual property rights therein.\n\n"
                    "4.2 Pre-Existing Materials. The Service Provider retains all right, title, "
                    "and interest in and to any tools, methodologies, processes, software, "
                    "know-how, or other materials owned or developed by the Service Provider "
                    "prior to or independently of this Agreement (\"Pre-Existing Materials\"). "
                    "To the extent any Pre-Existing Materials are incorporated into the Work "
                    "Product, the Service Provider grants the Client a non-exclusive, perpetual, "
                    "irrevocable, royalty-free license to use such Pre-Existing Materials as "
                    "part of the Work Product.\n\n"
                    "4.3 Client Materials. The Client retains all right, title, and interest "
                    "in and to any materials provided by the Client to the Service Provider "
                    "for use in performing the Services."
                ),
            ),
            Clause(
                id="svc-confidentiality",
                title="Confidentiality",
                section_number="5",
                body=(
                    "5.1 Each Party acknowledges that in the course of performing this "
                    "Agreement, it may receive or have access to confidential and proprietary "
                    "information of the other Party (\"Confidential Information\"). Each Party "
                    "agrees to: (a) hold all Confidential Information in strict confidence; "
                    "(b) not disclose Confidential Information to any third party without the "
                    "prior written consent of the disclosing Party; and (c) use Confidential "
                    "Information solely for the purpose of performing its obligations under "
                    "this Agreement.\n\n"
                    "5.2 The obligations of confidentiality shall not apply to information "
                    "that: (a) is publicly available through no fault of the receiving Party; "
                    "(b) was known to the receiving Party prior to disclosure; (c) is "
                    "independently developed by the receiving Party; or (d) is required to be "
                    "disclosed by law or regulation.\n\n"
                    "5.3 The obligations of confidentiality shall survive the termination of "
                    "this Agreement for a period of three (3) years."
                ),
            ),
            Clause(
                id="svc-warranties",
                title="Representations and Warranties",
                section_number="6",
                body=(
                    "6.1 The Service Provider represents and warrants that: (a) it has the "
                    "right, power, and authority to enter into this Agreement and perform its "
                    "obligations hereunder; (b) the Services shall be performed in a "
                    "professional and workmanlike manner consistent with generally accepted "
                    "industry standards; (c) the Work Product shall not infringe upon the "
                    "intellectual property rights of any third party; and (d) it shall comply "
                    "with all applicable laws and regulations in performing the Services.\n\n"
                    "6.2 EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, THE SERVICE PROVIDER "
                    "MAKES NO OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION "
                    "ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE."
                ),
            ),
            Clause(
                id="svc-liability",
                title="Limitation of Liability",
                section_number="7",
                body=(
                    "7.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER PARTY FOR ANY "
                    "INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, PUNITIVE, OR EXEMPLARY "
                    "DAMAGES, INCLUDING BUT NOT LIMITED TO DAMAGES FOR LOSS OF PROFITS, "
                    "GOODWILL, USE, DATA, OR OTHER INTANGIBLE LOSSES, ARISING OUT OF OR IN "
                    "CONNECTION WITH THIS AGREEMENT, REGARDLESS OF THE THEORY OF LIABILITY.\n\n"
                    "7.2 THE TOTAL AGGREGATE LIABILITY OF THE SERVICE PROVIDER UNDER THIS "
                    "AGREEMENT SHALL NOT EXCEED THE TOTAL FEES PAID OR PAYABLE BY THE CLIENT "
                    "TO THE SERVICE PROVIDER DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY "
                    "PRECEDING THE EVENT GIVING RISE TO THE CLAIM.\n\n"
                    "7.3 The foregoing limitations shall not apply to: (a) breaches of "
                    "confidentiality obligations; (b) indemnification obligations; or "
                    "(c) willful misconduct or gross negligence."
                ),
            ),
            Clause(
                id="svc-indemnification",
                title="Indemnification",
                section_number="8",
                body=(
                    "8.1 The Service Provider shall indemnify, defend, and hold harmless the "
                    "Client and its officers, directors, employees, and agents from and against "
                    "any and all claims, damages, losses, liabilities, costs, and expenses "
                    "(including reasonable attorneys' fees) arising out of or in connection "
                    "with: (a) any breach of this Agreement by the Service Provider; (b) the "
                    "negligence or willful misconduct of the Service Provider; or (c) any claim "
                    "that the Work Product infringes upon the intellectual property rights of "
                    "any third party.\n\n"
                    "8.2 The Client shall indemnify, defend, and hold harmless the Service "
                    "Provider from and against any claims arising out of: (a) any breach of "
                    "this Agreement by the Client; (b) the Client's use of the Work Product "
                    "in a manner not contemplated by this Agreement; or (c) materials provided "
                    "by the Client."
                ),
            ),
            Clause(
                id="svc-governing-law",
                title="Governing Law",
                section_number="9",
                body=(
                    "This Agreement shall be governed by and construed in accordance with the "
                    "laws of the State of [STATE], without regard to its conflict of laws "
                    "principles. Any dispute arising under this Agreement shall be resolved "
                    "through binding arbitration conducted in [CITY, STATE] in accordance "
                    "with the rules of the American Arbitration Association."
                ),
            ),
            Clause(
                id="svc-miscellaneous",
                title="General Provisions",
                section_number="10",
                body=(
                    "10.1 Independent Contractor. The Service Provider is an independent "
                    "contractor and nothing in this Agreement shall be construed to create "
                    "an employment, agency, joint venture, or partnership relationship.\n\n"
                    "10.2 Entire Agreement. This Agreement, together with all SOWs and "
                    "exhibits, constitutes the entire agreement between the Parties.\n\n"
                    "10.3 Amendment. This Agreement may be amended only by a written "
                    "instrument signed by both Parties.\n\n"
                    "10.4 Assignment. Neither Party may assign this Agreement without the "
                    "prior written consent of the other Party.\n\n"
                    "10.5 Force Majeure. Neither Party shall be liable for any failure or "
                    "delay in performance due to causes beyond its reasonable control, "
                    "including acts of God, war, terrorism, natural disasters, or government "
                    "actions.\n\n"
                    "10.6 Severability. If any provision of this Agreement is held invalid "
                    "or unenforceable, the remaining provisions shall continue in full force "
                    "and effect."
                ),
            ),
        ]

    def _signature_block(self, provider: Party, client: Party) -> str:
        return (
            f"IN WITNESS WHEREOF, the Parties have executed this Service Agreement "
            f"as of the Effective Date.\n\n"
            f"SERVICE PROVIDER: {provider.name}\n\n"
            f"Signature: ___________________________\n"
            f"Name: {provider.representative or '[AUTHORIZED REPRESENTATIVE]'}\n"
            f"Title: {provider.title or '[TITLE]'}\n"
            f"Date: ___________________________\n\n"
            f"CLIENT: {client.name}\n\n"
            f"Signature: ___________________________\n"
            f"Name: {client.representative or '[AUTHORIZED REPRESENTATIVE]'}\n"
            f"Title: {client.title or '[TITLE]'}\n"
            f"Date: ___________________________"
        )
