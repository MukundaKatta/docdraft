"""Freelance Contract template."""

from __future__ import annotations

from docdraft.models import Clause, Document, DocumentType, Party, Term


class FreelanceContractTemplate:
    """Generates freelance/independent contractor agreement documents."""

    name = "Freelance Contract"
    document_type = DocumentType.FREELANCE
    description = "Defines terms for freelance/independent contractor engagements."

    def generate(
        self,
        freelancer: Party,
        client: Party,
        project_description: str = "[PROJECT DESCRIPTION]",
        rate: str = "[RATE]",
        term: Term | None = None,
        **kwargs,
    ) -> Document:
        if term is None:
            term = Term(duration_months=3, notice_period_days=14)

        preamble = (
            f'This Independent Contractor Agreement ("Agreement") is entered into as of '
            f"the date last signed below (the \"Effective Date\"), by and between "
            f'{client.name} (the "Client"), with its principal place of business at '
            f'{client.address}, and {freelancer.name} (the "Contractor"), '
            f"residing at {freelancer.address}.\n\n"
            f"WHEREAS, the Client desires to engage the Contractor to perform certain "
            f"services as described herein, and the Contractor desires to perform such "
            f"services, upon the terms and conditions set forth in this Agreement;\n\n"
            f"NOW, THEREFORE, in consideration of the mutual promises and covenants "
            f"contained herein, the Parties agree as follows:"
        )

        doc = Document(
            title="INDEPENDENT CONTRACTOR AGREEMENT",
            document_type=DocumentType.FREELANCE,
            parties=[freelancer, client],
            term=term,
            preamble=preamble,
            metadata={"project": project_description, "rate": rate},
        )

        for clause in self._build_clauses(freelancer, client, project_description, rate):
            doc.add_clause(clause)

        doc.signature_block = self._signature_block(freelancer, client)
        return doc

    def _build_clauses(
        self, freelancer: Party, client: Party, project: str, rate: str
    ) -> list[Clause]:
        return [
            Clause(
                id="free-services",
                title="Services",
                section_number="1",
                body=(
                    f"1.1 The Contractor agrees to perform the following services for the "
                    f'Client (the "Services"): {project}\n\n'
                    f"1.2 The Contractor shall perform the Services in accordance with the "
                    f"specifications, standards, and deadlines set forth in the project brief "
                    f"or statement of work attached as Exhibit A.\n\n"
                    f"1.3 The Contractor shall provide all equipment, tools, and materials "
                    f"necessary to perform the Services, unless otherwise agreed in writing."
                ),
            ),
            Clause(
                id="free-relationship",
                title="Independent Contractor Relationship",
                section_number="2",
                body=(
                    "2.1 The Contractor is an independent contractor and not an employee, "
                    "agent, partner, or joint venturer of the Client. Nothing in this "
                    "Agreement shall be interpreted or construed as creating or establishing "
                    "an employment relationship between the Client and the Contractor.\n\n"
                    "2.2 The Contractor shall have no authority to bind the Client or to "
                    "make any representation or warranty on behalf of the Client.\n\n"
                    "2.3 The Contractor shall be solely responsible for the payment of all "
                    "federal, state, and local income taxes, self-employment taxes, and any "
                    "other taxes arising from the compensation paid under this Agreement. "
                    "The Client shall not withhold any taxes from payments to the Contractor.\n\n"
                    "2.4 The Contractor acknowledges that they are not eligible for any "
                    "employee benefits from the Client, including but not limited to health "
                    "insurance, retirement plans, paid time off, or workers' compensation "
                    "coverage.\n\n"
                    "2.5 The Contractor retains the right to determine the method, manner, "
                    "and means of performing the Services. The Client may provide general "
                    "direction regarding the desired results but shall not control the "
                    "details of the Contractor's work."
                ),
            ),
            Clause(
                id="free-compensation",
                title="Compensation",
                section_number="3",
                body=(
                    f"3.1 The Client shall pay the Contractor {rate} for the Services "
                    f"rendered under this Agreement.\n\n"
                    f"3.2 The Contractor shall submit invoices to the Client on a bi-weekly "
                    f"basis, detailing the Services performed and hours worked (if applicable). "
                    f"All invoices shall be payable within fifteen (15) days of receipt.\n\n"
                    f"3.3 In the event of a dispute regarding an invoice, the Client shall pay "
                    f"the undisputed portion and promptly notify the Contractor in writing of "
                    f"the disputed amount with a detailed explanation.\n\n"
                    f"3.4 Late payments shall accrue interest at the rate of one and one-half "
                    f"percent (1.5%) per month or the maximum rate permitted by law, whichever "
                    f"is less."
                ),
            ),
            Clause(
                id="free-ip",
                title="Intellectual Property",
                section_number="4",
                body=(
                    "4.1 Work Product Assignment. Upon full payment, the Contractor assigns "
                    "to the Client all right, title, and interest in and to all deliverables "
                    "and work product created by the Contractor specifically for the Client "
                    'under this Agreement ("Work Product"), including all intellectual property '
                    "rights therein.\n\n"
                    "4.2 Contractor Tools. The Contractor retains ownership of all pre-existing "
                    "tools, libraries, frameworks, methodologies, and other materials owned or "
                    "developed by the Contractor independently of this Agreement (\"Contractor "
                    "Tools\"). To the extent any Contractor Tools are incorporated into the "
                    "Work Product, the Contractor grants the Client a non-exclusive, perpetual, "
                    "royalty-free, worldwide license to use, modify, and distribute such "
                    "Contractor Tools solely as part of the Work Product.\n\n"
                    "4.3 Portfolio Rights. The Contractor retains the right to display the "
                    "Work Product as part of the Contractor's portfolio, unless the Client "
                    "provides written notice restricting such use."
                ),
            ),
            Clause(
                id="free-confidentiality",
                title="Confidentiality",
                section_number="5",
                body=(
                    "5.1 The Contractor agrees to hold in confidence all information "
                    "designated as confidential by the Client or that reasonably should be "
                    "understood to be confidential given the nature of the information "
                    "(\"Confidential Information\"). The Contractor shall not disclose "
                    "Confidential Information to any third party or use it for any purpose "
                    "other than performing the Services.\n\n"
                    "5.2 Confidential Information does not include information that: "
                    "(a) is publicly known through no breach of this Agreement; "
                    "(b) was in the Contractor's possession before disclosure; "
                    "(c) is independently developed by the Contractor; or "
                    "(d) is disclosed pursuant to legal requirement.\n\n"
                    "5.3 The obligations under this Section shall survive termination of "
                    "this Agreement for a period of two (2) years."
                ),
            ),
            Clause(
                id="free-term",
                title="Term and Termination",
                section_number="6",
                body=(
                    "6.1 This Agreement shall commence on the Effective Date and shall "
                    "continue until the Services are completed, or for a period of three (3) "
                    "months, whichever is earlier, unless terminated earlier pursuant to this "
                    "Section.\n\n"
                    "6.2 Either Party may terminate this Agreement for any reason upon "
                    "fourteen (14) days' prior written notice to the other Party.\n\n"
                    "6.3 Either Party may terminate this Agreement immediately upon written "
                    "notice if the other Party materially breaches this Agreement and fails "
                    "to cure such breach within seven (7) days after receipt of written notice.\n\n"
                    "6.4 Upon termination: (a) the Client shall pay the Contractor for all "
                    "Services satisfactorily performed through the date of termination; "
                    "(b) the Contractor shall deliver to the Client all completed and "
                    "in-progress Work Product; and (c) each Party shall return or destroy "
                    "the other Party's Confidential Information."
                ),
            ),
            Clause(
                id="free-warranties",
                title="Representations and Warranties",
                section_number="7",
                body=(
                    "7.1 The Contractor represents and warrants that: (a) the Contractor "
                    "has the skills, qualifications, and experience necessary to perform the "
                    "Services; (b) the Services will be performed in a professional and "
                    "workmanlike manner; (c) the Work Product will be original and will not "
                    "infringe upon the intellectual property rights of any third party; and "
                    "(d) the Contractor has the right to enter into this Agreement.\n\n"
                    "7.2 The Contractor shall, at the Contractor's expense, re-perform any "
                    "Services that fail to conform to the foregoing warranties, provided that "
                    "the Client notifies the Contractor of such nonconformity within thirty "
                    "(30) days of delivery."
                ),
            ),
            Clause(
                id="free-liability",
                title="Limitation of Liability",
                section_number="8",
                body=(
                    "8.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, "
                    "INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THIS "
                    "AGREEMENT.\n\n"
                    "8.2 THE CONTRACTOR'S TOTAL LIABILITY UNDER THIS AGREEMENT SHALL NOT "
                    "EXCEED THE TOTAL COMPENSATION PAID OR PAYABLE TO THE CONTRACTOR UNDER "
                    "THIS AGREEMENT."
                ),
            ),
            Clause(
                id="free-miscellaneous",
                title="General Provisions",
                section_number="9",
                body=(
                    "9.1 Entire Agreement. This Agreement constitutes the entire agreement "
                    "between the Parties and supersedes all prior agreements.\n\n"
                    "9.2 Amendment. This Agreement may only be amended by written instrument "
                    "signed by both Parties.\n\n"
                    "9.3 Governing Law. This Agreement shall be governed by the laws of the "
                    "State of [STATE], without regard to conflict of laws principles.\n\n"
                    "9.4 Severability. If any provision is found unenforceable, the remaining "
                    "provisions shall remain in effect.\n\n"
                    "9.5 Notices. All notices shall be in writing and sent to the addresses "
                    "set forth above.\n\n"
                    "9.6 Waiver. No waiver of any provision shall be effective unless in "
                    "writing.\n\n"
                    "9.7 Counterparts. This Agreement may be executed in counterparts, each "
                    "of which shall be deemed an original."
                ),
            ),
        ]

    def _signature_block(self, freelancer: Party, client: Party) -> str:
        return (
            f"IN WITNESS WHEREOF, the Parties have executed this Independent Contractor "
            f"Agreement as of the Effective Date.\n\n"
            f"CLIENT: {client.name}\n\n"
            f"Signature: ___________________________\n"
            f"Name: {client.representative or '[AUTHORIZED REPRESENTATIVE]'}\n"
            f"Title: {client.title or '[TITLE]'}\n"
            f"Date: ___________________________\n\n"
            f"CONTRACTOR: {freelancer.name}\n\n"
            f"Signature: ___________________________\n"
            f"Date: ___________________________"
        )
