"""Cmdline"""
import click

from crawlerstack_anticaptcha import __version__
from crawlerstack_anticaptcha.api.rest_api import start
from crawlerstack_anticaptcha.utils.log import init_log

init_log()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-V', '--version', is_flag=True, help='Show version and exit.')
def main(ctx, version):
    """captcha_cracker"""
    if version:
        click.echo(f'Version: {__version__}')

    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option('-h', '--host', default='0.0.0.0', show_default=True,
              help='The host of the api service')
@click.option('-p', '--port', default=8080, show_default=True, help='Api service port')
def api(host, port):
    """Start api service"""
    start(str(host), int(port))


if __name__ == '__main__':
    main()  # pylint:disable=no-value-for-parameter
