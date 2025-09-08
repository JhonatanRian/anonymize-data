import os
from unittest import TestCase

from typer.testing import CliRunner

from anonymizer_data.cli import app

runner = CliRunner()


class TestAnonymizeFunction(TestCase):
    def test_anonymize(self):
        os.environ["NO_COLOR"] = "1"
        input_value = "Sensitive Data"
        expected_output = "********* Data"

        result = runner.invoke(app=app, args=[input_value])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(expected_output, result.output.strip())
        del os.environ["NO_COLOR"]
