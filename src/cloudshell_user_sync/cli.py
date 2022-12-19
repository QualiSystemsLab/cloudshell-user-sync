import click
import pkg_resources
from cloudshell_user_sync.commands import sync_groups


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Display cloudshell-user-sync version"""
    click.echo("cloudshell-user-sync version " + pkg_resources.get_distribution("cloudshell-user-sync").version)


@cli.command()
def run():
    """Run Sync Groups Command"""
    click.echo("Starting User Sync...")
    sync_groups.sync_groups_flow()
    click.secho("Sync flow completed", fg="green")


@cli.command()
def service():
    """Install User Sync Service to run automatically"""
    pass


@cli.command()
def config():
    """View Currently Set Config"""
    pass


@cli.command()
@click.argument("user")
@click.argument("password")
@click.option("--target",
              required=True,
              type=click.Choice(["ldap", "cloudshell"], case_sensitive=False),
              help="Specify target credentials type. cloudshell / ldap.")
def credential(user, password, target):
    """Set Credentials For Cloudshell and LDAP"""
    click.echo(f"setting credential {user}, {password} to {target}")
    pass
