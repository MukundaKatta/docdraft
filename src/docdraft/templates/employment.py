"""Employment Agreement template."""

from __future__ import annotations

from docdraft.models import Clause, Document, DocumentType, Party, Term


class EmploymentAgreementTemplate:
    """Generates employment agreement documents."""

    name = "Employment Agreement"
    document_type = DocumentType.EMPLOYMENT
    description = "Defines terms and conditions of employment between employer and employee."

    def generate(
        self,
        employer: Party,
        employee: Party,
        job_title: str = "[JOB TITLE]",
        salary: str = "[SALARY]",
        term: Term | None = None,
        **kwargs,
    ) -> Document:
        if term is None:
            term = Term(notice_period_days=14)

        preamble = (
            f'This Employment Agreement ("Agreement") is entered into as of the date '
            f"last signed below (the \"Effective Date\"), by and between "
            f'{employer.name} (the "Employer"), with its principal place of business at '
            f'{employer.address}, and {employee.name} (the "Employee"), residing at '
            f"{employee.address}.\n\n"
            f"WHEREAS, the Employer desires to employ the Employee, and the Employee "
            f"desires to accept such employment, upon the terms and conditions set forth "
            f"herein;\n\n"
            f"NOW, THEREFORE, in consideration of the mutual covenants and promises "
            f"contained herein, and for other good and valuable consideration, the receipt "
            f"and sufficiency of which are hereby acknowledged, the Parties agree as follows:"
        )

        doc = Document(
            title="EMPLOYMENT AGREEMENT",
            document_type=DocumentType.EMPLOYMENT,
            parties=[employer, employee],
            term=term,
            preamble=preamble,
            metadata={"job_title": job_title, "salary": salary},
        )

        for clause in self._build_clauses(employer, employee, job_title, salary):
            doc.add_clause(clause)

        doc.signature_block = self._signature_block(employer, employee)
        return doc

    def _build_clauses(
        self, employer: Party, employee: Party, job_title: str, salary: str
    ) -> list[Clause]:
        return [
            Clause(
                id="emp-position",
                title="Position and Duties",
                section_number="1",
                body=(
                    f'1.1 The Employer hereby employs the Employee as {job_title} ("Position"). '
                    f"The Employee shall perform all duties and responsibilities customarily "
                    f"associated with such Position, as well as such other duties as may be "
                    f"reasonably assigned by the Employer from time to time.\n\n"
                    f"1.2 The Employee shall devote their full business time, attention, skill, "
                    f"and best efforts to the performance of their duties hereunder and to the "
                    f"furtherance of the Employer's business interests. The Employee shall not, "
                    f"without the prior written consent of the Employer, engage in any other "
                    f"business activity, whether or not such activity is pursued for gain, "
                    f"profit, or other pecuniary advantage, that would interfere with the "
                    f"Employee's duties hereunder.\n\n"
                    f"1.3 The Employee shall report directly to [SUPERVISOR] or such other "
                    f"person as the Employer may designate from time to time."
                ),
            ),
            Clause(
                id="emp-compensation",
                title="Compensation and Benefits",
                section_number="2",
                body=(
                    f"2.1 Base Salary. The Employer shall pay the Employee a base salary of "
                    f"{salary} per annum (the \"Base Salary\"), payable in accordance with the "
                    f"Employer's standard payroll practices, less all applicable withholdings "
                    f"and deductions required by law.\n\n"
                    f"2.2 Benefits. The Employee shall be eligible to participate in all "
                    f"employee benefit plans and programs maintained by the Employer for its "
                    f"employees generally, including but not limited to health insurance, "
                    f"dental insurance, vision insurance, life insurance, disability insurance, "
                    f"and retirement plans, subject to the terms and eligibility requirements "
                    f"of such plans.\n\n"
                    f"2.3 Paid Time Off. The Employee shall be entitled to [NUMBER] days of "
                    f"paid time off per calendar year, to be taken at such times as are "
                    f"mutually agreeable to the Employee and the Employer, in accordance with "
                    f"the Employer's PTO policy.\n\n"
                    f"2.4 Bonus. The Employee may be eligible for an annual performance bonus "
                    f"at the sole discretion of the Employer, based upon the achievement of "
                    f"individual and company performance objectives."
                ),
            ),
            Clause(
                id="emp-at-will",
                title="At-Will Employment",
                section_number="3",
                body=(
                    "The Employee's employment with the Employer is \"at-will.\" This means "
                    "that either the Employee or the Employer may terminate the employment "
                    "relationship at any time, with or without cause, and with or without "
                    "notice, subject to the provisions of Section 7 of this Agreement. "
                    "Nothing in this Agreement shall be construed to create any right to "
                    "continued employment or to limit the Employer's right to terminate "
                    "the Employee's employment at any time."
                ),
            ),
            Clause(
                id="emp-confidentiality",
                title="Confidentiality",
                section_number="4",
                body=(
                    '4.1 "Confidential Information" means all information, whether written, '
                    "oral, electronic, or otherwise, that is proprietary to the Employer or "
                    "any of its affiliates, including but not limited to trade secrets, "
                    "technical data, business plans, financial information, customer lists, "
                    "marketing strategies, product development plans, personnel information, "
                    "and any other information designated as confidential or that reasonably "
                    "should be understood to be confidential.\n\n"
                    "4.2 The Employee agrees to hold all Confidential Information in strict "
                    "confidence and not to disclose, publish, or otherwise reveal any "
                    "Confidential Information to any third party during or after their "
                    "employment, except as required in the performance of their duties or "
                    "as authorized in writing by the Employer.\n\n"
                    "4.3 Upon termination of employment for any reason, the Employee shall "
                    "immediately return to the Employer all documents, records, files, "
                    "notebooks, and other materials containing Confidential Information, "
                    "including all copies thereof."
                ),
            ),
            Clause(
                id="emp-ip",
                title="Intellectual Property and Work Product",
                section_number="5",
                body=(
                    '5.1 All inventions, discoveries, improvements, works of authorship, '
                    "designs, formulas, ideas, processes, techniques, know-how, data, and "
                    "other work product, whether or not patentable or copyrightable, that are "
                    "conceived, developed, or made by the Employee, alone or jointly with "
                    "others, during the period of employment and that relate to the Employer's "
                    "business or result from any work performed for the Employer "
                    '(collectively, "Work Product") shall be the sole and exclusive property '
                    "of the Employer.\n\n"
                    "5.2 The Employee hereby irrevocably assigns to the Employer all right, "
                    "title, and interest in and to all Work Product, including all intellectual "
                    "property rights therein. The Employee agrees to execute all documents and "
                    "take all actions necessary to effectuate and confirm such assignment.\n\n"
                    "5.3 The Employee acknowledges that all Work Product that constitutes works "
                    "of authorship shall be considered \"works made for hire\" as defined under "
                    "the United States Copyright Act."
                ),
            ),
            Clause(
                id="emp-non-compete",
                title="Non-Competition and Non-Solicitation",
                section_number="6",
                body=(
                    "6.1 Non-Competition. During the Employee's employment and for a period of "
                    "[MONTHS] months following the termination of employment for any reason, "
                    "the Employee shall not, directly or indirectly, engage in, own, manage, "
                    "operate, control, be employed by, participate in, or be connected in any "
                    "manner with any business that competes with the Employer's business within "
                    "[GEOGRAPHIC AREA].\n\n"
                    "6.2 Non-Solicitation of Customers. During the Employee's employment and for "
                    "a period of [MONTHS] months following the termination of employment, the "
                    "Employee shall not, directly or indirectly, solicit or attempt to solicit "
                    "any customer, client, or account of the Employer for the purpose of "
                    "providing products or services competitive with those offered by the "
                    "Employer.\n\n"
                    "6.3 Non-Solicitation of Employees. During the Employee's employment and "
                    "for a period of [MONTHS] months following the termination of employment, "
                    "the Employee shall not, directly or indirectly, recruit, solicit, or "
                    "induce any employee or contractor of the Employer to terminate their "
                    "relationship with the Employer."
                ),
                is_optional=True,
                jurisdiction_notes=(
                    "Non-compete clauses are unenforceable in California (Cal. Bus. & Prof. "
                    "Code 16600) and restricted in many other states. Review local law."
                ),
            ),
            Clause(
                id="emp-termination",
                title="Termination",
                section_number="7",
                body=(
                    "7.1 Termination by Employer for Cause. The Employer may terminate the "
                    "Employee's employment immediately for Cause. \"Cause\" shall mean: "
                    "(a) material breach of this Agreement; (b) conviction of, or plea of "
                    "guilty or no contest to, a felony or any crime involving moral turpitude; "
                    "(c) willful misconduct or gross negligence in the performance of duties; "
                    "(d) fraud, embezzlement, or misappropriation of Employer property; or "
                    "(e) material violation of Employer policies.\n\n"
                    "7.2 Termination Without Cause. Either Party may terminate this Agreement "
                    "without Cause upon fourteen (14) days' prior written notice to the other "
                    "Party.\n\n"
                    "7.3 Effect of Termination. Upon termination of employment for any reason, "
                    "the Employer shall pay the Employee all earned but unpaid Base Salary, "
                    "accrued but unused PTO, and any other amounts required by applicable law, "
                    "through the date of termination."
                ),
            ),
            Clause(
                id="emp-governing-law",
                title="Governing Law and Dispute Resolution",
                section_number="8",
                body=(
                    "This Agreement shall be governed by and construed in accordance with the "
                    "laws of the State of [STATE], without regard to its conflict of laws "
                    "principles. Any dispute arising out of or relating to this Agreement or "
                    "the Employee's employment shall be resolved through binding arbitration "
                    "administered by the American Arbitration Association in accordance with "
                    "its Employment Arbitration Rules, and judgment on the award rendered by "
                    "the arbitrator(s) may be entered in any court having jurisdiction thereof."
                ),
            ),
            Clause(
                id="emp-miscellaneous",
                title="Miscellaneous",
                section_number="9",
                body=(
                    "9.1 Entire Agreement. This Agreement constitutes the entire agreement "
                    "between the Parties concerning the subject matter hereof and supersedes "
                    "all prior agreements and understandings.\n\n"
                    "9.2 Amendment. This Agreement may not be modified except by a written "
                    "instrument signed by both Parties.\n\n"
                    "9.3 Severability. If any provision of this Agreement is held to be "
                    "invalid or unenforceable, the remaining provisions shall remain in full "
                    "force and effect.\n\n"
                    "9.4 Waiver. The failure of either Party to enforce any provision of this "
                    "Agreement shall not constitute a waiver of such provision or the right "
                    "to enforce it at a later time.\n\n"
                    "9.5 Notices. All notices under this Agreement shall be in writing and "
                    "shall be deemed given when delivered personally, sent by confirmed "
                    "email, or sent by certified mail, return receipt requested."
                ),
            ),
        ]

    def _signature_block(self, employer: Party, employee: Party) -> str:
        return (
            f"IN WITNESS WHEREOF, the Parties have executed this Employment Agreement "
            f"as of the Effective Date.\n\n"
            f"EMPLOYER: {employer.name}\n\n"
            f"Signature: ___________________________\n"
            f"Name: {employer.representative or '[AUTHORIZED REPRESENTATIVE]'}\n"
            f"Title: {employer.title or '[TITLE]'}\n"
            f"Date: ___________________________\n\n"
            f"EMPLOYEE: {employee.name}\n\n"
            f"Signature: ___________________________\n"
            f"Date: ___________________________"
        )
