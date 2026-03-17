"""Privacy Policy template."""

from __future__ import annotations

from docdraft.models import Clause, Document, DocumentType, Party, Term


class PrivacyPolicyTemplate:
    """Generates privacy policy documents."""

    name = "Privacy Policy"
    document_type = DocumentType.PRIVACY
    description = "Defines how an organization collects, uses, and protects personal data."

    def generate(
        self,
        company: Party,
        website: str = "[WEBSITE URL]",
        effective_date_str: str = "",
        term: Term | None = None,
        **kwargs,
    ) -> Document:
        preamble = (
            f"This Privacy Policy describes how {company.name} (\"we,\" \"us,\" or \"our\") "
            f"collects, uses, discloses, and protects the personal information of users "
            f"(\"you\" or \"your\") of our website located at {website} and any related "
            f"services, applications, or platforms (collectively, the \"Services\"). By "
            f"accessing or using our Services, you acknowledge that you have read, understood, "
            f"and agree to be bound by this Privacy Policy. If you do not agree with this "
            f"Privacy Policy, please do not use our Services."
        )

        doc = Document(
            title="PRIVACY POLICY",
            document_type=DocumentType.PRIVACY,
            parties=[company],
            preamble=preamble,
            metadata={"website": website},
        )

        for clause in self._build_clauses(company, website):
            doc.add_clause(clause)

        return doc

    def _build_clauses(self, company: Party, website: str) -> list[Clause]:
        return [
            Clause(
                id="priv-collection",
                title="Information We Collect",
                section_number="1",
                body=(
                    "1.1 Information You Provide Directly. We collect information that you "
                    "voluntarily provide to us when you: (a) create an account or register for "
                    "our Services; (b) make a purchase or transaction; (c) contact us with "
                    "inquiries or requests; (d) participate in surveys, promotions, or contests; "
                    "or (e) otherwise communicate with us. This information may include your "
                    "name, email address, postal address, telephone number, payment information, "
                    "and any other information you choose to provide.\n\n"
                    "1.2 Information Collected Automatically. When you access or use our "
                    "Services, we automatically collect certain information, including: "
                    "(a) device information such as your hardware model, operating system, "
                    "unique device identifiers, and mobile network information; "
                    "(b) log information such as access times, pages viewed, IP address, and "
                    "the page you visited before navigating to our Services; "
                    "(c) location information based on your IP address or, with your consent, "
                    "more precise location data from your mobile device; and "
                    "(d) information collected through cookies, pixel tags, web beacons, and "
                    "similar tracking technologies.\n\n"
                    "1.3 Information from Third Parties. We may receive information about you "
                    "from third parties, including business partners, marketing partners, "
                    "social media platforms, data brokers, and publicly available sources. We "
                    "may combine this information with other information we collect about you."
                ),
            ),
            Clause(
                id="priv-use",
                title="How We Use Your Information",
                section_number="2",
                body=(
                    "We use the information we collect for the following purposes: "
                    "(a) to provide, maintain, and improve our Services; "
                    "(b) to process transactions and send related information, including "
                    "purchase confirmations, invoices, and receipts; "
                    "(c) to send you technical notices, updates, security alerts, and "
                    "support and administrative messages; "
                    "(d) to respond to your comments, questions, and requests, and to "
                    "provide customer service; "
                    "(e) to communicate with you about products, services, offers, "
                    "promotions, rewards, and events offered by us and others, and to "
                    "provide news and information we think will be of interest to you; "
                    "(f) to monitor and analyze trends, usage, and activities in connection "
                    "with our Services; "
                    "(g) to detect, investigate, and prevent fraudulent transactions and other "
                    "illegal activities and to protect the rights and property of the company "
                    "and others; "
                    "(h) to personalize and improve the Services and provide content, features, "
                    "or advertisements that match user profiles or interests; "
                    "(i) to facilitate contests, sweepstakes, and promotions and to process "
                    "and deliver entries and rewards; and "
                    "(j) to comply with legal obligations and enforce our terms and policies."
                ),
            ),
            Clause(
                id="priv-sharing",
                title="How We Share Your Information",
                section_number="3",
                body=(
                    "3.1 We may share your personal information in the following circumstances: "
                    "(a) with service providers, contractors, and agents who perform services "
                    "on our behalf and need access to such information to carry out their work; "
                    "(b) in response to a request for information if we believe disclosure is in "
                    "accordance with, or required by, any applicable law, regulation, or legal "
                    "process; (c) if we believe your actions are inconsistent with our user "
                    "agreements or policies, or to protect the rights, property, and safety of "
                    "us or others; (d) in connection with, or during negotiations of, any "
                    "merger, sale of company assets, financing, or acquisition of all or a "
                    "portion of our business by another company; and (e) with your consent or "
                    "at your direction.\n\n"
                    "3.2 We may also share aggregated or de-identified information that cannot "
                    "reasonably be used to identify you.\n\n"
                    "3.3 We do not sell your personal information to third parties for their "
                    "direct marketing purposes without your explicit consent."
                ),
            ),
            Clause(
                id="priv-cookies",
                title="Cookies and Tracking Technologies",
                section_number="4",
                body=(
                    "4.1 We and our third-party partners use cookies, web beacons, pixel tags, "
                    "and similar tracking technologies to collect information about your "
                    "interactions with our Services. Cookies are small data files stored on "
                    "your device that help us improve our Services and your experience.\n\n"
                    "4.2 We use the following types of cookies: (a) Strictly Necessary Cookies, "
                    "which are essential for the operation of our Services; (b) Performance "
                    "Cookies, which collect information about how you use our Services; "
                    "(c) Functionality Cookies, which remember choices you make to improve your "
                    "experience; and (d) Targeting Cookies, which are used to deliver "
                    "advertisements relevant to you.\n\n"
                    "4.3 You can set your browser to refuse all or some browser cookies or to "
                    "alert you when websites set or access cookies. If you disable or refuse "
                    "cookies, some parts of the Services may become inaccessible or not "
                    "function properly."
                ),
            ),
            Clause(
                id="priv-security",
                title="Data Security",
                section_number="5",
                body=(
                    "5.1 We implement appropriate technical and organizational security "
                    "measures designed to protect the security, confidentiality, and integrity "
                    "of your personal information. These measures include encryption, access "
                    "controls, secure data storage, and regular security assessments.\n\n"
                    "5.2 However, no method of transmission over the Internet or electronic "
                    "storage is completely secure. While we strive to use commercially "
                    "acceptable means to protect your personal information, we cannot "
                    "guarantee its absolute security.\n\n"
                    "5.3 In the event of a data breach that compromises your personal "
                    "information, we will notify you and the relevant authorities in "
                    "accordance with applicable law."
                ),
            ),
            Clause(
                id="priv-rights",
                title="Your Rights and Choices",
                section_number="6",
                body=(
                    "6.1 Depending on your location, you may have the following rights "
                    "regarding your personal information: (a) the right to access and receive "
                    "a copy of your personal information; (b) the right to rectify or update "
                    "inaccurate or incomplete personal information; (c) the right to request "
                    "deletion of your personal information; (d) the right to restrict or object "
                    "to the processing of your personal information; (e) the right to data "
                    "portability; and (f) the right to withdraw consent where processing is "
                    "based on consent.\n\n"
                    "6.2 To exercise any of these rights, please contact us using the "
                    "information provided in Section 10 below. We will respond to your request "
                    "within the timeframe required by applicable law.\n\n"
                    "6.3 You may opt out of receiving promotional communications from us by "
                    "following the unsubscribe instructions included in each promotional email "
                    "or by contacting us directly."
                ),
                jurisdiction_notes=(
                    "Rights vary by jurisdiction. GDPR (EU), CCPA (California), LGPD (Brazil), "
                    "and other laws provide specific rights. Tailor to applicable law."
                ),
            ),
            Clause(
                id="priv-retention",
                title="Data Retention",
                section_number="7",
                body=(
                    "We retain your personal information for as long as necessary to fulfill "
                    "the purposes for which it was collected, including to satisfy any legal, "
                    "accounting, or reporting requirements. To determine the appropriate "
                    "retention period, we consider the amount, nature, and sensitivity of the "
                    "personal information, the potential risk of harm from unauthorized use or "
                    "disclosure, the purposes for which we process the information, whether we "
                    "can achieve those purposes through other means, and applicable legal "
                    "requirements."
                ),
            ),
            Clause(
                id="priv-children",
                title="Children's Privacy",
                section_number="8",
                body=(
                    "Our Services are not directed to children under the age of thirteen (13), "
                    "and we do not knowingly collect personal information from children under "
                    "thirteen (13). If we learn that we have collected personal information "
                    "from a child under thirteen (13), we will take steps to delete such "
                    "information as soon as possible. If you believe we have collected "
                    "information from a child under thirteen (13), please contact us "
                    "immediately using the information provided in Section 10."
                ),
            ),
            Clause(
                id="priv-changes",
                title="Changes to This Privacy Policy",
                section_number="9",
                body=(
                    "We may update this Privacy Policy from time to time. If we make material "
                    "changes, we will notify you by posting the updated policy on our website "
                    "and updating the \"Last Updated\" date at the top of this Privacy Policy. "
                    "We may also provide notice through our Services or by sending you an "
                    "email. Your continued use of our Services after the effective date of the "
                    "revised Privacy Policy constitutes your acceptance of the changes."
                ),
            ),
            Clause(
                id="priv-contact",
                title="Contact Us",
                section_number="10",
                body=(
                    f"If you have any questions, concerns, or requests regarding this Privacy "
                    f"Policy or our data practices, please contact us at:\n\n"
                    f"{company.name}\n"
                    f"{company.address}\n"
                    f"Email: {company.email or '[PRIVACY EMAIL]'}\n\n"
                    f"For EU residents, you have the right to lodge a complaint with your "
                    f"local data protection supervisory authority."
                ),
            ),
        ]
