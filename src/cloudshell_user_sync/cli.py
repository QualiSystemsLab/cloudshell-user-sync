import click
import pkg_resources

from cloudshell_user_sync import exceptions
from cloudshell_user_sync.commands import run_service, set_config, set_credential, set_mapping, sync_groups


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Display CLI version"""
    click.echo("cloudshell-user-sync version " + pkg_resources.get_distribution("cloudshell-user-sync").version)


@cli.command()
def run():
    """Pull LDAP Data and sync to Cloudshell"""
    sync_groups.sync_groups_flow()


@cli.command()
@click.argument("action", required=True, type=click.Choice(["install", "update", "start"], case_sensitive=True))
@click.option(
    "--startup",
    required=False,
    type=click.Choice(["manual", "auto", "disabled", "delayed"], case_sensitive=True),
    default="auto",
    help="How the service starts. manual / auto. Default auto.",
)
def service(action, startup):
    """Install Windows service to run job automatically"""
    click.echo(f"Running service '{action}' action")
    if action == "install" and startup:
        click.echo(f"installing with startup type '{startup}'")
    run_service.run_service_flow()


@cli.command()
@click.argument("target", required=False, type=click.Choice(["ldap", "cloudshell", "cs", "service"], case_sensitive=False))
@click.argument("key", type=str, required=False)
@click.argument("value", type=str, required=False)
def config(target, key, value):
    """
    View or Set Config - Pass no params to view config
    """
    set_config.view_or_set_config(target, key, value)


@cli.command()
@click.argument("user")
@click.argument("password")
@click.option(
    "--target",
    required=True,
    type=click.Choice(["ldap", "cloudshell", "cs"], case_sensitive=False),
    help="Specify target credentials type. cloudshell / ldap.",
)
def credential(user, password, target):
    """Set Credentials For Cloudshell and LDAP"""
    click.echo(f"setting credentials for {target}")
    set_credential.set_credentials(user, password, target)
    click.secho("Credentials Set", fg="green")


@cli.command()
@click.argument("ldapgroup", required=False)
@click.option("--csgroups", required=False, help="Comma Separated List of Cloudshell groups - ex: group1,group2,group3")
@click.option("--delete", is_flag=True, show_default=True, default=False, help="Flag to delete the Target LDAP Group")
def mapping(ldapgroup, csgroups, delete):
    """Set LDAP group --> Cloudshell Groups Mapping"""
    params = [ldapgroup, csgroups, delete]
    if all(params):
        raise exceptions.FatalError("Not Valid Combination of parameters")
    if ldapgroup and csgroups:
        click.echo(f"setting mapping for {ldapgroup} --> {csgroups}")
        set_mapping.set_ldap_mapping(ldap_cn=ldapgroup, cloudshell_groups=csgroups)
        click.secho("Mapping Set", fg="green")
    elif ldapgroup and delete:
        set_mapping.delete_ldap_mapping(ldapgroup)
        click.secho(f"LDAP Group '{ldapgroup}' Deleted", fg="green")
    elif not any(params):
        set_mapping.view_mappings()
