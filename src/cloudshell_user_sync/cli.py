import click
import pkg_resources

from cloudshell_user_sync.commands import set_config
from cloudshell_user_sync.commands import set_credential
from cloudshell_user_sync.commands import sync_groups
from cloudshell_user_sync.commands import run_service
from cloudshell_user_sync.commands import set_mapping


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
@click.argument("target",
                required=False,
                type=click.Choice(["ldap", "cloudshell", "cs", "service"], case_sensitive=False))
@click.argument("key", type=str, required=False)
@click.argument("value", type=str, required=False)
def config(target, key, value):
    """
    View Or Set Config - Pass no params to view config
    """
    set_config.view_or_set_config(target, key, value)


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


@cli.command()
@click.argument("ldapgroup", required=False)
@click.argument("csgroups", required=False)
@click.option("--delete", is_flag=True, show_default=True, default=False, help="Delete the Target LDAP Group")
def mapping(ldapgroup, csgroups, delete):
    """Map LDAP group CN to Cloudshell Groups (pass comma separated)"""
    params = [ldapgroup, csgroups, delete]
    if ldapgroup and csgroups:
        click.echo(f"setting mapping for {ldapgroup} --> {csgroups}")
        set_mapping.set_ldap_mapping(ldap_cn=ldapgroup, cloudshell_groups=csgroups)
        click.secho("Mapping Set", fg="green")
    elif ldapgroup and delete:
        set_mapping.delete_ldap_mapping(ldapgroup)
        click.secho(f"LDAP Group {ldapgroup} Deleted", fg="green")
    elif not any(params):
        set_mapping.view_mappings()
