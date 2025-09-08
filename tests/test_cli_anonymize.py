from unittest import TestCase
from unittest.mock import patch

from typer.testing import CliRunner

from anonymizer_data.cli import app

runner = CliRunner()


class TestAnonymizeFunction(TestCase):
    @patch("rich.console.Console.print")
    def test_anonymize(self, mock_print):
        input_value = "Sensitive Data"
        expected_output = "********* Data"

        result = runner.invoke(app=app, args=[input_value])

        self.assertEqual(result.exit_code, 0)
        mock_print.assert_called_once_with(expected_output, style="#ccc010 bold")
