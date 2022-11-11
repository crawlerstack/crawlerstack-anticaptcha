""""test cmdline"""
from typing import List

import pytest
import uvicorn
from click.testing import CliRunner

from crawlerstack_anticaptcha import __version__, cmdline


@pytest.mark.parametrize(
    ['invoke_args', 'exit_code', 'output_keyword'],
    [
        ([], 0, 'help'),
        (['--help'], 0, 'help'),
        (['--version'], 0, __version__),
        (['-V'], 0, __version__)
    ]
)
def test_main(
        clicker: CliRunner,
        invoke_args: List[str],
        exit_code: int,
        output_keyword: str
):
    """test main"""
    result = clicker.invoke(cmdline.main, invoke_args)
    assert result.exit_code == exit_code
    assert output_keyword in result.output


@pytest.mark.parametrize(
    ['invoke_arg', 'exit_code'],
    [
        (['api'], 0)
    ]
)
def test_api(clicker, invoke_arg, exit_code, mocker):
    """test api"""
    start = mocker.patch.object(uvicorn, 'run')
    res = clicker.invoke(cmdline.main, invoke_arg)
    assert res.exit_code == exit_code
    start.assert_called()
