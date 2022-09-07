"""Cmdline"""
import click

from crawlerstack_anticaptcha import __version__


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-V', '--version', is_flag=True, help='Show version and exit.')
def main(ctx, version):
    """captcha_cracker"""
    if version:
        click.echo(f'Version: {__version__}')

    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


if __name__ == '__main__':
    main()  # pylint:disable=E1120
