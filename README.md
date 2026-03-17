# DOCDRAFT - AI Legal Document Generator

DOCDRAFT is a Python CLI tool for generating professional legal documents from templates. It supports multiple document types with real legal language, jurisdiction-aware clause customization, and multiple output formats.

## Features

- **6 Complete Legal Document Templates**: NDA (mutual/unilateral), Employment Agreement, Service Agreement, Freelance Contract, Privacy Policy, Terms of Service
- **Jurisdiction-Aware Customization**: Adapts clauses based on jurisdiction (US states, UK, EU, Canada, Australia)
- **Industry-Specific Adjustments**: Tailors language for technology, healthcare, finance, and other industries
- **Multiple Output Formats**: Markdown and plain text
- **Interactive CLI**: Guided document creation with rich terminal output
- **Pydantic Models**: Validated document structures

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Generate an NDA
docdraft generate nda --party1 "Acme Corp" --party2 "Jane Doe" --variant mutual

# Generate an employment agreement
docdraft generate employment --employer "TechCo Inc" --employee "John Smith" --state "California"

# Generate a service agreement
docdraft generate service --provider "Dev Agency" --client "StartupXYZ"

# Generate a freelance contract
docdraft generate freelance --freelancer "Jane Designer" --client "BigCorp"

# Generate a privacy policy
docdraft generate privacy --company "MyApp Inc" --website "https://myapp.com"

# Generate terms of service
docdraft generate terms --company "SaaS Corp" --website "https://saas.example.com"

# List available templates
docdraft templates

# Output as plain text
docdraft generate nda --party1 "Acme" --party2 "Bob" --format plain

# Generate a report of created documents
docdraft report
```

## Project Structure

```
src/docdraft/
  cli.py              - Click CLI interface with rich output
  models.py           - Pydantic data models (Document, Clause, Party, Term)
  report.py           - Document generation reporting
  templates/
    nda.py             - NDA template (mutual/unilateral)
    employment.py      - Employment agreement template
    service.py         - Service agreement template
    freelance.py       - Freelance contract template
    privacy.py         - Privacy policy template
    terms.py           - Terms of service template
  generator/
    builder.py         - DocumentBuilder assembling documents
    customizer.py      - ClauseCustomizer for jurisdiction/industry
    formatter.py       - DocumentFormatter for markdown/plain text
```

## Requirements

- Python 3.10+
- pydantic
- click
- rich

## License

MIT
