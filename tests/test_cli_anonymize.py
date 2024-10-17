from unittest import TestCase

from typer.testing import CliRunner

from anonymizer.cli import app

runner = CliRunner()


class TestAnonymizeFunction(TestCase):
    def test_anonymize(self):
        input_value = "Sensitive Data"
        expected_output = "\x1b[1;38;5;178m********* Data\x1b[0m"

        result = runner.invoke(app=app, args=[input_value])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(expected_output, result.output.strip())
