"""CLI interface for DOCDRAFT using Click and Rich."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from docdraft.generator.builder import DocumentBuilder
from docdraft.models import Industry, Jurisdiction, NDAVariant, OutputFormat
from docdraft.report import ReportGenerator
from docdraft.templates import TEMPLATE_REGISTRY

console = Console()
report_gen = ReportGenerator()


JURISDICTION_CHOICES = [j.value for j in Jurisdiction]
INDUSTRY_CHOICES = [i.value for i in Industry]
FORMAT_CHOICES = [f.value for f in OutputFormat]


@click.group()
@click.version_option(version="1.0.0", prog_name="docdraft")
def cli():
    """DOCDRAFT - AI Legal Document Generator.

    Generate professional legal documents from templates with
    jurisdiction-aware customization.
    """
    pass


@cli.command()
def templates():
    """List all available document templates."""
    table = Table(title="Available Templates", show_header=True, header_style="bold cyan")
    table.add_column("Type", style="bold")
    table.add_column("Name")
    table.add_column("Description")

    for key, tmpl_cls in TEMPLATE_REGISTRY.items():
        table.add_row(key, tmpl_cls.name, tmpl_cls.description)

    console.print(table)


@cli.group()
def generate():
    """Generate a legal document."""
    pass


@generate.command()
@click.option("--party1", required=True, help="Name of the first party")
@click.option("--party2", required=True, help="Name of the second party")
@click.option(
    "--variant",
    type=click.Choice(["mutual", "unilateral"]),
    default="mutual",
    help="NDA variant",
)
@click.option("--jurisdiction", type=click.Choice(JURISDICTION_CHOICES), default="us-general")
@click.option("--industry", type=click.Choice(INDUSTRY_CHOICES), default="general")
@click.option("--format", "output_format", type=click.Choice(FORMAT_CHOICES), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def nda(party1, party2, variant, jurisdiction, industry, output_format, output):
    """Generate a Non-Disclosure Agreement."""
    builder = DocumentBuilder(
        jurisdiction=Jurisdiction(jurisdiction),
        industry=Industry(industry),
        output_format=OutputFormat(output_format),
    )

    doc, text = builder.build_nda(
        party1_name=party1,
        party2_name=party2,
        variant=NDAVariant(variant),
    )

    report_gen.add_document(doc, text)
    _output_document(doc.title, text, output)


@generate.command()
@click.option("--employer", required=True, help="Employer name")
@click.option("--employee", required=True, help="Employee name")
@click.option("--title", "job_title", default="[JOB TITLE]", help="Job title")
@click.option("--salary", default="[SALARY]", help="Annual salary")
@click.option("--jurisdiction", type=click.Choice(JURISDICTION_CHOICES), default="us-general")
@click.option("--industry", type=click.Choice(INDUSTRY_CHOICES), default="general")
@click.option("--format", "output_format", type=click.Choice(FORMAT_CHOICES), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def employment(employer, employee, job_title, salary, jurisdiction, industry, output_format, output):
    """Generate an Employment Agreement."""
    builder = DocumentBuilder(
        jurisdiction=Jurisdiction(jurisdiction),
        industry=Industry(industry),
        output_format=OutputFormat(output_format),
    )

    doc, text = builder.build_employment(
        employer_name=employer,
        employee_name=employee,
        job_title=job_title,
        salary=salary,
    )

    report_gen.add_document(doc, text)
    _output_document(doc.title, text, output)


@generate.command()
@click.option("--provider", required=True, help="Service provider name")
@click.option("--client", required=True, help="Client name")
@click.option("--services", default="[DESCRIPTION OF SERVICES]", help="Services description")
@click.option("--fee", default="[FEE AMOUNT]", help="Service fee")
@click.option("--jurisdiction", type=click.Choice(JURISDICTION_CHOICES), default="us-general")
@click.option("--industry", type=click.Choice(INDUSTRY_CHOICES), default="general")
@click.option("--format", "output_format", type=click.Choice(FORMAT_CHOICES), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def service(provider, client, services, fee, jurisdiction, industry, output_format, output):
    """Generate a Service Agreement."""
    builder = DocumentBuilder(
        jurisdiction=Jurisdiction(jurisdiction),
        industry=Industry(industry),
        output_format=OutputFormat(output_format),
    )

    doc, text = builder.build_service(
        provider_name=provider,
        client_name=client,
        services_description=services,
        fee=fee,
    )

    report_gen.add_document(doc, text)
    _output_document(doc.title, text, output)


@generate.command()
@click.option("--freelancer", required=True, help="Freelancer name")
@click.option("--client", required=True, help="Client name")
@click.option("--project", default="[PROJECT DESCRIPTION]", help="Project description")
@click.option("--rate", default="[RATE]", help="Payment rate")
@click.option("--jurisdiction", type=click.Choice(JURISDICTION_CHOICES), default="us-general")
@click.option("--industry", type=click.Choice(INDUSTRY_CHOICES), default="general")
@click.option("--format", "output_format", type=click.Choice(FORMAT_CHOICES), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def freelance(freelancer, client, project, rate, jurisdiction, industry, output_format, output):
    """Generate a Freelance Contract."""
    builder = DocumentBuilder(
        jurisdiction=Jurisdiction(jurisdiction),
        industry=Industry(industry),
        output_format=OutputFormat(output_format),
    )

    doc, text = builder.build_freelance(
        freelancer_name=freelancer,
        client_name=client,
        project_description=project,
        rate=rate,
    )

    report_gen.add_document(doc, text)
    _output_document(doc.title, text, output)


@generate.command()
@click.option("--company", required=True, help="Company name")
@click.option("--website", default="[WEBSITE URL]", help="Website URL")
@click.option("--email", default=None, help="Privacy contact email")
@click.option("--jurisdiction", type=click.Choice(JURISDICTION_CHOICES), default="us-general")
@click.option("--industry", type=click.Choice(INDUSTRY_CHOICES), default="general")
@click.option("--format", "output_format", type=click.Choice(FORMAT_CHOICES), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def privacy(company, website, email, jurisdiction, industry, output_format, output):
    """Generate a Privacy Policy."""
    builder = DocumentBuilder(
        jurisdiction=Jurisdiction(jurisdiction),
        industry=Industry(industry),
        output_format=OutputFormat(output_format),
    )

    doc, text = builder.build_privacy(
        company_name=company,
        website=website,
        company_email=email,
    )

    report_gen.add_document(doc, text)
    _output_document(doc.title, text, output)


@generate.command()
@click.option("--company", required=True, help="Company name")
@click.option("--website", default="[WEBSITE URL]", help="Website URL")
@click.option("--service-name", default="[SERVICE NAME]", help="Name of the service")
@click.option("--email", default=None, help="Contact email")
@click.option("--jurisdiction", type=click.Choice(JURISDICTION_CHOICES), default="us-general")
@click.option("--industry", type=click.Choice(INDUSTRY_CHOICES), default="general")
@click.option("--format", "output_format", type=click.Choice(FORMAT_CHOICES), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def terms(company, website, service_name, email, jurisdiction, industry, output_format, output):
    """Generate Terms of Service."""
    builder = DocumentBuilder(
        jurisdiction=Jurisdiction(jurisdiction),
        industry=Industry(industry),
        output_format=OutputFormat(output_format),
    )

    doc, text = builder.build_terms(
        company_name=company,
        website=website,
        service_name=service_name,
        company_email=email,
    )

    report_gen.add_document(doc, text)
    _output_document(doc.title, text, output)


@cli.command()
def report():
    """Show a report of generated documents in this session."""
    summary = report_gen.summary()
    console.print(Panel(summary, title="Generation Report", border_style="green"))


def _output_document(title: str, text: str, output_path: str | None) -> None:
    """Output the generated document to console or file."""
    if output_path:
        path = Path(output_path)
        path.write_text(text, encoding="utf-8")
        console.print(
            Panel(
                f"Document saved to: {path.resolve()}",
                title=f"[bold green]{title}[/bold green]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                text,
                title=f"[bold green]{title}[/bold green]",
                border_style="blue",
                expand=False,
            )
        )


if __name__ == "__main__":
    cli()
