import pytest
import subprocess
from ngs_pipeline.pipeline import run_command

def test_run_command_success():

    run_command(["echo", "System test is a successful"])
def test_run_command_failure():

    with pytest.raises(FileNotFoundError):
        run_command(["The_command_that_not_existed"])