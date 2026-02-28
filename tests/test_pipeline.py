import pytest
from unittest.mock import patch
from ngs_pipeline.pipeline import run_command
from ngs_pipeline.pipeline import run_pipeline


def test_run_command_success():

    run_command(["echo", "System test is a successful"])


def test_run_command_failure():

    with pytest.raises(FileNotFoundError):
        run_command(["The_command_that_not_existed"])


def test_run_pipeline(tmp_path):
    with patch("ngs_pipeline.pipeline.run_command") as mock_cmd:
        run_pipeline("input.fastq", "ref.fa", str(tmp_path))

        assert mock_cmd.call_count == 9
        first_arg = mock_cmd.call_args_list[3][0][0]

        expected_trimmed = str(tmp_path / "trimmed.fastq")
        assert first_arg == ["bwa", "mem", "ref.fa", expected_trimmed]
