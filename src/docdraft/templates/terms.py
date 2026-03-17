"""Terms of Service template."""

from __future__ import annotations

from docdraft.models import Clause, Document, DocumentType, Party


class TermsOfServiceTemplate:
    """Generates terms of service documents."""

    name = "Terms of Service"
    document_type = DocumentType.TERMS
    description = "Defines rules and guidelines for using a service or platform."

    def generate(
        self,
        company: Party,
        website: str = "[WEBSITE URL]",
        service_name: str = "[SERVICE NAME]",
        **kwargs,
    ) -> Document:
        preamble = (
            f'These Terms of Service ("Terms") govern your access to and use of the '
            f"services, website, and applications (collectively, the \"Services\") provided "
            f"by {company.name} (\"we,\" \"us,\" or \"our\"), accessible at {website}. "
            f"Please read these Terms carefully before using our Services.\n\n"
            f"By accessing or using our Services, you agree to be bound by these Terms and "
            f"our Privacy Policy. If you do not agree to these Terms, you may not access or "
            f"use the Services. If you are using the Services on behalf of an organization, "
            f"you represent and warrant that you have the authority to bind that organization "
            f"to these Terms."
        )

        doc = Document(
            title="TERMS OF SERVICE",
            document_type=DocumentType.TERMS,
            parties=[company],
            preamble=preamble,
            metadata={"website": website, "service_name": service_name},
        )

        for clause in self._build_clauses(company, website, service_name):
            doc.add_clause(clause)

        return doc

    def _build_clauses(
        self, company: Party, website: str, service_name: str
    ) -> list[Clause]:
        return [
            Clause(
                id="tos-eligibility",
                title="Eligibility",
                section_number="1",
                body=(
                    "You must be at least eighteen (18) years of age, or the age of legal "
                    "majority in your jurisdiction, to use our Services. By using our Services, "
                    "you represent and warrant that you meet the eligibility requirements. If "
                    "you are using the Services on behalf of a business or other legal entity, "
                    "you represent that you have the authority to bind such entity to these Terms."
                ),
            ),
            Clause(
                id="tos-accounts",
                title="User Accounts",
                section_number="2",
                body=(
                    "2.1 To access certain features of the Services, you may be required to "
                    "create an account. You agree to provide accurate, current, and complete "
                    "information during the registration process and to update such information "
                    "to keep it accurate, current, and complete.\n\n"
                    "2.2 You are responsible for safeguarding your account credentials and for "
                    "all activities that occur under your account. You agree to notify us "
                    "immediately of any unauthorized use of your account or any other breach of "
                    "security.\n\n"
                    "2.3 We reserve the right to suspend or terminate your account at any time, "
                    "with or without cause, and with or without notice. You may delete your "
                    "account at any time by contacting us or through the account settings page."
                ),
            ),
            Clause(
                id="tos-acceptable-use",
                title="Acceptable Use Policy",
                section_number="3",
                body=(
                    "3.1 You agree not to use the Services to: (a) violate any applicable law, "
                    "regulation, or third-party right; (b) upload, transmit, or distribute any "
                    "content that is unlawful, harmful, threatening, abusive, harassing, "
                    "defamatory, vulgar, obscene, or otherwise objectionable; (c) impersonate "
                    "any person or entity or falsely state or misrepresent your affiliation "
                    "with any person or entity; (d) interfere with or disrupt the Services or "
                    "servers or networks connected to the Services; (e) attempt to gain "
                    "unauthorized access to any part of the Services or any other systems or "
                    "networks; (f) use any robot, spider, scraper, or other automated means to "
                    "access the Services without our prior written consent; (g) collect or "
                    "harvest any personal information of other users; (h) transmit any viruses, "
                    "worms, defects, Trojan horses, or other items of a destructive nature; or "
                    "(i) use the Services for any illegal or unauthorized purpose.\n\n"
                    "3.2 We reserve the right, but have no obligation, to monitor and investigate "
                    "any use of the Services and to remove or disable access to any content that "
                    "violates these Terms."
                ),
            ),
            Clause(
                id="tos-content",
                title="User Content",
                section_number="4",
                body=(
                    "4.1 You retain ownership of all content that you submit, post, or display "
                    'through the Services ("User Content"). By submitting User Content, you '
                    "grant us a worldwide, non-exclusive, royalty-free, sublicensable, and "
                    "transferable license to use, reproduce, distribute, prepare derivative "
                    "works of, display, and perform your User Content in connection with the "
                    "Services and our business operations.\n\n"
                    "4.2 You represent and warrant that: (a) you own or have the necessary "
                    "rights to submit your User Content; (b) your User Content does not "
                    "infringe upon the intellectual property or other rights of any third "
                    "party; and (c) your User Content complies with these Terms and all "
                    "applicable laws.\n\n"
                    "4.3 We are not responsible for any User Content submitted by users of "
                    "the Services. We do not endorse any User Content or any opinion, "
                    "recommendation, or advice expressed therein."
                ),
            ),
            Clause(
                id="tos-ip",
                title="Intellectual Property Rights",
                section_number="5",
                body=(
                    f"5.1 The Services and all content, features, and functionality thereof, "
                    f"including but not limited to text, graphics, logos, icons, images, audio "
                    f"clips, data compilations, software, and the compilation thereof, are the "
                    f"exclusive property of {company.name} or its licensors and are protected "
                    f"by copyright, trademark, patent, trade secret, and other intellectual "
                    f"property laws.\n\n"
                    f"5.2 Subject to your compliance with these Terms, we grant you a limited, "
                    f"non-exclusive, non-transferable, non-sublicensable, revocable license to "
                    f"access and use the Services for your personal or internal business "
                    f"purposes.\n\n"
                    f"5.3 You may not: (a) copy, modify, or distribute the Services or any "
                    f"content therein; (b) decompile, reverse engineer, or disassemble the "
                    f"Services; (c) remove any copyright or other proprietary notices; or "
                    f"(d) transfer the Services to another person or entity."
                ),
            ),
            Clause(
                id="tos-payment",
                title="Fees and Payment",
                section_number="6",
                body=(
                    "6.1 Certain features of the Services may require payment of fees. You "
                    "agree to pay all applicable fees as described on the Services in connection "
                    "with the features you select.\n\n"
                    "6.2 All fees are non-refundable except as expressly stated in these Terms "
                    "or as required by applicable law. We reserve the right to change our fees "
                    "at any time upon reasonable notice.\n\n"
                    "6.3 If you subscribe to a recurring plan, you authorize us to charge your "
                    "payment method on a recurring basis. You may cancel your subscription at "
                    "any time, and the cancellation will take effect at the end of the current "
                    "billing period.\n\n"
                    "6.4 You are responsible for all taxes associated with your use of the "
                    "Services, except for taxes based on our net income."
                ),
                is_optional=True,
            ),
            Clause(
                id="tos-disclaimers",
                title="Disclaimers",
                section_number="7",
                body=(
                    "THE SERVICES ARE PROVIDED \"AS IS\" AND \"AS AVAILABLE\" WITHOUT WARRANTIES "
                    "OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO "
                    "IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, "
                    "TITLE, AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SERVICES WILL BE "
                    "UNINTERRUPTED, SECURE, ERROR-FREE, OR FREE OF VIRUSES OR OTHER HARMFUL "
                    "COMPONENTS. YOUR USE OF THE SERVICES IS AT YOUR SOLE RISK. NO ADVICE OR "
                    "INFORMATION, WHETHER ORAL OR WRITTEN, OBTAINED FROM US OR THROUGH THE "
                    "SERVICES SHALL CREATE ANY WARRANTY NOT EXPRESSLY STATED IN THESE TERMS."
                ),
            ),
            Clause(
                id="tos-liability",
                title="Limitation of Liability",
                section_number="8",
                body=(
                    f"8.1 TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT "
                    f"SHALL {company.name.upper()}, ITS AFFILIATES, OFFICERS, DIRECTORS, "
                    f"EMPLOYEES, AGENTS, OR LICENSORS BE LIABLE FOR ANY INDIRECT, INCIDENTAL, "
                    f"SPECIAL, CONSEQUENTIAL, PUNITIVE, OR EXEMPLARY DAMAGES, INCLUDING BUT "
                    f"NOT LIMITED TO DAMAGES FOR LOSS OF PROFITS, GOODWILL, USE, DATA, OR "
                    f"OTHER INTANGIBLE LOSSES, ARISING OUT OF OR IN CONNECTION WITH YOUR USE "
                    f"OF OR INABILITY TO USE THE SERVICES.\n\n"
                    f"8.2 OUR TOTAL AGGREGATE LIABILITY TO YOU FOR ALL CLAIMS ARISING OUT OF "
                    f"OR RELATING TO THESE TERMS OR THE SERVICES SHALL NOT EXCEED THE GREATER "
                    f"OF: (A) THE AMOUNTS YOU HAVE PAID TO US IN THE TWELVE (12) MONTHS "
                    f"PRECEDING THE CLAIM; OR (B) ONE HUNDRED DOLLARS ($100.00).\n\n"
                    f"8.3 THE LIMITATIONS IN THIS SECTION APPLY REGARDLESS OF THE THEORY OF "
                    f"LIABILITY, WHETHER BASED ON WARRANTY, CONTRACT, TORT, NEGLIGENCE, STRICT "
                    f"LIABILITY, OR ANY OTHER LEGAL THEORY."
                ),
            ),
            Clause(
                id="tos-indemnification",
                title="Indemnification",
                section_number="9",
                body=(
                    "You agree to indemnify, defend, and hold harmless "
                    f"{company.name}, its affiliates, and their respective officers, directors, "
                    "employees, and agents from and against any and all claims, damages, "
                    "obligations, losses, liabilities, costs, and expenses (including "
                    "reasonable attorneys' fees) arising from: (a) your use of the Services; "
                    "(b) your violation of these Terms; (c) your violation of any third-party "
                    "right, including any intellectual property, privacy, or publicity right; "
                    "or (d) any User Content you submit through the Services."
                ),
            ),
            Clause(
                id="tos-termination",
                title="Termination",
                section_number="10",
                body=(
                    "10.1 We may terminate or suspend your access to the Services immediately, "
                    "without prior notice or liability, for any reason, including if you breach "
                    "these Terms.\n\n"
                    "10.2 Upon termination, your right to use the Services will immediately "
                    "cease. All provisions of these Terms that by their nature should survive "
                    "termination shall survive, including ownership provisions, warranty "
                    "disclaimers, indemnification, and limitations of liability.\n\n"
                    "10.3 You may terminate your account at any time by discontinuing use of "
                    "the Services and deleting your account."
                ),
            ),
            Clause(
                id="tos-governing-law",
                title="Governing Law and Dispute Resolution",
                section_number="11",
                body=(
                    "11.1 These Terms shall be governed by and construed in accordance with "
                    "the laws of the State of [STATE], without regard to its conflict of laws "
                    "principles.\n\n"
                    "11.2 Any dispute arising out of or relating to these Terms or the Services "
                    "shall be resolved through binding arbitration conducted in accordance with "
                    "the rules of the American Arbitration Association. The arbitration shall "
                    "take place in [CITY, STATE], and the arbitrator's decision shall be final "
                    "and binding.\n\n"
                    "11.3 Notwithstanding the foregoing, either Party may seek injunctive or "
                    "other equitable relief in any court of competent jurisdiction.\n\n"
                    "11.4 YOU AGREE THAT ANY DISPUTE RESOLUTION PROCEEDINGS WILL BE CONDUCTED "
                    "ONLY ON AN INDIVIDUAL BASIS AND NOT IN A CLASS, CONSOLIDATED, OR "
                    "REPRESENTATIVE ACTION."
                ),
            ),
            Clause(
                id="tos-changes",
                title="Changes to These Terms",
                section_number="12",
                body=(
                    "We reserve the right to modify these Terms at any time. If we make "
                    "material changes, we will provide notice through the Services or by other "
                    "means. Your continued use of the Services after the effective date of the "
                    "revised Terms constitutes your acceptance of the changes. If you do not "
                    "agree to the new Terms, you must stop using the Services."
                ),
            ),
            Clause(
                id="tos-miscellaneous",
                title="General Provisions",
                section_number="13",
                body=(
                    "13.1 Entire Agreement. These Terms, together with our Privacy Policy, "
                    "constitute the entire agreement between you and us regarding the Services.\n\n"
                    "13.2 Severability. If any provision of these Terms is found to be invalid "
                    "or unenforceable, the remaining provisions shall remain in full force and "
                    "effect.\n\n"
                    "13.3 Waiver. Our failure to enforce any right or provision of these Terms "
                    "shall not constitute a waiver of such right or provision.\n\n"
                    "13.4 Assignment. You may not assign these Terms without our prior written "
                    "consent. We may assign these Terms without restriction.\n\n"
                    f"13.5 Contact. If you have any questions about these Terms, please contact "
                    f"us at {company.email or '[CONTACT EMAIL]'}."
                ),
            ),
        ]
