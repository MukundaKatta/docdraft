"""Tests for the CLI interface."""

from click.testing import CliRunner

from docdraft.cli import cli


class TestCLI:
    def setup_method(self):
        self.runner = CliRunner()

    def test_version(self):
        result = self.runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_templates_command(self):
        result = self.runner.invoke(cli, ["templates"])
        assert result.exit_code == 0
        assert "nda" in result.output.lower()
        assert "employment" in result.output.lower()
        assert "service" in result.output.lower()
        assert "freelance" in result.output.lower()
        assert "privacy" in result.output.lower()
        assert "terms" in result.output.lower()

    def test_generate_nda(self):
        result = self.runner.invoke(
            cli, ["generate", "nda", "--party1", "Acme Corp", "--party2", "Jane Doe"]
        )
        assert result.exit_code == 0
        assert "NON-DISCLOSURE" in result.output

    def test_generate_nda_unilateral(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "nda",
                "--party1", "Acme Corp",
                "--party2", "Jane Doe",
                "--variant", "unilateral",
            ],
        )
        assert result.exit_code == 0
        assert "UNILATERAL" in result.output

    def test_generate_employment(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "employment",
                "--employer", "TechCo",
                "--employee", "John Smith",
            ],
        )
        assert result.exit_code == 0
        assert "EMPLOYMENT" in result.output

    def test_generate_service(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "service",
                "--provider", "Dev Agency",
                "--client", "StartupXYZ",
            ],
        )
        assert result.exit_code == 0
        assert "SERVICE" in result.output

    def test_generate_freelance(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "freelance",
                "--freelancer", "Jane Designer",
                "--client", "BigCorp",
            ],
        )
        assert result.exit_code == 0
        assert "CONTRACTOR" in result.output

    def test_generate_privacy(self):
        result = self.runner.invoke(
            cli,
            ["generate", "privacy", "--company", "MyApp Inc"],
        )
        assert result.exit_code == 0
        assert "PRIVACY" in result.output

    def test_generate_terms(self):
        result = self.runner.invoke(
            cli,
            ["generate", "terms", "--company", "SaaS Corp"],
        )
        assert result.exit_code == 0
        assert "TERMS" in result.output

    def test_generate_with_jurisdiction(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "nda",
                "--party1", "Acme",
                "--party2", "Bob",
                "--jurisdiction", "us-california",
            ],
        )
        assert result.exit_code == 0
        assert "California" in result.output

    def test_generate_with_industry(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "nda",
                "--party1", "Acme",
                "--party2", "Bob",
                "--industry", "technology",
            ],
        )
        assert result.exit_code == 0
        assert "source code" in result.output.lower()

    def test_generate_plain_format(self):
        result = self.runner.invoke(
            cli,
            [
                "generate", "nda",
                "--party1", "Acme",
                "--party2", "Bob",
                "--format", "plain",
            ],
        )
        assert result.exit_code == 0
        # Plain format uses === separators
        assert "=" * 10 in result.output

    def test_generate_to_file(self, tmp_path):
        output_file = tmp_path / "test_nda.md"
        result = self.runner.invoke(
            cli,
            [
                "generate", "nda",
                "--party1", "Acme",
                "--party2", "Bob",
                "-o", str(output_file),
            ],
        )
        assert result.exit_code == 0
        assert output_file.exists()
        content = output_file.read_text()
        assert "NON-DISCLOSURE" in content

    def test_report_empty(self):
        result = self.runner.invoke(cli, ["report"])
        assert result.exit_code == 0

    def test_missing_required_option(self):
        result = self.runner.invoke(cli, ["generate", "nda", "--party1", "Acme"])
        assert result.exit_code != 0
