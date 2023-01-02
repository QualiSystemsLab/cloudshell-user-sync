"""
this module exists because click.echo throws exception when job is running as service
"""
import click


def safe_echo(msg):
    try:
        click.echo(msg)
    except:  # noqa: E722  # pylint: disable=bare-except
        pass


def safe_green_echo(msg):
    try:
        click.secho(msg, fg="green")
    except:  # noqa: E722  # pylint: disable=bare-except
        pass


def safe_yellow_echo(msg):
    try:
        click.secho(msg, fg="yellow")
    except:  # noqa: E722  # pylint: disable=bare-except
        pass
