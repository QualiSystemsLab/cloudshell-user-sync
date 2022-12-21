import click
import pkg_resources
from cloudshell_user_sync.commands import view_config
from cloudshell_user_sync.commands import set_credential
from cloudshell_user_sync.commands import sync_groups
from cloudshell_user_sync.commands import run_service


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
    run_service.run_service_flow()


@cli.command()
def config():
    """View Currently Set Config"""
    view_config.view_config_json()


@cli.command()
@click.argument("user")
@click.argument("password")
@click.option("--target",
              required=True,
              type=click.Choice(["ldap", "cloudshell", "cs"], case_sensitive=False),
              help="Specify target credentials type. cloudshell / ldap.")
def credential(user, password, target):
    """Set Credentials For Cloudshell and LDAP"""
    click.echo(f"setting credential {user}, {password} to {target}")
    set_credential.set_credentials(user, password, target)
    click.secho("Credentials Set", fg="green")
